extends Node3D
## Original geometric art laboratory. No gameplay simulation or game assets.

const EXTENSION_PATH := "res://native/alttp_probe.gdextension"
var core_session: Node
var reference_view: TextureRect
var player_marker: Node3D
var marker_origin := Vector2.ZERO
var last_generation := -1
var core_smoke := false
var camera: Camera3D
var hud: Label
var frame_times: Array[float] = []
var frame_count := 0
var capture_path := ""
var report_path := ""
var assets_path := ""
var sram_path := ""
var finishing := false
var native_loaded := false

func _ready() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--assets="):
			assets_path = argument.trim_prefix("--assets=")
		if argument.begins_with("--sram="):
			sram_path = argument.trim_prefix("--sram=")
		if argument == "--core-smoke":
			core_smoke = true
		if argument.begins_with("--capture="):
			capture_path = argument.trim_prefix("--capture=")
		if argument.begins_with("--report="):
			report_path = argument.trim_prefix("--report=")
	var version := Engine.get_version_info()
	if version.major != 4 or version.minor != 7 or version.patch != 2:
		push_error("This prototype requires the pinned Godot 4.7.2 build.")
		get_tree().quit(2)
		return
	if not GDExtensionManager.is_extension_loaded(EXTENSION_PATH):
		GDExtensionManager.load_extension(EXTENSION_PATH)
	native_loaded = GDExtensionManager.is_extension_loaded(EXTENSION_PATH)
	if not native_loaded:
		push_error("Native probe missing. Run scripts/build-godot-probe.py first.")
		get_tree().quit(2)
		return
	_build_scene()
	print("ALTTP_SCENE_READY native_loaded=true gameplay_connected=false")
	if "--core-api-smoke" in OS.get_cmdline_user_args():
		_run_core_api_smoke()
		return
	if not assets_path.is_empty():
		_connect_core()
	elif core_smoke:
		push_error("--core-smoke requires --assets")
		get_tree().quit(2)
	if "--smoke" in OS.get_cmdline_user_args():
		_finish.call_deferred(false)

func _material(color: Color, roughness := 0.65) -> StandardMaterial3D:
	var material := StandardMaterial3D.new()
	material.albedo_color = color
	material.roughness = roughness
	return material

func _mesh(shape: Mesh, position_at: Vector3, material: Material) -> MeshInstance3D:
	var instance := MeshInstance3D.new()
	instance.mesh = shape
	instance.position = position_at
	instance.material_override = material
	add_child(instance)
	return instance

func _box(size: Vector3, position_at: Vector3, material: Material) -> MeshInstance3D:
	var shape := BoxMesh.new()
	shape.size = size
	return _mesh(shape, position_at, material)

func _sphere(radius: float, position_at: Vector3, material: Material) -> MeshInstance3D:
	var shape := SphereMesh.new()
	shape.radius = radius
	shape.height = radius * 2.0
	return _mesh(shape, position_at, material)

func _build_scene() -> void:
	var environment := WorldEnvironment.new()
	var settings := Environment.new()
	settings.background_mode = Environment.BG_COLOR
	settings.background_color = Color("17252a")
	settings.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	settings.ambient_light_color = Color("cfdfec")
	settings.ambient_light_energy = 0.6
	environment.environment = settings
	add_child(environment)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-48, -30, 0)
	sun.light_color = Color("fff1d4")
	sun.light_energy = 1.6
	sun.shadow_enabled = true
	add_child(sun)
	camera = Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 15.0
	camera.position = Vector3(10, 14, 14)
	add_child(camera)
	camera.look_at(Vector3(0, 0.4, 0))
	camera.current = true
	var grass := _material(Color("75a854"))
	var soil := _material(Color("685142"))
	var path := _material(Color("ddc494"))
	var wall := _material(Color("f1dcb4"))
	var roof := _material(Color("ad5f45"), 0.48)
	var dark := _material(Color("403d33"))
	var foliage := _material(Color("3d7656"), 0.5)
	var bark := _material(Color("886047"))
	_box(Vector3(12, 0.7, 10), Vector3(0, -0.55, 0), soil)
	_box(Vector3(12, 0.12, 10), Vector3(0, -0.14, 0), grass)
	_box(Vector3(1.5, 0.05, 5), Vector3(0, -0.05, 2.5), path)
	_box(Vector3(3, 1.9, 2.5), Vector3(0, 0.92, -1.5), wall)
	var roof_shape := PrismMesh.new()
	roof_shape.size = Vector3(3.6, 1.3, 3.1)
	_mesh(roof_shape, Vector3(0, 2.48, -1.5), roof)
	_box(Vector3(0.8, 1.3, 0.1), Vector3(0, 0.6, -0.2), dark)
	_box(Vector3(0.65, 0.6, 0.1), Vector3(1, 1.1, -0.2), _material(Color("87c5ce"), 0.2))
	for point in [Vector3(-4, 0, -2.5), Vector3(-3.8, 0, 2), Vector3(3.8, 0, -2.6), Vector3(4, 0, 1.8)]:
		_box(Vector3(0.35, 1.2, 0.35), point + Vector3(0, 0.55, 0), bark)
		_sphere(1.05, point + Vector3(0, 1.8, 0), foliage)
	for point in [Vector3(-2, 0.2, 1.6), Vector3(2.8, 0.2, 3.5)]:
		_sphere(0.45, point, foliage)
	var token := CylinderMesh.new()
	token.top_radius = 0.25
	token.bottom_radius = 0.35
	token.height = 0.6
	player_marker = Node3D.new()
	add_child(player_marker)
	var marker_body := _mesh(token, Vector3(0, 0.3, 2), _material(Color("4b9c79"), 0.35))
	var marker_head := _sphere(0.23, Vector3(0, 0.78, 2), _material(Color("e7c392")))
	# Only the geometric marker follows native snapshots, never a Godot controller.
	marker_body.reparent(player_marker)
	marker_head.reparent(player_marker)
	var canvas := CanvasLayer.new()
	add_child(canvas)
	hud = Label.new()
	hud.position = Vector2(24, 20)
	hud.add_theme_color_override("font_color", Color("f2f3df"))
	hud.add_theme_color_override("font_shadow_color", Color("17252a"))
	hud.add_theme_constant_override("shadow_offset_x", 2)
	hud.add_theme_constant_override("shadow_offset_y", 2)
	hud.add_theme_font_size_override("font_size", 19)
	canvas.add_child(hud)
	_update_hud()

func _update_hud() -> void:
	hud.text = "ZELDA ALTTP / 3D LABORATORY — M0\nHiran Tiago Lins Borba · Toronto, ON, CA\n\nNative extension loaded · original procedural geometry\nGameplay core NOT connected · no ROM required\n\nRenderer: %s\nMouse wheel: zoom · Escape: exit" % RenderingServer.get_current_rendering_method()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		finishing = true
		if core_session != null:
			core_session.running = false
		_finish.call_deferred(false)
	if event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			camera.size = maxf(8.0, camera.size - 0.5)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			camera.size = minf(22.0, camera.size + 0.5)

func _process(delta: float) -> void:
	if not native_loaded or finishing:
		return
	frame_count += 1
	if frame_count > 30 and frame_times.size() < 14400:
		frame_times.append(delta * 1000.0)
	if not core_smoke and not capture_path.is_empty() and frame_count >= 90:
		finishing = true
		_finish(true)

func _finish(capture: bool) -> void:
	if capture:
		await RenderingServer.frame_post_draw
		var error := get_viewport().get_texture().get_image().save_png(capture_path)
		if error != OK:
			push_error("Could not save viewport capture: %s" % error)
			get_tree().quit(3)
			return
	var samples := frame_times.duplicate()
	samples.sort()
	var report := {
		"stage": "M1" if core_session != null else "M0", "engine": Engine.get_version_info().string,
		"os": OS.get_name(), "renderer": RenderingServer.get_current_rendering_method(),
		"adapter": RenderingServer.get_video_adapter_name(),
		"native_extension_loaded": native_loaded, "gameplay_core_connected": core_session != null and core_session.connected,
		"sample_count": samples.size(), "frame_p95_ms": null,
		"note": "Diagnostic integration only; not the 120-second gameplay benchmark."
	}
	if core_session != null:
		report["core_snapshot"] = core_session.latest
		report["audio_output"] = "muted; 534-sample APU batch per simulation tick"
		report["save_policy"] = "read-only SRAM import; no save writes"
	if not samples.is_empty():
		report.frame_p95_ms = samples[mini(samples.size() - 1, int(ceil(samples.size() * 0.95)) - 1)]
	if not report_path.is_empty():
		var file := FileAccess.open(report_path, FileAccess.WRITE)
		if file == null:
			push_error("Cannot write report")
			get_tree().quit(3)
			return
		file.store_string(JSON.stringify(report, "\t"))
	print("ALTTP_M1_REPORT " if core_session != null else "ALTTP_M0_REPORT ", JSON.stringify(report))
	get_tree().quit(0)

func _connect_core() -> void:
	Engine.physics_ticks_per_second = 60
	core_session = load("res://scenes/core_session.gd").new()
	core_session.failed.connect(_core_failed)
	core_session.snapshot_updated.connect(_core_updated)
	add_child(core_session)
	if not core_session.start(assets_path, sram_path, core_smoke):
		get_tree().quit(2)
		return
	var canvas := CanvasLayer.new()
	add_child(canvas)
	reference_view = TextureRect.new()
	reference_view.position = Vector2(760, 252)
	reference_view.size = Vector2(512, 448)
	reference_view.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	canvas.add_child(reference_view)
	player_marker.visible = false

func _core_failed(message: String) -> void:
	push_error("C integration error: " + message)
	get_tree().quit(2)

func _core_updated(state: Dictionary) -> void:
	player_marker.visible = bool(state.player_active)
	if player_marker.visible:
		if int(state.scene_generation) != last_generation:
			marker_origin = Vector2(state.x, state.y)
			last_generation = int(state.scene_generation)
		player_marker.position = Vector3((state.x - marker_origin.x) / 16.0, 0, (state.y - marker_origin.y) / 16.0)
	hud.text = "ZELDA ALTTP / C INTEGRATION — M1 EXPERIMENT
Hiran Tiago Lins Borba · Toronto, ON, CA

C core connected · 60 simulation ticks/s target
Audio synthesized but muted · save writes disabled
3D environment is illustrative, NOT collision-aligned

Tick %d · module %d/%d · area %d · room %d
Player: (%d, %d) · raw Z: %d

Arrows: move · Enter: Start · Z/X/A/S: B/A/Y/X
Right panel: live reference from the SAME simulation
Mouse wheel: zoom · Escape: exit" % [state.tick, state.module, state.submodule, state.area, state.room, state.x, state.y, state.z_raw]
	if int(state.tick) % 6 == 0:
		var image: Image = core_session.reference_image()
		if image != null:
			if reference_view.texture == null:
				reference_view.texture = ImageTexture.create_from_image(image)
			else:
				reference_view.texture.update(image)
	if core_smoke and int(state.tick) >= 240 and not finishing:
		finishing = true
		core_session.running = false
		print("ALTTP_CORE_SMOKE_PASSED ticks=240")
		_finish.call_deferred(not capture_path.is_empty())

func _run_core_api_smoke() -> void:
	var extension := "res://native/alttp_core.gdextension"
	if not GDExtensionManager.is_extension_loaded(extension):
		GDExtensionManager.load_extension(extension)
	if not ClassDB.class_exists("AlttpCoreBridge"):
		_core_failed("Core bridge class was not registered")
		return
	var api: Object = ClassDB.instantiate("AlttpCoreBridge")
	var missing: Dictionary = JSON.parse_string(api.call("request", "open", "/alttp-nonexistent-local-assets.dat"))
	var unopened: Dictionary = JSON.parse_string(api.call("request", "step", "0"))
	var wrong_type: Dictionary = JSON.parse_string(api.call("request", "step", 123))
	api.free()
	if missing.get("ok", true) or unopened.get("ok", true) or wrong_type.get("ok", true):
		_core_failed("Structured error handling failed at native boundary")
		return
	print("ALTTP_CORE_API_SMOKE_PASSED no_assets=true")
	_finish.call_deferred(false)
