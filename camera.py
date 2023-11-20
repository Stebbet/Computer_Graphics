# import a bunch of useful matrix functions (for translation, scaling etc)
from matutils import *
from pyglet.gl import *
import numpy as np
import ctypes
from math import cos, sin, radians
from sklearn.preprocessing import normalize

class Camera:
    '''
    Base class for handling the camera.
    '''


    def __init__(self):
        self.pos = [0., 0., 0.]
        self.front = [0., 0., -1.0]
        self.up = [0., 1., 0.]
        self.world_up = [0., 1., 0.]
        self.yaw = -90.
        self.pitch = 0.1
        self.zoom = 45.
        self.update_vectors()

    def mouse_turn(self, dx, dy):
        self.yaw -= dx * 0.2
        self.pitch -= dy * 0.2
        self.update_vectors()


    def mouse_movement(self, dx, dy):
        self.pos[0] -= dx * 0.06
        self.pos[1] -= dy * 0.06

    def scroll(self, y):
        # Mouse scroll events
        self.zoom -= y
        if self.zoom < 1.0:
            self.zoom = 1.0

        if self.zoom > 45.0:
            self.zoom = 45.0

    def update_vectors(self):
        f = [0, 0, 0]
        f[0] = cos(radians(self.yaw)) * cos(radians(self.pitch))
        f[1] = sin(radians(self.pitch))
        f[2] = sin(radians(self.yaw)) * cos(radians(self.pitch))

        v = np.array([f[0], f[1], f[2]])
        self.front = normalize(v[:, np.newaxis], axis=0).ravel()
        w = np.array([0, 1, 0])

        r = np.cross(self.front, w)
        Right = normalize(r[:, np.newaxis], axis=0).ravel()

        u = np.cross(Right, self.front)
        self.up = normalize(u[:, np.newaxis], axis=0).ravel()



    def getViewMatrix(self):
        return gluLookAt(self.pos[0], self.pos[1], self.pos[2],
                         self.pos[0] + self.front[0], self.pos[1] + self.front[1], self.pos[2] + self.front[2],
                         self.up[0], self.up[1], self.up[2])
