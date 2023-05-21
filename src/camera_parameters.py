import math

import bpy


data = bpy.data
scene = data.scenes["Scene"]


class Camera:
    def __init__(self):
        self.obj = data.cameras["Camera"]
        self.look_at_obj = data.objects["camera_look_at"]
        self._dof_prop = self.obj.dof

    # @property
    # def use_depth_of_field(self):
    #     return self._dof_prop.use_dof

    # @use_depth_of_field.setter
    # def use_depth_of_field(self, enable):
    #     self._dof_prop.use_dof = enable

    @property
    def focal_length(self):
        return scene["focal_length"]

    @focal_length.setter
    def focal_length(self, focal_length):
        scene["focal_length"] = focal_length
        data.scenes["Scene"]["focal_length"] = focal_length

    # @property
    # def fstop(self):
    #     return self._dof_prop.aperture_fstop

    # @fstop.setter
    # def fstop(self, fstop):
    #     self._dof_prop.aperture_fstop = fstop

    @property
    def relative_camera_distance(self):
        return scene["relative_camera_distance"]

    @relative_camera_distance.setter
    def relative_camera_distance(self, distance):
        scene["relative_camera_distance"] = distance

    def orbit(self, attitude, azimuth):
        self.look_at_obj.rotation_euler[0] = math.radians(attitude)
        self.look_at_obj.rotation_euler[2] = math.radians(azimuth)

    def look_at_2d(self, x, y):
        self.look_at_obj.location[0] = x
        self.look_at_obj.location[1] = y
