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
        # Animation timers
        self.dt = 0.
        self.fire_timer = 0

        self.light = LightSource(self, position=[3., 20, -3.], Ia=[0.6, 0.6, 0.6], Id=[.6, 139/500, 147/500],
                                 Is=[.5, 139/500, 147/500])

        # for shadow map rendering
        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)


        # draw a skybox for the horizon
        self.skybox = SkyBox(scene=self)

        # Light Source

        self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=0.2),
                                            mesh=Sphere(material=Material(Ka=[10, 10, 10])), shader=PhongShader())

        self.environment = EnvironmentMappingTexture(width=200, height=200)

        self.groundlevel = -2

        # River and the floor models are part of the same object
        floor = load_obj_file('models/scene.obj')
        self.river = DrawModelFromMesh(scene=self,
                                       M=poseMatrix(position=[0, self.groundlevel, 0], orientation=[0, 0, 0], scale=.5),
                                       mesh=floor[0], shader=ShadowMappingShader(shadow_map=self.shadows), name='river')

        self.floor_r = DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[0, self.groundlevel, 0], orientation=[0, 0, 0],
                                                      scale=[.18, .5, .5]),
                                         mesh=floor[1], shader=ShadowMappingShader(shadow_map=self.shadows), name='floor_r')

        self.floor_l = DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[-.4, self.groundlevel, 0], orientation=[0, 0, 0],
                                                      scale=[.4, .5, .5]),
                                         mesh=floor[2], shader=ShadowMappingShader(shadow_map=self.shadows), name='floor_l')

        # Helicpter chasing the Pterodactyl
        helicopter = load_obj_file('models/helicopter.obj')
        self.helicopter = DrawModelFromMesh(scene=self,
                                            M=poseMatrix(), mesh=helicopter[0],
                                            shader=ShadowMappingShader(shadow_map=self.shadows), name='helicopter')

        #  --------------------------- Buildings ---------------------------- #

        # Office
        office = load_obj_file('models/office.obj')
        self.add_models_list([DrawModelFromMesh(scene=self,
                                                M=poseMatrix(position=[-0.3, -0.8, 6], orientation=[0, radians(90), 0],
                                                             scale=9), mesh=mesh,
                                                shader=ShadowMappingShader(shadow_map=self.shadows), name='office') for
                              mesh in office])

        # Office next to the bridge
        self.add_models_list([DrawModelFromMesh(scene=self,
                                                M=poseMatrix(position=[-6, -0.9, -9], orientation=[0, radians(90), 0],
                                                             scale=[9, 9, 11]), mesh=mesh,
                                                shader=ShadowMappingShader(shadow_map=self.shadows), name='office') for
                              mesh in office])

        # Bridge Object
        bridge = load_obj_file('models/bridge.obj')
        self.bridge = [DrawModelFromMesh(scene=self,
                                                M=poseMatrix(position=[-1, -1.4, -5], orientation=[0, 0, 0],
                                                             scale=9), mesh=mesh,
                                                shader=ShadowMappingShader(shadow_map=self.shadows), name='bridge') for mesh in bridge]
        self.add_models_list(self.bridge)

        # Large buildings
        large_buildings = load_obj_file('models/large_buildings.obj')
        self.large_buildings = [DrawModelFromMesh(scene=self,
                                                M=poseMatrix(position=[-6.1, self.groundlevel - .15, 6.85],
                                                             orientation=[0, radians(90), 0], scale=18),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='large_buildings') for mesh in large_buildings]
        self.add_models_list(self.large_buildings)

        # Main skyscraper
        skyscraper = np.array(load_obj_file('models/building1.obj'))
        self.skyscraper_windows = DrawModelFromMesh(scene=self,
                                                    M=poseMatrix(position=[1.3, self.groundlevel - 0.5, 0],
                                                                 orientation=[0, 0, 0], scale=0.007),
                                                    mesh=skyscraper[1],
                                                    shader=EnvironmentShader(map=self.environment, name='windows'),
                                                    name='skyscraper_windows')

        # Skyscraper
        self.skyscraper = [DrawModelFromMesh(scene=self,
                                             M=poseMatrix(position=[1.3, self.groundlevel - 0.5, 0],
                                                          orientation=[0, 0, 0], scale=0.007),
                                             mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                             name='skyscraper')
                           for mesh in skyscraper[np.r_[0, 2]]]
        self.add_models_list(self.skyscraper)

        # Skyscraper right of main skyscraper
        skyscraper2 = load_obj_file('models/skyscraper2.obj')
        self.add_models_list([DrawModelFromMesh(scene=self,
                                                M=poseMatrix(position=[1.5, -0.3, 2], orientation=[0, 0, 0],
                                                             scale=15),
                                                mesh=mesh, shader=ShadowMappingShader(self.shadows), name='skyscraper')
                              for mesh in skyscraper2])

        # Capitol building in front of main skyscraper
        capitol = load_obj_file('models/capitol.obj')
        self.capitol = [DrawModelFromMesh(scene=self,
                                          M=poseMatrix(position=[-.35, 1, 1.2], orientation=[0, radians(90), 0],
                                                       scale=10),
                                          mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='capitol')
                        for mesh in capitol]
        self.add_models_list(self.capitol)

        stadium = load_obj_file('models/stadium.obj')
        self.stadium = [DrawModelFromMesh(scene=self,
                                          M=poseMatrix(position=[5, -1, -17], orientation=[0, 0, 0],
                                                       scale=12),
                                          mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='stadium')
                        for mesh in stadium]
        self.add_models_list(self.stadium)

        # London Wheel
        wheel = load_obj_file('models/wheel2.obj')
        self.add_models_list([DrawModelFromMesh(scene=self,
                                                M=poseMatrix(position=[-4, self.groundlevel, 0], orientation=[0, 0, 0],
                                                             scale=0.003),
                                                mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows),
                                                name='skyscraper') for mesh in wheel])

        # Terraced houses
        terrace = load_obj_file('models/appart3.obj')
        self.terrace = [[DrawModelFromMesh(scene=self,
                                           M=poseMatrix(position=[7, -.3, zpos], orientation=[0, radians(-90), 0],
                                                        scale=5),
                                           mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows)) for mesh in
                         terrace] for zpos in range(3, 12)]

        self.terrace2 = [[DrawModelFromMesh(scene=self,
                                            M=poseMatrix(position=[7, -.3, zpos2 - .7], orientation=[0, radians(90), 0],
                                                         scale=5),
                                            mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows))
                          for mesh in terrace] for zpos2 in range(1, 10)]

        # Firestation Object
        firestation = load_obj_file('models/firestation.obj')
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[-7.5, -4, -12], orientation=[0, 0, 0],
                                                      scale=[12, 10, 10]), mesh=firestation[0],
                                         shader=ShadowMappingShader(shadow_map=self.shadows), name='firestation'))

        # Factory Object
        factory = load_obj_file('models/factory.obj')
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[-12, -.5, 4.5], orientation=[0, radians(90), 0],
                                                      scale=[7, 9, 9]), mesh=factory[0],
                                         shader=ShadowMappingShader(shadow_map=self.shadows), name='factory'))

        #  --------------------------- Dinosaurs ---------------------------- #

        # Pterodactyl
        self.pterodactyl_scale = 6
        pterodactyl = load_obj_file('models/pterodactyl.obj')
        self.pterodactyl = DrawModelFromMesh(scene=self,
                                             M=poseMatrix(), mesh=pterodactyl[0],
                                             shader=ShadowMappingShader(shadow_map=self.shadows), name='pterodactyl')

        # Trex in the stadium
        trex1 = load_obj_file('models/trex.obj')
        self.trex = DrawModelFromMesh(scene=self,
                                      M=poseMatrix(position=[7, -1.4, -6], orientation=[0, radians(210), 0], scale=7),
                                      mesh=trex1[0],
                                      shader=ShadowMappingShader(shadow_map=self.shadows), name='trex1')
        self.add_model(self.trex)

        brontosaurus = load_obj_file('models/apatosaurus.obj')
        # Brontosaurus by the wheel
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[-6.4, -.3, -9], orientation=[0, radians(100), 0],
                                                      scale=10), mesh=brontosaurus[0],
                                         shader=ShadowMappingShader(shadow_map=self.shadows), name='apatosaurus'))
        # Brontosaurus by the terrace
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[13, .2, -1.3], orientation=[0, 0, 0],
                                                      scale=14), mesh=brontosaurus[0],
                                         shader=ShadowMappingShader(shadow_map=self.shadows), name='apatosaurus2'))
        # Fire from the Trex
        fire = load_obj_file('models/fire.obj')
        self.fire = DrawModelFromMesh(scene=self,
                                      M=poseMatrix(position=[3.1, -.8, -3.5],
                                                   orientation=[radians(-30), radians(220), radians(0)],
                                                   scale=3), mesh=fire[0],
                                      shader=ShadowMappingShader(shadow_map=self.shadows), name='fire')
        # Monkey on the building
        monkey = load_obj_file('models/monkey.obj')
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[1.2, 7.6, 0],
                                                      orientation=[0, radians(-50), 0],
                                                      scale=1), mesh=monkey[0],
                                         shader=ShadowMappingShader(shadow_map=self.shadows), name='monkey'))
        # Smaller triceratops
        triceratops = load_obj_file('models/triceratops.obj')
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[-6, -2.2, -3], orientation=[0, radians(-50), 0],
                                                      scale=5), mesh=triceratops[0],
                                         shader=ShadowMappingShader(self.shadows), name='triceratops'))
        # Big triceratops
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[-4, -2.4, -9.5], orientation=[0, radians(-70), 0],
                                                      scale=8), mesh=triceratops[0],
                                         shader=ShadowMappingShader(self.shadows), name='triceratops'))
        # Velociraptor by on the wheel
        velociraptor = load_obj_file('models/velociraptor.obj')
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[-5, -2, -1], orientation=[0, radians(50), 0],
                                                      scale=4), mesh=velociraptor[0],
                                         shader=ShadowMappingShader(shadow_map=self.shadows), name='velociraptor'))
        # Velociraptor by the triceratops
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[-8, -2.4, -3], orientation=[0, radians(10), 0],
                                                      scale=6), mesh=velociraptor[0],
                                         shader=ShadowMappingShader(shadow_map=self.shadows), name='velociraptor2'))

        # Velociraptor by the flaming trex
        self.add_model(DrawModelFromMesh(scene=self,
                                         M=poseMatrix(position=[2.2, -2.3, -10], orientation=[0, radians(-100), 0],
                                                      scale=8), mesh=velociraptor[0],
                                         shader=ShadowMappingShader(shadow_map=self.shadows), name='velociraptor3'))

    def draw_shadow_map(self):
        # Draw the shadows for the objects
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for model in self.skyscraper:
            model.draw()
        for model in self.stadium:
            model.draw()
        self.pterodactyl.draw()
        self.helicopter.draw()
        self.floor_r.draw()
        self.floor_l.draw()
        self.river.draw()

    def draw_reflections(self):
        # Draw the reflections of the objects
        self.river.draw()
        self.floor_r.draw()
        self.floor_l.draw()
        for model in self.stadium:
            model.draw()
        for model in self.capitol:
            model.draw()
        self.trex.draw()
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

        # Update the animations
        self.animations()

        # render the shadows
        self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:
            self.environment.update(self)
            self.skyscraper_windows.draw()
            self.show_shadow_map.draw()

        # Draw all the objects in the scene
        for model in self.models:
            model.draw()

        # Draw the model groups
        for i in self.terrace:
            for model in i:
                model.draw()
        for i in self.terrace2:
            for model in i:
                model.draw()
        self.floor_l.draw()
        self.floor_r.draw()
        self.river.draw()
        # Draw the objects that have animations
        self.helicopter.draw()
        self.pterodactyl.draw()
        self.fire.draw()
        self.show_light.draw()


        # Once we are done drawing, we display the scene and use double buffering to avoid artefacts:
        if not framebuffer:
            pygame.display.flip()

    def animations(self):
        '''
        This function update the animations of objects over time
        '''

        self.dt += 0.02  # Delta time for the animations
        self.fire_timer += 0.02  # Timer for when to visualise the fire for the T-Rex

        # Updating the position of xpos over sin and zpos over cos makes the object rotate in a circle
        xpos = 2 * sin(self.dt)
        zpos = 2 * cos(self.dt)
        ypos = 0.3 * sin(self.dt)

        self.pterodactyl.M = poseMatrix(position=[xpos,ypos + 3, zpos],
                                        orientation=[0.3 * sin(self.dt), radians(90) + self.dt, radians(20)],
                                        scale=self.pterodactyl_scale)

        self.helicopter.M = poseMatrix(position=[-xpos, ypos + 4, -zpos],
                                       orientation=[-0.3 * sin(self.dt), radians(-90) + self.dt, radians(20)],
                                       scale=4)

        # Switch the fire on or off if the timer reaches 0.3
        if self.fire_timer > 0.3:
            self.fire.visible = not self.fire.visible
            self.fire_timer = 0  # Reset the timer back to 0


if __name__ == '__main__':
    # initialises the scene object
    scene = ExeterScene()

    # starts drawing the scene
    scene.run()
