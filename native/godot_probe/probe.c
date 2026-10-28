/* Copyright (c) 2026 Hiran Tiago Lins Borba. MIT; see root LICENSE.
 * Base M0 probe; ALTTP_WITH_CORE_HOST additionally registers the M1 C bridge. */
#include "gdextension_interface.h"
#ifdef ALTTP_WITH_CORE_HOST
#include "godot_bridge.h"
#endif
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#ifdef _WIN32
#define ALTTP_EXPORT __declspec(dllexport)
#else
#define ALTTP_EXPORT __attribute__((visibility("default")))
#endif

#define ALTTP_PROBE_ABI 1u
static uint32_t initialized;
static GDExtensionGodotVersion2 engine_version;

ALTTP_EXPORT uint32_t alttp_probe_abi_version(void) { return ALTTP_PROBE_ABI; }
ALTTP_EXPORT uint32_t alttp_probe_is_initialized(void) { return initialized; }

static void probe_initialize(void *userdata, GDExtensionInitializationLevel level) {
  (void)userdata;
  if (level != GDEXTENSION_INITIALIZATION_SCENE) return;
  initialized = 1;
#ifdef ALTTP_WITH_CORE_HOST
  alttp_godot_register();
#endif
  printf("ALTTP_NATIVE_READY abi=%u godot=%u.%u.%u\n", ALTTP_PROBE_ABI,
         engine_version.major, engine_version.minor, engine_version.patch);
  fflush(stdout);
}

static void probe_deinitialize(void *userdata, GDExtensionInitializationLevel level) {
  (void)userdata;
  if (level != GDEXTENSION_INITIALIZATION_SCENE) return;
  initialized = 0;
#ifdef ALTTP_WITH_CORE_HOST
  alttp_godot_unregister();
#endif
  puts("ALTTP_NATIVE_STOPPED");
  fflush(stdout);
}

ALTTP_EXPORT GDExtensionBool alttp_probe_init(
    GDExtensionInterfaceGetProcAddress get_proc, GDExtensionClassLibraryPtr library,
    GDExtensionInitialization *initialization) {
  (void)library;
  if (!get_proc || !initialization) return 0;
  GDExtensionInterfaceFunctionPtr function = get_proc("get_godot_version2");
  GDExtensionInterfaceGetGodotVersion2 get_version;
  _Static_assert(sizeof(function) == sizeof(get_version), "Function pointer ABI mismatch");
  memcpy(&get_version, &function, sizeof(get_version));
  if (!get_version) return 0;
  get_version(&engine_version);
  if (engine_version.major != 4 || engine_version.minor != 7 || engine_version.patch != 2) {
    fputs("ALTTP_NATIVE_ERROR: this probe is pinned to Godot 4.7.2\n", stderr);
    return 0;
  }
#ifdef ALTTP_WITH_CORE_HOST
  if (!alttp_godot_prepare(get_proc, library)) return 0;
#endif
  initialization->minimum_initialization_level = GDEXTENSION_INITIALIZATION_SCENE;
  initialization->userdata = NULL;
  initialization->initialize = probe_initialize;
  initialization->deinitialize = probe_deinitialize;
  return 1;
}
