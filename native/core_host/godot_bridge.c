/* Minimal C binding for the experimental single-owner core. MIT, Hiran Tiago Lins Borba. */
#include "godot_bridge.h"
#include "core_host.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <stddef.h>

/* Opaque aligned storage for the pinned 64-bit engine's String/StringName.
 * These small builtins are constructed/destroyed only through the Godot API. */
typedef union { max_align_t align; uint8_t bytes[64]; } Builtin;
_Static_assert(sizeof(void *) == 8, "Only 64-bit Godot builds are configured");
static GDExtensionClassLibraryPtr library;
static Builtin class_name, parent_name;
static GDExtensionInterfaceStringNameNewWithUtf8Chars name_new;
static GDExtensionInterfaceStringNewWithUtf8Chars string_new;
static GDExtensionInterfaceVariantStringify stringify;
static GDExtensionInterfaceStringToUtf8Chars to_utf8;
static GDExtensionInterfaceVariantGetType variant_type;
static GDExtensionInterfaceClassdbRegisterExtensionClass6 register_class;
static GDExtensionInterfaceClassdbRegisterExtensionClassMethod register_method;
static GDExtensionInterfaceClassdbUnregisterExtensionClass unregister_class;
static GDExtensionInterfaceClassdbConstructObject construct_object;
static GDExtensionInterfaceObjectSetInstance set_instance;
static GDExtensionPtrDestructor string_destroy, name_destroy;
static GDExtensionVariantFromTypeConstructorFunc string_variant;
typedef struct { int owns_core; } Bridge;
static int registered;

#define LOAD(destination, symbol) do { \
  GDExtensionInterfaceFunctionPtr p = get(symbol); \
  _Static_assert(sizeof(p)==sizeof(destination), "Function pointer ABI mismatch"); \
  memcpy(&(destination), &p, sizeof(p)); if (!(destination)) return 0; \
} while(0)
int alttp_godot_prepare(GDExtensionInterfaceGetProcAddress get, GDExtensionClassLibraryPtr lib) {
  library=lib;
  LOAD(name_new,"string_name_new_with_utf8_chars");
  LOAD(string_new,"string_new_with_utf8_chars");
  LOAD(stringify,"variant_stringify"); LOAD(to_utf8,"string_to_utf8_chars");
  LOAD(variant_type,"variant_get_type");
  LOAD(register_class,"classdb_register_extension_class6");
  LOAD(register_method,"classdb_register_extension_class_method");
  LOAD(unregister_class,"classdb_unregister_extension_class");
  LOAD(construct_object,"classdb_construct_object");
  LOAD(set_instance,"object_set_instance");
  GDExtensionInterfaceVariantGetPtrDestructor get_destructor;
  GDExtensionInterfaceGetVariantFromTypeConstructor get_constructor;
  LOAD(get_destructor,"variant_get_ptr_destructor");
  LOAD(get_constructor,"get_variant_from_type_constructor");
  string_destroy=get_destructor(GDEXTENSION_VARIANT_TYPE_STRING);
  name_destroy=get_destructor(GDEXTENSION_VARIANT_TYPE_STRING_NAME);
  string_variant=get_constructor(GDEXTENSION_VARIANT_TYPE_STRING);
  return string_destroy && name_destroy && string_variant;
}
static void return_string(GDExtensionVariantPtr out,const char *text) {
  Builtin string;
  string_new(&string,text);
  string_variant(out,&string);
  string_destroy(&string);
}
static char *argument_string(GDExtensionConstVariantPtr value) {
  if (variant_type(value)!=GDEXTENSION_VARIANT_TYPE_STRING) return NULL;
  Builtin string;
  /* variant_stringify writes to an initialized String. */
  string_new(&string,"");
  stringify(value,&string);
  GDExtensionInt size=to_utf8(&string,NULL,0);
  if(size<0 || size>32768) { string_destroy(&string);return NULL; }
  char *text=calloc((size_t)size+1,1);
  if(text) to_utf8(&string,text,size);
  string_destroy(&string);
  return text;
}
static void error_reply(GDExtensionVariantPtr out,const char *text) {
  char reply[2048];size_t pos=0;
  const char *prefix="{\"ok\":false,\"error\":\"";
  memcpy(reply,prefix,strlen(prefix));pos=strlen(prefix);
  for(size_t i=0;text[i] && pos+8<sizeof(reply);i++) {
    unsigned char c=(unsigned char)text[i];
    if(c=='"' || c=='\\')reply[pos++]='\\';
    if(c<32) { reply[pos++]=' ';continue; }
    reply[pos++]=(char)c;
  }
  reply[pos++]='"';reply[pos++]='}';reply[pos]=0;
  return_string(out,reply);
}
static void request(void *userdata,GDExtensionClassInstancePtr instance,
 const GDExtensionConstVariantPtr *args,GDExtensionInt count,
 GDExtensionVariantPtr out,GDExtensionCallError *error) {
  (void)userdata;
  error->error=GDEXTENSION_CALL_OK;
  if(count<2 || count>3) { error_reply(out,"request expects operation, payload, and optional SRAM path strings");return; }
  char *op=argument_string(args[0]),*payload=argument_string(args[1]);
  char *sram=count==3?argument_string(args[2]):NULL;
  if(!op || !payload || (count==3&&!sram)) {
    error_reply(out,"Arguments must be strings of at most 32768 bytes");goto done;
  }
  Bridge *self=instance;
  if(!strcmp(op,"open")) {
    if(alttp_core_open(payload,sram)) { self->owns_core=1;return_string(out,alttp_core_json()); }
    else error_reply(out,alttp_core_error());
  } else if(!self->owns_core) error_reply(out,"This bridge does not own an open core session");
  else if(!strcmp(op,"step")) {
    char *end;errno=0;unsigned long buttons=strtoul(payload,&end,10);
    if(errno || !*payload || *end || buttons>4095) error_reply(out,"Expected a decimal low-12-bit input mask");
    else if(alttp_core_step((uint32_t)buttons)) return_string(out,alttp_core_json());
    else error_reply(out,alttp_core_error());
  } else if(!strcmp(op,"snapshot")) return_string(out,alttp_core_json());
  else if(!strcmp(op,"frame")) return_string(out,alttp_core_frame_hex());
  else if(!strcmp(op,"close")) { alttp_core_close();self->owns_core=0;return_string(out,"{\"ok\":true}"); }
  else error_reply(out,"Unknown operation");
done:
  free(op);free(payload);free(sram);
}
static GDExtensionObjectPtr create_instance(void *userdata,GDExtensionBool notify) {
  (void)userdata;(void)notify;
  Bridge *self=calloc(1,sizeof(*self));
  if(!self)return NULL;
  /* The compatibility constructor performs built-in postinitialization;
   * this lightweight Object adds no virtual notification overrides. */
  GDExtensionObjectPtr object=construct_object(&parent_name);
  set_instance(object,&class_name,self);
  return object;
}
static void free_instance(void *userdata,GDExtensionClassInstancePtr instance) {
  (void)userdata;Bridge *self=instance;
  if(self->owns_core)alttp_core_close();free(self);
}
void alttp_godot_register(void) {
  name_new(&class_name,"AlttpCoreBridge");name_new(&parent_name,"Object");
  GDExtensionClassCreationInfo6 info={0};
  info.is_exposed=1;info.create_instance_func=create_instance;info.free_instance_func=free_instance;
  register_class(library,&class_name,&parent_name,&info);
  Builtin name,empty_name,empty_string;
  name_new(&name,"request");name_new(&empty_name,"");string_new(&empty_string,"");
  GDExtensionPropertyInfo result={0};result.type=GDEXTENSION_VARIANT_TYPE_STRING;
  result.name=&empty_name;result.class_name=&empty_name;result.hint_string=&empty_string;
  GDExtensionClassMethodInfo method={0};method.name=&name;method.call_func=request;
  method.method_flags=GDEXTENSION_METHOD_FLAG_NORMAL|GDEXTENSION_METHOD_FLAG_VARARG;
  method.has_return_value=1;method.return_value_info=&result;
  register_method(library,&class_name,&method);
  string_destroy(&empty_string);name_destroy(&empty_name);name_destroy(&name);
  registered=1;
}
void alttp_godot_unregister(void) {
  if(!registered)return;
  alttp_core_close();unregister_class(library,&class_name);
  name_destroy(&parent_name);name_destroy(&class_name);registered=0;
}
