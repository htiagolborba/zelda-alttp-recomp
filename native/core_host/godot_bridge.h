#ifndef ALTTP_GODOT_CORE_BRIDGE_H
#define ALTTP_GODOT_CORE_BRIDGE_H
#include "gdextension_interface.h"
int alttp_godot_prepare(GDExtensionInterfaceGetProcAddress get, GDExtensionClassLibraryPtr library);
void alttp_godot_register(void);
void alttp_godot_unregister(void);
#endif
