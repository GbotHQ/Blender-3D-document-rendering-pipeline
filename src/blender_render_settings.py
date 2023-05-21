import bpy


def warn_about_device_fallback(device, device_to_fallback_to):
    print(
        f"Failed to enable {device}, falling back to {device_to_fallback_to}"
        f""" (when rendering from a command line, use [--engine CYCLES] with [--cycles-device {device}] and ignore this message)"""
    )


data = bpy.data
renderer = bpy.ops.render
preferences = bpy.context.preferences
cycles_preferences = preferences.addons["cycles"].preferences


def enable_cycles_devices(device_type):
    cycles_preferences.compute_device_type = device_type

    enabled_device = False
    for device in bpy.context.preferences.addons["cycles"].preferences.devices:
        if device.type == device_type:
            device.use = True
            enabled_device = True
        else:
            device.use = False

    return enabled_device


def enable_cycles_gpu(cycles):
    device = "OPTIX"
    if enable_cycles_devices(device):
        cycles.device = "GPU"
        return True
    warn_about_device_fallback(device, "CUDA")

    device = "CUDA"
    if enable_cycles_devices(device):
        cycles.device = "GPU"
        return True
    warn_about_device_fallback(device, "CPU")

    return False


def set_render_engine_cycles(cycles, cycles_device, cycles_samples, cycles_denoise):
    cycles.preview_samples = cycles_samples
    cycles.samples = cycles_samples
    cycles.use_denoising = cycles_denoise

    if cycles_device == "gpu" and not enable_cycles_gpu(cycles):
        cycles_device = "cpu"

    if cycles_device == "cpu":
        cycles.device = "CPU"
    elif cycles_device != "gpu":
        raise ValueError(f"{cycles_device} is not a valid device")


class RenderSettings:
    def __init__(self):
        self.scene = data.scenes["Scene"]
        self.file_output = self.scene.node_tree.nodes["File Output"]
        self.cycles = self.scene.cycles

    @property
    def render_resolution(self):
        return self.scene.render.resolution_x, self.scene.render.resolution_y

    @render_resolution.setter
    def render_resolution(self, resolution):
        self.scene.render.resolution_x = resolution[0]
        self.scene.render.resolution_y = resolution[1]

    def set_render_engine(
        self,
        render_engine,
        cycles_device="gpu",
        cycles_samples=8,
        cycles_denoise=True,
    ):
        if render_engine == "cycles":
            set_render_engine_cycles(
                self.cycles, cycles_device, cycles_samples, cycles_denoise
            )
            self.scene.render.engine = "CYCLES"
        elif render_engine == "eevee":
            self.scene.render.engine = "BLENDER_EEVEE"
        elif render_engine == "workbench":
            self.scene.render.engine = "BLENDER_WORKBENCH"
        else:
            raise ValueError(f"{render_engine} is not a valid render engine")

    @property
    def output_path(self):
        return self.file_output.base_path

    @output_path.setter
    def output_path(self, path):
        self.file_output.base_path = str(path)

    @property
    def compression_ratio(self):
        return self.file_output.file_slots["image"].format.compression

    @compression_ratio.setter
    def compression_ratio(self, ratio):
        self.file_output.file_slots["image"].format.compression = ratio
        self.file_output.file_slots["coordinates"].format.compression = ratio

    @property
    def current_frame(self):
        return self.scene.frame_current

    @current_frame.setter
    def current_frame(self, index):
        self.scene.frame_current = index

    def render(self):
        renderer.render(scene="Scene")
