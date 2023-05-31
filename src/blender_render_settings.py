import bpy


def warn_about_device_fallback(device, device_to_fallback_to):
    print(f"""Failed to enable {device}, falling back to {device_to_fallback_to}""")


data = bpy.data
renderer = bpy.ops.render
preferences = bpy.context.preferences
cycles_preferences = preferences.addons["cycles"].preferences


def enable_cycles_devices(device_type):
    cycles_preferences.compute_device_type = device_type

    cycles_preferences.get_devices()

    enabled_device = False
    for device in bpy.context.preferences.addons["cycles"].preferences.devices:
        if device.type == device_type:
            device.use = True
            enabled_device = True
        else:
            device.use = False

    return enabled_device


def enable_cycles_gpu(device: str):
    if device == "OPTIX":
        if enable_cycles_devices(device):
            return True
        warn_about_device_fallback(device, "CUDA")

    device = "CUDA"
    if enable_cycles_devices(device):
        return True
    warn_about_device_fallback(device, "CPU")

    return False


def set_render_engine_cycles(cycles, device, samples, denoise):
    cycles.preview_samples = samples
    cycles.samples = samples
    cycles.use_denoising = denoise

    if device not in ["CPU", "CUDA", "OPTIX"]:
        raise ValueError(f"{device} is not a valid device")

    if device in ["OPTIX", "CUDA"]:
        enable_cycles_gpu(device)
        cycles.device = "GPU"
        return

    cycles.device = "CPU"


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
    def jpeg_quality(self):
        return self.file_output.file_slots["image"].format.compression

    @jpeg_quality.setter
    def jpeg_quality(self, ratio):
        self.file_output.file_slots["image"].format.compression = ratio
        # self.file_output.file_slots["coordinates"].format.compression = ratio

    @property
    def current_frame(self):
        return self.scene.frame_current

    @current_frame.setter
    def current_frame(self, index):
        self.scene.frame_current = index

    def render(self):
        renderer.render(scene="Scene")
