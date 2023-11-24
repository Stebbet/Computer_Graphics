import pygame

# import the scene class
from cubeMap import FlattenCubeMap
from scene import Scene
from lightSource import LightSource

from blender import load_obj_file

from BaseModel import DrawModelFromMesh

from shaders import *

from math import sin, cos, radians

from ShadowMapping import *

from sphereModel import Sphere

from skyBox import *

from environmentMapping import *


class ExeterScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.dt = 0.
        self.light = LightSource(self, position=[-3., 9, 3.], Ia=[0.6,0.6,0.6], Id=[.6,139/500,147/500], Is=[.5,139/500,147/500])

        self.shaders = 'phong'

        # for shadow map rendering
        self.shadows = ShadowMap(light=self.light)
        self.draw_shadows = True
        self.show_shadow_map = ShowTexture(self, self.shadows)

        # draw a skybox for the horizon
        self.skybox = SkyBox(scene=self)

        self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=0.2),
                                            mesh=Sphere(material=Material(Ka=self.light.Id)), shader=FlatShader())


        self.environment = EnvironmentMappingTexture(width=200, height=200)

        # self.sphere = DrawModelFromMesh(scene=self, M=poseMatrix(), mesh=Sphere(), shader=EnvironmentShader(map=self.environment))
        # self.sphere = DrawModelFromMesh(scene=self, M=poseMatrix(), mesh=Sphere(), shader=FlatShader())


        # The ground and river
        self.groundlevel = -2
        floor = load_obj_file('models/scene.obj')
        self.floor = [DrawModelFromMesh(scene=self,
                                       M=poseMatrix(position=[0, self.groundlevel, 0], orientation=[0, 0, 0],
                                                    scale=[.5,.5,.5]),
                                       mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='floor') for mesh in floor]

        # Define the Pterodactyls
        self.pterodactyl_scale = 4
        pterodactyl = load_obj_file('models/pterodactyl.obj')
        self.pterodactyl = DrawModelFromMesh(scene=self,
                                        M=poseMatrix(), mesh=pterodactyl[0],
                                        shader=ShadowMappingShader(shadow_map=self.shadows), name='pterodactyl')

        helicopter = load_obj_file('models/helicopter.obj')
        self.helicopter = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(), mesh=helicopter[0],
                                             shader=ShadowMappingShader(shadow_map=self.shadows), name='helicopter')

        # Office
        office = load_obj_file('models/office.obj')
        self.office = [DrawModelFromMesh(scene=self,
                                        M=poseMatrix(position=[-0.3,-0.9,6.5], orientation=[0,radians(90),0], scale=8), mesh=mesh,
                                        shader=ShadowMappingShader(shadow_map=self.shadows), name='office') for mesh in office]


        self.office2 = [DrawModelFromMesh(scene=self,
                                        M=poseMatrix(position=[-4, -0.9, -8], orientation=[0,radians(90),0], scale=8), mesh=mesh,
                                        shader=ShadowMappingShader(shadow_map=self.shadows), name='office') for mesh in office]

        # Bridge Object
        bridge = load_obj_file('models/bridge.obj')
        self.bridge = [DrawModelFromMesh(scene=self,
                                          M=poseMatrix(position=[-1, -1.4, -5], orientation=[0, 0, 0],
                                                       scale=9), mesh=mesh,
                                          shader=ShadowMappingShader(shadow_map=self.shadows), name='office') for mesh in bridge]

        # Large buildings
        large_buildings = load_obj_file('models/large_buildings.obj')
        self.large_buildings = [DrawModelFromMesh(scene=self,
                                                  M=poseMatrix(position=[-6, self.groundlevel - .15, 7], orientation=[0, radians(90), 0], scale=16),
                                                  mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='large_buildings') for mesh in large_buildings]

        # Main skyscraper
        skyscraper = load_obj_file('models/building1.obj')
        self.skyscraper = [DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[1, self.groundlevel - 1, 0], orientation=[0, 0, 0], scale=0.007),
                                             mesh=mesh, shader=ShadowMappingShader(self.shadows), name='skyscraper') for mesh in skyscraper]

        # London Wheel
        wheel = load_obj_file('models/wheel2.obj')
        self.wheel = [DrawModelFromMesh(scene=self,
                                        M=poseMatrix(position=[-4, self.groundlevel, 0], orientation=[0, 0, 0], scale=0.003),
                                        mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                        name='skyscraper') for mesh in wheel]

        # environment box for reflections
        # self.envbox = EnvironmentBox(scene=self)

        # this object allows to visualise the flattened cube

        # self.flattened_cube = FlattenCubeMap(scene=self, cube=CubeMap(name='skybox/ame_ash'))
        self.flattened_cube = FlattenCubeMap(scene=self, cube=self.environment)


    def draw_shadow_map(self):
        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for model in self.skyscraper:
            model.draw()
        for model in self.bridge:
            model.draw()
        self.pterodactyl.draw()
        self.helicopter.draw()

    def draw_reflections(self):
        self.skybox.draw()

    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''
        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # when using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        # first, we draw the skybox
        self.skybox.draw()

        # Draw the animations
        self.animations()

        # render the shadows
        if self.draw_shadows:
            self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:
            # glEnable(GL_BLEND)
            # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            # self.envbox.draw()
            # self.environment.update(self)
            # self.envbox.draw()

            # self.environment.update(self)
            for model in self.floor:
                model.draw()
            for model in self.skyscraper:
                model.draw()
            for model in self.large_buildings:
                model.draw()
            for model in self.wheel:
                model.draw()
            for model in self.office:
                model.draw()
            for model in self.office2:
                model.draw()
            for model in self.bridge:
                model.draw()

            self.pterodactyl.draw()
            self.helicopter.draw()

            self.flattened_cube.draw()
            self.show_shadow_map.draw()


        # then we loop over all models in the list and draw them


        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        '''
        Process additional keyboard events for this demo.
        '''
        Scene.keyboard(self, event)

        if event.key == pygame.K_1:
            print('--> using shadows shading')
            if self.draw_shadows:
                self.draw_shadows = False
            else:
                self.draw_shadows = True

    def animations(self):
        self.dt += 0.01
        xpos = 2 * sin(self.dt)
        zpos = 2 * cos(self.dt)

        self.pterodactyl.M = poseMatrix(position=[xpos, 0.3 * sin(self.dt) + 3, zpos],
                                   orientation=[0.3 * sin(self.dt), radians(90) + self.dt, radians(20)], scale=self.pterodactyl_scale)

        self.helicopter.M = poseMatrix(position=[-xpos, 0.3 * sin(self.dt) + 4, -zpos],
                                        orientation=[-0.3 * sin(self.dt), radians(-90) + self.dt, radians(20)],
                                        scale=4)

if __name__ == '__main__':
    # initialises the scene object
    # scene = Scene(shaders='gouraud')
    scene = ExeterScene()

    # starts drawing the scene
    scene.run()

#TODO:
#  - Find a model for the river - DONE
#  - Design and complete the scene
#  - Rampaging Trex into Trex animation maybe
#  - Fire breathing Pterodactyl
#  - Comment everything better
