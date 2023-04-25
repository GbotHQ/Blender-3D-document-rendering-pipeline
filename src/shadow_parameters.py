import bpy


data = bpy.data
scene = data.scenes["Scene"]


class Shadows:
    def __init__(self):
        self.obj = data.objects["shadow_plane"]

    @property
    def visible(self):
        return not self.obj.hide_render

    @visible.setter
    def visible(self, visible):
        hide = not visible
        self.obj.hide_render = hide
        self.obj.hide_viewport = hide

    @property
    def seed(self):
        return self.obj["seed"]

    @seed.setter
    def seed(self, seed):
        self.obj["seed"] = seed
