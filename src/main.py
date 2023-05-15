from typing import Union
import sys

from pathlib import Path as pth
from pathlib import PurePath as ppth

import shutil

import bpy

blend_dir = pth(bpy.data.filepath).parent
project_dir = (blend_dir / "..").resolve()
src_dir = project_dir / "src"
config_dir = project_dir / "config"
output_dir = project_dir / "renders"

# add src to python path so that python can do imports
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

import config

import ground_parameters
import blender_render_settings
import hdri_parameters
import camera_parameters
import light_parameters
import paper_parameters
import shadow_parameters

# # blender requires a module reload when not running from a command line
# import importlib
# importlib.reload(ground_parameters)
# importlib.reload(blender_render_settings)
# importlib.reload(camera_parameters)
# importlib.reload(light_parameters)
# importlib.reload(paper_parameters)


def generate_and_render(conf: config.Config, output_path: Union[str, pth]):
    # ground parameters
    ground = ground_parameters.Ground()
    ground.visible = conf.ground.visible

    if conf.ground.visible:
        ground.offset = conf.ground.offset
        ground.texture_rotation = conf.ground.texture_rotation
        ground.displacement_strength = conf.ground.displacement_strength
        ground.subdivisions = conf.ground.subdivisions

    # load textures
    ground.replace_texture(conf.ground.albedo_tex, "albedo")
    ground.replace_texture(conf.ground.roughness_tex, "roughness")
    ground.replace_texture(conf.ground.displacement_tex, "depth")

    shadows = shadow_parameters.Shadows()
    shadows.visible = conf.shadows.visible
    shadows.seed = conf.shadows.seed

    # paper parameters
    paper = paper_parameters.Paper()
    paper.text_image_path = conf.paper.document_image_path
    paper.paper_size_cm(*conf.paper.size)
    paper.subdivisions = conf.paper.subdivisions
    paper.crumpling_strength = conf.paper.crumpling_strength
    paper.fold_messiness = conf.paper.fold_messiness
    paper.fold_smoothness = conf.paper.fold_smoothness
    paper.texture_rotation = conf.paper.texture_rotation
    paper.offset = conf.paper.offset

    for i, (fold, fold_conf) in enumerate(zip(paper.folds, conf.folds)):
        fold.strength = fold_conf.strength
        fold.angle = fold_conf.angle + i * 90

    # camera parameters
    camera = camera_parameters.Camera()

    camera.focal_length = conf.camera.focal_length
    camera.relative_camera_distance = conf.camera.relative_camera_distance
    camera.depth_of_field = conf.camera.depth_of_field
    camera.fstop = conf.camera.fstop
    camera.orbit(*conf.camera.orbit)
    camera.look_at_2d(*conf.camera.look_at_2d)

    # light parameters
    lights = [light_parameters.Light(f"light_{i}") for i in range(2)]
    for light, light_conf in zip(lights, conf.lights):
        light.visible = light_conf.visible

        if not light_conf.visible:
            continue

        light.distance = light_conf.distance
        light.orbit(*light_conf.orbit)
        light.look_at_2d(*light_conf.look_at_2d)

        light.power = light_conf.power
        light.shadow_softness_radius = light_conf.shadow_softness_radius
        light.light_cone_angle = light_conf.light_cone_angle

        light.color = light_conf.color

    # hdri parameters
    hdri = hdri_parameters.HDRI()

    hdri.image_path = conf.hdri.texture_path
    hdri.light_strength = conf.hdri.light_strength
    hdri.backdrop_strength = conf.hdri.backdrop_strength
    hdri.seed = conf.hdri.seed

    # render settings
    render_settings = blender_render_settings.RenderSettings()

    # jump to the first frame
    render_settings.current_frame = 1

    render_settings.output_path = output_path
    render_settings.compression_ratio = conf.render.compression_ratio
    render_settings.render_resolution = conf.render.resolution

    # change render engine to cycles, change to using specified device and change sampling settings
    render_settings.change_render_engine(
        conf.render.render_engine,
        conf.render.cycles_device,
        conf.render.cycles_samples,
        conf.render.cycles_denoise,
    )

    # render
    render_settings.render()


if __name__ == "__main__":
    samples = [k for k in config_dir.iterdir() if k.is_file() and k.suffix == ".json"]

    for i, k in enumerate(samples):
        print(f"Generating sample {i+1} of {len(samples)}...")

        sample = config.read_config(k)

        output_path = output_dir / k.stem

        if output_path.is_dir():
            shutil.rmtree(output_path)

        generate_and_render(sample, output_path)
