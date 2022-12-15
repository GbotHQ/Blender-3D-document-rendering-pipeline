import math

import bpy


data = bpy.data
scene = data.scenes["Scene"]


class Light:
    def __init__(self, obj_name):
        self.obj = data.objects[obj_name]
        self.__data = self.obj.data
        self.look_at_obj = self.obj.constraints["Child Of"].target

    @property
    def visible(self):
        return not self.obj.hide_render

    @visible.setter
    def visible(self, visible):
        hide = not visible
        self.obj.hide_render = hide
        self.obj.hide_viewport = hide

    @property
    def power(self):
        return self.__data.energy

    @power.setter
    def power(self, power):
        self.__data.energy = power

    @property
    def color(self):
        return self.__data.color

    @color.setter
    def color(self, color):
        self.__data.color = color

    @property
    def distance(self):
        return scene["distance"]

    @distance.setter
    def distance(self, distance):
        self.obj.location[2] = distance

    def orbit(self, attitude, azimuth):
        self.look_at_obj.rotation_euler[0] = math.radians(attitude)
        self.look_at_obj.rotation_euler[2] = math.radians(azimuth)

    def look_at_2d(self, x, y):
        self.look_at_obj.location[0] = x
        self.look_at_obj.location[1] = y

    @property
    def shadow_softness_radius(self):
        return self.__data.shadow_soft_size

    @shadow_softness_radius.setter
    def shadow_softness_radius(self, radius):
        self.__data.shadow_soft_size = radius

    @property
    def light_cone_angle(self):
        return math.degrees(self.__data.spot_size)

    @light_cone_angle.setter
    def light_cone_angle(self, angle):
        self.__data.spot_size = math.radians(angle)
