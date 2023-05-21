import math

import bpy


data = bpy.data
scene = data.scenes["Scene"]


textures = {
    "albedo": bpy.data.images["background_albedo"],
    "roughness": bpy.data.images["background_roughness"],
    "depth": bpy.data.images["background_depth"],
}


class Ground:
    def __init__(self):
        self.obj = data.objects["ground_plane"]

    @property
    def visible(self):
        return not self.obj.hide_render

    @visible.setter
    def visible(self, visible):
        hide = not visible
        self.obj.hide_render = hide
        self.obj.hide_viewport = hide

    @property
    def displacement_strength(self):
        return scene["ground_plane_displacement"]

    @displacement_strength.setter
    def displacement_strength(self, strength):
        scene["ground_plane_displacement"] = strength

    @property
    def texture_rotation(self):
        return math.degrees(scene["ground_plane_rotation"])

    @texture_rotation.setter
    def texture_rotation(self, angle):
        scene["ground_plane_rotation"] = math.radians(angle)

    @property
    def subdivisions(self):
        return self.obj.modifiers["Subdivision"].render_levels

    @subdivisions.setter
    def subdivisions(self, n_divisions):
        self.obj.modifiers["Subdivision"].render_levels = n_divisions
        self.obj.modifiers["Subdivision"].levels = n_divisions

    @property
    def offset(self):
        return self.obj.modifiers["UVWarp"].offset[0]

    @offset.setter
    def offset(self, offset):
        self.obj.modifiers["UVWarp"].offset[0] = offset
        self.obj.modifiers["UVWarp"].offset[1] = offset * 2

    @property
    def uv_scale(self):
        return self.obj["uv_scale"]

    @uv_scale.setter
    def uv_scale(self, scale):
        self.obj["uv_scale"] = scale

    @property
    def texture_seed(self):
        return self.obj["texture_seed"]

    @texture_seed.setter
    def texture_seed(self, seed):
        self.obj["texture_seed"] = seed

    def replace_texture(self, path, type):
        textures[type].filepath = path
