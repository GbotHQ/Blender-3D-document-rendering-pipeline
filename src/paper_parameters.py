import math

import bpy


data = bpy.data
scene = data.scenes["Scene"]

text_texture = bpy.data.images["text"]


class Fold:
    def __init__(self, obj, index):
        self.obj = obj
        self.index = index
        self.__modifier = self.obj.modifiers["fold_and_crumble"]
        self.__angle_index = f"Input_{self.index + 2}"
        self.__strength_index = f"Input_{self.index + 7}"

    @property
    def angle(self):
        return math.degrees(self.__modifier[self.__angle_index])

    @angle.setter
    def angle(self, angle):
        self.__modifier[self.__angle_index] = math.radians(angle)

    @property
    def strength(self):
        return self.__modifier[self.__strength_index]

    @strength.setter
    def strength(self, strength):
        self.__modifier[self.__strength_index] = float(strength)


class Paper:
    def __init__(self):
        self.obj = data.objects["paper"]
        self.__fold_modifier = self.obj.modifiers["fold_and_crumble"]
        self.folds = [Fold(self.obj, i) for i in range(2)]

    def paper_size_cm(self, width, height):
        scene["paper_width_cm"] = width
        scene["paper_height_cm"] = height

    @property
    def subdivisions(self):
        return self.obj.modifiers["Subdivision"].render_levels

    @subdivisions.setter
    def subdivisions(self, n_divisions):
        self.obj.modifiers["Subdivision"].render_levels = n_divisions
        self.obj.modifiers["Subdivision"].levels = n_divisions

    @property
    def crumpling_strength(self):
        return self.__fold_modifier["Input_6"]

    @crumpling_strength.setter
    def crumpling_strength(self, strength):
        self.__fold_modifier["Input_6"] = strength

    @property
    def fold_messiness(self):
        return self.__fold_modifier["Input_9"]

    @fold_messiness.setter
    def fold_messiness(self, messiness):
        self.__fold_modifier["Input_9"] = messiness

    @property
    def fold_smoothness(self):
        return self.__fold_modifier["Input_10"]

    @fold_smoothness.setter
    def fold_smoothness(self, smoothness):
        self.__fold_modifier["Input_10"] = smoothness

    @property
    def texture_rotation(self):
        return math.degrees(self.obj.modifiers["UVWarp"].rotation)

    @texture_rotation.setter
    def texture_rotation(self, angle):
        self.obj.modifiers["UVWarp"].rotation = math.radians(angle)

    @property
    def offset(self):
        return self.obj.modifiers["UVWarp"].offset[0]

    @offset.setter
    def offset(self, offset):
        self.obj.modifiers["UVWarp"].offset[0] = offset
        self.obj.modifiers["UVWarp"].offset[1] = offset * 2

    @property
    def text_image_path(self):
        return text_texture.filepath

    @text_image_path.setter
    def text_image_path(self, path):
        text_texture.filepath = path
