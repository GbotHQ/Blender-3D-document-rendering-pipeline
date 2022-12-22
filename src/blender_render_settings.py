import math

import bpy


def warn_about_device_fallback(device, device_to_fallback_to):
    print(
        f"Failed to enable {device}, falling back to {device_to_fallback_to}"
        f""" (when rendering from a command line, use [--engine CYCLES] with [--cycles-device {device}] and ignore this message)"""
    )


data = bpy.data
scene = data.scenes["Scene"]
scene_renderer = scene.render
file_output = scene.node_tree.nodes["File Output"]
renderer = bpy.ops.render
hdri_light = data.worlds["World"].node_tree.nodes["Background"]
hdri_backdrop = data.worlds["World"].node_tree.nodes["Background.001"]
hdri_image = bpy.data.images["hdri"]
preferences = bpy.context.preferences
cycles_preferences = preferences.addons["cycles"].preferences
cycles = scene.cycles


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


def enable_gpu():
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


def change_render_engine_cycles(cycles_device, cycles_samples, cycles_denoise):
    cycles.preview_samples = cycles_samples
    cycles.use_denoising = cycles_denoise

    if cycles_device == "gpu":
        if not enable_gpu():
            cycles_device = "cpu"

    if cycles_device == "cpu":
        cycles.device = "CPU"
    elif cycles_device != "gpu":
        raise Exception(f"{cycles_device} is not a valid device")


class RenderSettings:
    def __init__(self):
        pass

    @property
    def render_resolution(self):
        return scene_renderer.resolution_x, scene_renderer.resolution_y

    @render_resolution.setter
    def render_resolution(self, resolution):
        scene_renderer.resolution_x = resolution[0]
        scene_renderer.resolution_y = resolution[1]

    def change_render_engine(
        self,
        render_engine,
        cycles_device="gpu",
        cycles_samples=8,
        cycles_denoise=True,
    ):
        if render_engine == "cycles":
            change_render_engine_cycles(
                cycles_device, cycles_samples, cycles_denoise
            )
            scene_renderer.engine = "CYCLES"
        elif render_engine == "eevee":
            scene_renderer.engine = "BLENDER_EEVEE"
        elif render_engine == "workbench":
            scene_renderer.engine = "BLENDER_WORKBENCH"
        else:
            raise Exception(f"{render_engine} is not a valid render engine")

    @property
    def output_path(self):
        return file_output.base_path

    @output_path.setter
    def output_path(self, path):
        file_output.base_path = path

    @property
    def compression_ratio(self):
        return file_output.file_slots['image'].format.compression

    @compression_ratio.setter
    def compression_ratio(self, ratio):
        file_output.file_slots['image'].format.compression = ratio
        file_output.file_slots['coordinates'].format.compression = ratio

    @property
    def current_frame(self):
        return scene.frame_current

    @current_frame.setter
    def current_frame(self, index):
        scene.frame_current = index

    @property
    def hdri_image_path(self):
        return hdri_image.filepath

    @hdri_image_path.setter
    def hdri_image_path(self, path):
        hdri_image.filepath = path

    @property
    def hdri_light_strength(self):
        return hdri_light.inputs[1].default_value

    @hdri_light_strength.setter
    def hdri_light_strength(self, strength):
        hdri_light.inputs[1].default_value = strength

    @property
    def hdri_backdrop_strength(self):
        return hdri_backdrop.inputs[1].default_value

    @hdri_backdrop_strength.setter
    def hdri_backdrop_strength(self, strength):
        hdri_backdrop.inputs[1].default_value = strength

    @property
    def hdri_image_rotation(self):
        return math.degrees(scene["hdri_rotation"])

    @hdri_image_rotation.setter
    def hdri_image_rotation(self, angle):
        scene["hdri_rotation"] = math.radians(angle)

    def render(self):
        renderer.render(layer="View Layer", scene="Scene")
