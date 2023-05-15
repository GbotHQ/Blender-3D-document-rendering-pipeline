import bpy


data = bpy.data
scene = data.scenes["Scene"]
file_output = scene.node_tree.nodes["File Output"]
hdri_light = data.worlds["World"].node_tree.nodes["Background"]
hdri_backdrop = data.worlds["World"].node_tree.nodes["Background.001"]
hdri_image = bpy.data.images["hdri"]


class HDRI:
    def __init__(self):
        pass

    @property
    def image_path(self):
        return hdri_image.filepath

    @image_path.setter
    def image_path(self, path):
        hdri_image.filepath = path

    @property
    def light_strength(self):
        return hdri_light.inputs[1].default_value

    @light_strength.setter
    def light_strength(self, strength):
        hdri_light.inputs[1].default_value = strength

    @property
    def backdrop_strength(self):
        return hdri_backdrop.inputs[1].default_value

    @backdrop_strength.setter
    def backdrop_strength(self, strength):
        hdri_backdrop.inputs[1].default_value = strength

    @property
    def seed(self):
        return scene["hdri_seed"]

    @seed.setter
    def seed(self, seed):
        scene["hdri_seed"] = seed
