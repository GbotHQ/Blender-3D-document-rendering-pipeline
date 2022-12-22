import sys

from random import random, uniform, randint

from pathlib import Path as pth
from pathlib import PurePath as ppth

import shutil

import bpy

blend_path = pth(bpy.data.filepath).parent
project_path = (blend_path / "..").resolve()
src_path = project_path / "src"

# add src to python path so that python can do imports
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

import config

import ground_parameters
import blender_render_settings
import camera_parameters
import light_parameters
import paper_parameters

# # blender requires a module reload when not running from a command line
# import importlib
# importlib.reload(ground_parameters)
# importlib.reload(blender_render_settings)
# importlib.reload(camera_parameters)
# importlib.reload(light_parameters)
# importlib.reload(paper_parameters)


def generator(index):
    """See parameters.md for more info"""

    ground_visible = random() > 0.3

    output_path = pth(project_path, "renders")
    assets_path = ppth(project_path, "test_assets")
    texture_path_base = ppth(assets_path, "WoodenPlanks05_MR_2K")

    render_dir_base = "dataset_render_"

    output_path /= f"{render_dir_base}{str(index).zfill(8)}"

    general_conf = {}
    general_conf["resolution"] = (1024, 1024)
    general_conf["compression_ratio"] = 70
    general_conf["render_engine"] = "cycles"
    general_conf["cycles_device"] = "gpu"
    general_conf["cycles_samples"] = 8
    general_conf["cycles_denoise"] = True
    general_conf["output_path"] = str(output_path)

    ground_conf = {}
    ground_conf["visible"] = ground_visible
    ground_conf["offset"] = uniform(-10, 10)
    ground_conf["texture_rotation"] = uniform(0, 360)
    ground_conf["displacement_strength"] = uniform(0.04, 0.2)
    ground_conf["subdivisions"] = 9

    for name, type in zip(
        (
            "WoodenPlanks05_2K_BaseColor.png",
            "WoodenPlanks05_2K_Roughness.png",
            "WoodenPlanks05_2K_Height.png",
        ),
        ("albedo", "roughness", "depth"),
    ):
        ground_conf[f"texture_path_{type}"] = str(texture_path_base / name)

    paper_conf = {}
    paper_conf["text_image_path"] = str(ppth(assets_path, "lorem ipsum.psd"))
    paper_conf["size"] = (21.0, 29.7)
    paper_conf["subdivisions"] = 8
    paper_conf["crumpling_strength"] = uniform(0, 1.5)
    paper_conf["fold_messiness"] = uniform(0.03, 0.4)
    paper_conf["fold_smoothness"] = uniform(0, 1)
    paper_conf["texture_rotation"] = uniform(0, 360)
    paper_conf["offset"] = uniform(-10, 10)

    folds_conf = []
    for _ in range(2):
        fold = {}
        fold["strength"] = uniform(0.1, 0.8) if random() > 0.3 else 0.0
        fold["angle"] = uniform(-15, 15)
        folds_conf.append(fold)

    folds_conf[1]["angle"] += 90

    camera_conf = {}
    camera_conf["focal_length"] = randint(24, 135)
    camera_conf["relative_camera_distance"] = 1.3
    camera_conf["depth_of_field"] = True
    camera_conf["fstop"] = uniform(1.0, 4.0)
    camera_conf["orbit"] = (uniform(0, 25), uniform(0, 360))
    camera_conf["look_at_2d"] = (0, 0)

    hdri_conf = {}
    hdri_conf["hdri_image_path"] = str(assets_path / "canary_wharf_2k.exr")
    hdri_conf["hdri_light_strength"] = uniform(0.02, 0.2)
    hdri_conf["hdri_backdrop_strength"] = 1.0
    hdri_conf["hdri_image_rotation"] = uniform(0, 360)

    lights_conf = []
    for _ in range(2):
        light = {}
        light["visible"] = True

        light["distance"] = uniform(2, 4)
        light["orbit"] = uniform(0, 45), uniform(0, 360)
        light["look_at_2d"] = uniform(-0.4, 0.4), uniform(-0.4, 0.4)

        light["power"] = uniform(500, 900)
        light["shadow_softness_radius"] = uniform(0.1, 0.8)
        light["light_cone_angle"] = uniform(30, 90)

        color = [uniform(0.7, 1) for _ in range(3)]
        color_total = sum(color)
        color = [c / color_total for c in color]
        light["color"] = color
        lights_conf.append(light)

    lights_conf[1]["visible"] = random() > 0.7
    if lights_conf[1]["visible"]:
        # both lights are visible, need to reduce light power
        for light in lights_conf:
            light["power"] /= 2

    conf = {
        "general": general_conf,
        "ground": ground_conf,
        "paper": paper_conf,
        "folds": folds_conf,
        "camera": camera_conf,
        "hdri": hdri_conf,
        "lights": lights_conf,
    }

    return conf


def generate_and_render(conf):
    # ground parameters
    ground = ground_parameters.Ground()
    ground.visible = conf["ground"]["visible"]

    if conf["ground"]["visible"]:
        ground.offset = conf["ground"]["offset"]
        ground.texture_rotation = conf["ground"]["texture_rotation"]
        ground.displacement_strength = conf["ground"]["displacement_strength"]
        ground.subdivisions = conf["ground"]["subdivisions"]

    # load textures
    for type in ("albedo", "roughness", "depth"):
        ground.replace_texture(conf["ground"][f"texture_path_{type}"], type)

    # paper parameters
    paper = paper_parameters.Paper()
    paper.text_image_path = conf["paper"]["text_image_path"]
    paper.paper_size_cm(*conf["paper"]["size"])
    paper.subdivisions = conf["paper"]["subdivisions"]
    paper.crumpling_strength = conf["paper"]["crumpling_strength"]
    paper.fold_messiness = conf["paper"]["fold_messiness"]
    paper.fold_smoothness = conf["paper"]["fold_smoothness"]
    paper.texture_rotation = conf["paper"]["texture_rotation"]
    paper.offset = conf["paper"]["offset"]

    for fold, fold_conf in zip(paper.folds, conf["folds"]):
        fold.strength = fold_conf["strength"]
        fold.angle = fold_conf["angle"]

    # camera parameters
    camera = camera_parameters.Camera()

    camera.focal_length = conf["camera"]["focal_length"]
    camera.relative_camera_distance = conf["camera"]["relative_camera_distance"]
    camera.depth_of_field = conf["camera"]["depth_of_field"]
    camera.fstop = conf["camera"]["fstop"]
    camera.orbit(*conf["camera"]["orbit"])
    camera.look_at_2d(*conf["camera"]["look_at_2d"])

    # light parameters
    lights = [light_parameters.Light(f"light_{i}") for i in range(2)]
    for light, light_conf in zip(lights, conf["lights"]):
        light.visible = light_conf["visible"]

        if not light_conf["visible"]:
            continue

        light.distance = light_conf["distance"]
        light.orbit(*light_conf["orbit"])
        light.look_at_2d(*light_conf["look_at_2d"])

        light.power = light_conf["power"]
        light.shadow_softness_radius = light_conf["shadow_softness_radius"]
        light.light_cone_angle = light_conf["light_cone_angle"]

        light.color = light_conf["color"]

    # render settings
    render_settings = blender_render_settings.RenderSettings()

    render_settings.hdri_image_path = conf["hdri"]["hdri_image_path"]
    render_settings.hdri_light_strength = conf["hdri"]["hdri_light_strength"]
    render_settings.hdri_backdrop_strength = conf["hdri"]["hdri_backdrop_strength"]
    render_settings.hdri_image_rotation = conf["hdri"]["hdri_image_rotation"]

    # jump to the first frame
    render_settings.current_frame = 1

    render_settings.output_path = conf["general"]["output_path"]
    render_settings.compression_ratio = conf["general"]["compression_ratio"]
    render_settings.render_resolution = conf["general"]["resolution"]

    # change render engine to cycles, change to using specified device and change sampling settings
    render_settings.change_render_engine(
        conf["general"]["render_engine"],
        conf["general"]["cycles_device"],
        conf["general"]["cycles_samples"],
        conf["general"]["cycles_denoise"],
    )

    # render
    render_settings.render()


class InvalidKeyInConfig(KeyError):
    def __init__(self, key):
        super().__init__(f"Invalid key ['{key}'] in config")


def check_config_validity(samples):
    """check config for invalid keys"""

    def check_allowed_keys(keys, allowed_keys):
        for key in keys:
            if key not in allowed_keys:
                raise InvalidKeyInConfig(key)

    sample_conf = generator(0)
    for conf in samples:
        check_allowed_keys(conf.keys(), sample_conf.keys())
        # check subkeys
        for k in conf:
            if isinstance(sample_conf[k], dict):
                check_allowed_keys(conf[k].keys(), sample_conf[k].keys())
            else:
                for i in range(len(sample_conf[k])):
                    check_allowed_keys(conf[k][i].keys(), sample_conf[k][i].keys())


if __name__ == "__main__":
    samples = config.read()
    print(f"Generating {len(samples)} samples...")

    check_config_validity(samples)

    for i, conf in enumerate(samples):
        default_conf = generator(i)

        # merge configs
        default_conf.update(conf)
        conf = default_conf

        out_path = pth(conf["general"]["output_path"])
        if out_path.is_dir():
            shutil.rmtree(out_path)

        generate_and_render(conf)
