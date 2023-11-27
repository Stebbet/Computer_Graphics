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
        self.fire_timer = 0
        self.fire_on = True

        self.light = LightSource(self, position=[-20, 50, 5], Ia=[0.6,0.6,0.6], Id=[.6,139/500,147/500], Is=[.5,139/500,147/500])

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
        self.river = DrawModelFromMesh(scene=self,
                                       M=poseMatrix(position=[0, self.groundlevel, 0], orientation=[0,0,0], scale=.5),
                                       mesh=floor[0], shader=ShadowMappingShader(self.shadows), name='river')

        self.floor_r = DrawModelFromMesh(scene=self,
                                       M=poseMatrix(position=[0, self.groundlevel, 0], orientation=[0, 0, 0],
                                                    scale=[.18,.5,.5]),
                                       mesh=floor[1], shader=ShadowMappingShader(self.shadows), name='floor_r')

        self.floor_l = DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[-.4, self.groundlevel, 0], orientation=[0, 0, 0],
                                                      scale=[.4, .5, .5]),
                                         mesh=floor[2], shader=ShadowMappingShader(self.shadows), name='floor_l')


        helicopter = load_obj_file('models/helicopter.obj')
        self.helicopter = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(), mesh=helicopter[0],
                                             shader=TextureShader(), name='helicopter')

        # Office
        office = load_obj_file('models/office.obj')
        self.office = [DrawModelFromMesh(scene=self,
                                        M=poseMatrix(position=[-0.3,-0.8,6], orientation=[0,radians(90),0], scale=9), mesh=mesh,
                                        shader=ShadowMappingShader(shadow_map=self.shadows), name='office') for mesh in office]

        # Office next to the bridge
        self.office2 = [DrawModelFromMesh(scene=self,
                                        M=poseMatrix(position=[-6, -0.9, -9], orientation=[0,radians(90),0], scale=[9, 9, 11]), mesh=mesh,
                                        shader=ShadowMappingShader(shadow_map=self.shadows), name='office') for mesh in office]

        # Bridge Object
        bridge = load_obj_file('models/bridge.obj')
        self.bridge = [DrawModelFromMesh(scene=self,
                                          M=poseMatrix(position=[-1, -1.4, -5], orientation=[0, 0, 0],
                                                       scale=9), mesh=mesh,
                                          shader=TextureShader(), name='office') for mesh in bridge]

        # Large buildings
        large_buildings = load_obj_file('models/large_buildings.obj')
        self.large_buildings = [DrawModelFromMesh(scene=self,
                                                  M=poseMatrix(position=[-6.1, self.groundlevel - .15, 6.85], orientation=[0, radians(90), 0], scale=18),
                                                  mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='large_buildings') for mesh in large_buildings]

        # Main skyscraper
        skyscraper = np.array(load_obj_file('models/building1.obj'))
        self.skyscraper_windows = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[1.3, self.groundlevel - 0.5, 0], orientation=[0, 0, 0], scale=0.007),
                                             mesh=skyscraper[1], shader=EnvironmentShader(map=self.environment, name='windows'), name='skyscraper_windows')

        self.skyscraper = [DrawModelFromMesh(scene=self,
                                            M=poseMatrix(position=[1.3, self.groundlevel - 0.5, 0], orientation=[0, 0, 0], scale=0.007),
                                            mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='skyscraper')
                                            for mesh in skyscraper[np.r_[0, 2]]]

        # Skyscraper right of main skyscraper
        skyscraper2 = load_obj_file('models/skyscraper2.obj')
        self.skyscraper2 = [DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[1.5, -0.3, 2], orientation=[0, 0, 0],
                                                          scale=15),
                                             mesh=mesh, shader=ShadowMappingShader(self.shadows), name='skyscraper')
                                            for mesh in skyscraper2]

        # Capitol building in front of main skyscraper
        capitol = load_obj_file('models/capitol.obj')
        self.capitol = [DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[-.35, 1, 1.2], orientation=[0, radians(90), 0],
                                                          scale=10),
                                             mesh=mesh, shader=TextureShader(), name='skyscraper')
                                            for mesh in capitol]

        stadium = load_obj_file('models/stadium.obj')
        self.stadium = [DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[5, -1 , -17], orientation=[0, 0, 0],
                                                          scale=12),
                                             mesh=mesh, shader=TextureShader(), name='stadium')
                                            for mesh in stadium]

        # London Wheel
        wheel = load_obj_file('models/wheel2.obj')
        self.wheel = [DrawModelFromMesh(scene=self,
                                        M=poseMatrix(position=[-4, self.groundlevel, 0], orientation=[0, 0, 0], scale=0.003),
                                        mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                        name='skyscraper') for mesh in wheel]

        terrace = load_obj_file('models/appart3.obj')
        self.terrace = [[DrawModelFromMesh(scene=self,
                                           M=poseMatrix(position=[7, -.3, zpos], orientation=[0,radians(-90), 0], scale=5),
                         mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows)) for mesh in terrace] for zpos in range(3,12)]

        self.terrace2 = [[DrawModelFromMesh(scene=self,
                                           M=poseMatrix(position=[7, -.3, zpos2 - .7], orientation=[0, radians(90), 0],
                                                        scale=5),
                                           mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows)) for mesh in
                         terrace] for zpos2 in range(1, 10)]

        firestation = load_obj_file('models/firestation.obj')
        self.firestation = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[-7.5, -4, -12], orientation=[0,0,0], scale=[12,10,10]), mesh=firestation[0],
                                             shader=TextureShader(), name='firestation')

        factory = load_obj_file('models/factory.obj')
        self.factory = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[-12, -.5, 4.5], orientation=[0,radians(90),0], scale=[7,9,9]), mesh=factory[0],
                                             shader=ShadowMappingShader(shadow_map=self.shadows), name='factory')

        #  --------------------------- Dinosaurs ---------------------------- #

        # Pterodactyl
        self.pterodactyl_scale = 6
        pterodactyl = load_obj_file('models/pterodactyl.obj')
        self.pterodactyl = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(), mesh=pterodactyl[0],
                                             shader=ShadowMappingShader(shadow_map=self.shadows), name='pterodactyl')

        trex1 = load_obj_file('models/trex.obj')
        self.trex =  DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[7, -1.4 , -6], orientation=[0,radians(210),0], scale=7), mesh=trex1[0],
                                             shader=TextureShader(), name='trex1')

        apataosaurus = load_obj_file('models/apatosaurus.obj')
        self.apatosaurus = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[-6.4, -.3, -9], orientation=[0,radians(100),0], scale=10), mesh=apataosaurus[0],
                                             shader=TextureShader(), name='apatosaurus')
        self.apatosaurus2 = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[13, .2, -1.3], orientation=[0, 0, 0],
                                                          scale=14), mesh=apataosaurus[0],
                                             shader=TextureShader(), name='apatosaurus2')

        fire = load_obj_file('models/fire.obj')
        self.fire = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[3.1, -.8, -3.5], orientation=[radians(-30), radians(220), radians(0)],
                                                          scale=3), mesh=fire[0],
                                             shader=TextureShader(), name='fire')

        monkey = load_obj_file('models/monkey.obj')
        self.monkey = DrawModelFromMesh(scene=self,
                                        M=poseMatrix(position=[1.2, 7.6, 0],
                                                       orientation=[0,radians(-50),0],
                                                       scale=1), mesh=monkey[0], shader=ShadowMappingShader(shadow_map=self.shadows), name='monkey')

        triceratops = load_obj_file('models/triceratops.obj')
        self.triceratops = DrawModelFromMesh(scene=self,
                                        M=poseMatrix(position=[-6, -2.2, -3], orientation=[0, radians(-50), 0],
                                                     scale=5), mesh=triceratops[0],
                                        shader=ShadowMappingShader(self.shadows), name='triceratops')

        self.triceratops2 = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[-4, -2.4, -9.5], orientation=[0, radians(-70), 0],
                                                          scale=8), mesh=triceratops[0],
                                             shader=ShadowMappingShader(self.shadows), name='triceratops')

        velociraptor = load_obj_file('models/velociraptor.obj')
        self.velociraptor = DrawModelFromMesh(scene=self,
                                        M=poseMatrix(position=[-5, -2, -1], orientation=[0, radians(50), 0],
                                                     scale=4), mesh=velociraptor[0],
                                        shader=TextureShader(), name='velociraptor')

        self.velociraptor2 = DrawModelFromMesh(scene=self,
                                              M=poseMatrix(position=[-8, -2.4, -3], orientation=[0, radians(10), 0],
                                                           scale=6), mesh=velociraptor[0],
                                              shader=TextureShader(), name='velociraptor')

        # By the flaming trex
        self.velociraptor3 = DrawModelFromMesh(scene=self,
                                               M=poseMatrix(position=[2.2, -2.3, -10], orientation=[0, radians(-100), 0],
                                                            scale=8), mesh=velociraptor[0],
                                               shader=TextureShader(), name='velociraptor')

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
        self.factory.draw()
        self.firestation.draw()
        for i in self.terrace:
            for model in i:
                model.draw()
        self.pterodactyl.draw()
        self.helicopter.draw()
        self.monkey.draw()

    def draw_reflections(self):
        self.skybox.draw()
        self.river.draw()
        self.floor_r.draw()
        self.floor_l.draw()
        for model in self.stadium:
            model.draw()
        for model in self.capitol:
            model.draw()

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

        # Draw reflections
       # self.draw_reflections()

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

            self.environment.update(self)

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
            for model in self.skyscraper2:
                model.draw()
            for model in self.stadium:
                model.draw()
            for model in self.capitol:
                model.draw()
            for i in self.terrace:
                for model in i:
                    model.draw()
            for i in self.terrace2:
                for model in i:
                    model.draw()

            self.river.draw()
            self.floor_l.draw()
            self.floor_r.draw()
            self.pterodactyl.draw()
            self.helicopter.draw()
            self.skyscraper_windows.draw()
            self.firestation.draw()
            self.factory.draw()
            self.trex.draw()
            self.apatosaurus.draw()
            self.apatosaurus2.draw()
            self.monkey.draw()
            self.velociraptor.draw()
            self.velociraptor2.draw()
            self.velociraptor3.draw()
            self.triceratops.draw()
            self.triceratops2.draw()

            self.flattened_cube.draw()
            self.show_shadow_map.draw()
            self.fire.draw()


        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def animations(self):
        self.dt += 0.01
        self.fire_timer += 0.01

        xpos = 2 * sin(self.dt)
        zpos = 2 * cos(self.dt)

        # rotations of the pterodactyl and the helicopter in the sky
        self.pterodactyl.M = poseMatrix(position=[xpos, 0.3 * sin(self.dt) + 3, zpos],
                                   orientation=[0.3 * sin(self.dt), radians(90) + self.dt, radians(20)], scale=self.pterodactyl_scale)

        self.helicopter.M = poseMatrix(position=[-xpos, 0.3 * sin(self.dt) + 4, -zpos],
                                        orientation=[-0.3 * sin(self.dt), radians(-90) + self.dt, radians(20)],
                                        scale=4)

        # timere for the fire-breathing trex
        if self.fire_timer >= 0.3:
            self.fire.visible = not self.fire.visible
            self.fire_timer = 0


if __name__ == '__main__':
    # initialises the scene object
    # scene = Scene(shaders='gouraud')
    scene = ExeterScene()

    # starts drawing the scene
    scene.run()

#TODO:
#  - Comment everything better
