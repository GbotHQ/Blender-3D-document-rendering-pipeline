import random as rng
from random import random, uniform, randint
from typing import Union, Tuple, Optional
import json

from pathlib import Path as pth
from typing import Any


def set_seed(seed: int):
    rng.seed(seed)


class Render:
    def __init__(
        self,
        project_root: Union[str, pth],
        resolution: Optional[Tuple[int, int]] = None,
        compression_ratio: Optional[int] = None,
        render_engine: Optional[str] = None,
        cycles_device: Optional[str] = None,
        cycles_samples: Optional[int] = None,
        cycles_denoise: Optional[bool] = None,
    ) -> None:
        self.resolution = resolution or (1024, 1024)
        self.compression_ratio = compression_ratio or 70
        self.render_engine = render_engine or "cycles"
        self.cycles_device = cycles_device or "CUDA"
        self.cycles_samples = cycles_samples or 2
        self.cycles_denoise = cycles_denoise or True


class Ground:
    def __init__(
        self,
        project_root: Union[str, pth],
        visible: Optional[bool] = None,
        offset: Optional[float] = None,
        texture_rotation: Optional[float] = None,
        displacement_strength: Optional[float] = None,
        subdivisions: Optional[int] = None,
        texture_path_base: Optional[Union[str, pth]] = None,
        albedo_tex: Optional[Union[str, pth]] = None,
        roughness_tex: Optional[Union[str, pth]] = None,
        displacement_tex: Optional[Union[str, pth]] = None,
        uv_scale: Optional[float] = None,
        texture_seed: Optional[int] = None,
    ) -> None:
        self.visible = visible or (random() > 0.3)
        self.offset = offset or uniform(-10, 10)
        self.texture_rotation = texture_rotation or uniform(0, 360)
        self.displacement_strength = displacement_strength or uniform(0.04, 0.2)
        self.subdivisions = subdivisions or 9
        self.uv_scale = uv_scale or uniform(1.2, 3)
        self.texture_seed = texture_seed or randint(0, 10000)

        self.texture_path_base = str(
            texture_path_base
            or pth(project_root, "test_assets", "WoodenPlanks05_MR_2K")
        )
        self.albedo_tex = str(
            albedo_tex or pth(self.texture_path_base, "WoodenPlanks05_2K_BaseColor.png")
        )
        self.roughness_tex = str(
            roughness_tex
            or pth(self.texture_path_base, "WoodenPlanks05_2K_Roughness.png")
        )
        self.displacement_tex = str(
            displacement_tex
            or pth(self.texture_path_base, "WoodenPlanks05_2K_Height.png")
        )


class Shadows:
    def __init__(
        self,
        visible: Optional[bool] = None,
        seed: Optional[int] = None,
    ) -> None:
        self.visible = visible or (random() > 0.4)
        self.seed = seed or randint(0, 1000)


class Paper:
    def __init__(
        self,
        project_root: Union[str, pth],
        document_image_path: Optional[Union[str, pth]] = None,
        size: Optional[Tuple[float, float]] = None,
        subdivisions: Optional[int] = None,
        crumpling_strength: Optional[float] = None,
        fold_messiness: Optional[float] = None,
        fold_smoothness: Optional[float] = None,
        texture_rotation: Optional[float] = None,
        offset: Optional[float] = None,
    ) -> None:
        self.document_image_path = str(
            document_image_path or pth(project_root, "test_assets", "lorem ipsum.psd")
        )
        self.size = size or (21.0, 29.7)
        self.subdivisions = subdivisions or 8
        self.crumpling_strength = crumpling_strength or uniform(0, 1.5)
        self.fold_messiness = fold_messiness or uniform(0.03, 0.4)
        self.fold_smoothness = fold_smoothness or uniform(0, 1)
        self.texture_rotation = texture_rotation or uniform(0, 360)
        self.offset = offset or uniform(-10, 10)


class Fold:
    def __init__(
        self,
        strength: Optional[float] = None,
        angle: Optional[float] = None,
    ) -> None:
        self.strength = strength or (uniform(0.1, 0.8) if random() > 0.3 else 0.0)
        self.angle = angle or uniform(-15, 15)


class Camera:
    def __init__(
        self,
        focal_length: Optional[int] = None,
        relative_camera_distance: Optional[float] = None,
        orbit: Optional[Tuple[float, float]] = None,
        look_at_2d: Optional[Tuple[int, int]] = None,
    ) -> None:
        self.focal_length = focal_length or randint(24, 135)
        self.relative_camera_distance = relative_camera_distance or 1.3
        self.orbit = orbit or (uniform(0, 25), uniform(0, 360))
        self.look_at_2d = look_at_2d or (0, 0)


class HDRI:
    def __init__(
        self,
        project_root: Union[str, pth],
        texture_path: Optional[Union[str, pth]] = None,
        light_strength: Optional[float] = None,
        backdrop_strength: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> None:
        self.texture_path = str(
            texture_path or pth(project_root, "test_assets", "canary_wharf_2k.exr")
        )
        self.light_strength = light_strength or uniform(0.02, 0.3)
        self.backdrop_strength = backdrop_strength or 1.0
        self.seed = seed or randint(0, 10000)


class Light:
    def __init__(
        self,
        visible: Optional[bool] = None,
        color: Optional[Tuple[float, float, float]] = None,
        distance: Optional[float] = None,
        orbit: Optional[Tuple[float, float]] = None,
        look_at_2d: Optional[Tuple[int, int]] = None,
        power: Optional[float] = None,
        shadow_softness_radius: Optional[float] = None,
        light_cone_angle: Optional[float] = None,
    ) -> None:
        self.visible = visible or True

        self.distance = distance or uniform(2, 4)
        self.orbit = orbit or (uniform(0, 45), uniform(0, 360))
        self.look_at_2d = look_at_2d or (
            uniform(-0.4, 0.4),
            uniform(-0.4, 0.4),
        )

        self.power = power or uniform(500, 900)
        self.shadow_softness_radius = shadow_softness_radius or uniform(0.03, 0.8)
        self.light_cone_angle = light_cone_angle or uniform(30, 90)

        self.color = color
        if not self.color:
            c = [uniform(0.7, 1) for _ in range(3)]
            color_total = sum(c)
            self.color = tuple(k / color_total for k in c)


class Config:
    def __init__(
        self,
        cycles_device: str = "CUDA",
        project_root: Optional[Union[str, pth]] = None,
        render: Optional[Render] = None,
        ground: Optional[Ground] = None,
        shadows: Optional[Shadows] = None,
        paper: Optional[Paper] = None,
        folds: Optional[Tuple[Fold, Fold]] = None,
        camera: Optional[Camera] = None,
        hdri: Optional[HDRI] = None,
        lights: Optional[Tuple[Light, Light]] = None,
    ) -> None:
        self.project_root = str(pth(project_root or pth.cwd()).resolve())

        self.render = render or Render(self.project_root, cycles_device=cycles_device)
        self.ground = ground or Ground(self.project_root)
        self.shadows = shadows or Shadows()
        self.paper = paper or Paper(self.project_root)
        self.folds = folds or tuple(Fold() for _ in range(2))
        self.camera = camera or Camera()
        self.hdri = hdri or HDRI(self.project_root)
        if lights:
            self.lights = lights
        else:
            self.lights = tuple(Light() for _ in range(2))
            self.lights[1].visible = random() > 0.7
            if self.lights[1].visible:
                # both lights are visible, need to reduce light power
                self.lights[0].power /= 2

    def to_dict(self) -> dict:
        def to_dict_recursive(obj) -> Any:
            if not hasattr(obj, "__dict__"):
                return obj

            dictionary = obj.__dict__.copy()

            for key in dictionary:
                for k in (tuple, list):
                    if isinstance(dictionary[key], k):
                        dictionary[key] = k(
                            to_dict_recursive(k) for k in dictionary[key]
                        )
                        break
                else:
                    dictionary[key] = to_dict_recursive(dictionary[key])

            return dictionary

        return to_dict_recursive(self)

    def from_dict(self, dictionary) -> "Config":
        def from_dict_recursive(obj, dictionary) -> Any:
            if not hasattr(obj, "__dict__"):
                return dictionary

            obj_dict = obj.__dict__
            for key in obj_dict:
                for k in (tuple, list):
                    if isinstance(obj_dict[key], k):
                        obj_dict[key] = k(
                            from_dict_recursive(k, l)
                            for k, l in zip(obj_dict[key], dictionary[key])
                        )
                        break
                else:
                    obj_dict[key] = from_dict_recursive(obj_dict[key], dictionary[key])

            obj.__dict__ = obj_dict
            return obj

        return from_dict_recursive(self, dictionary)


def write_config(path: Union[str, pth], config: Config):
    with open(path, "w") as json_file:
        json.dump(config.to_dict(), json_file, indent=2)


def read_config(path: Union[str, pth]) -> Config:
    with open(path) as json_file:
        return Config().from_dict(json.load(json_file))
