from pyglet.gl import *
import ctypes
from pywavefront import Wavefront
from scene import Scene
from lightSource import LightSource
from matutils import poseMatrix


class LondonScene():
    def __init__(self):
        self.scene = Scene(900, 600)

        city = Wavefront('models/city.obj')
        self.scene.add_model(city, [[0, -15, -25], [0, 0, 0, 0], [1, 1, 1]])

        dino = Wavefront('models/styracosaurus.obj')
        self.scene.add_model(dino, [[0, -17.5, -30], [270, 1, 0, 0], [0.4, 0.4, 0.4]])

    def load_scene(self):
        self.scene.run()


if __name__ == '__main__':
    scene = LondonScene()
    scene.load_scene()
