# pygame is just used to create a window with the operating system on which to draw.
import pygame

# imports all openGL functions
from OpenGL.GL import *

# import the shader class
from shaders import *
# import the camera class
from camera import Camera

# and we import a bunch of helper functions
from matutils import *

from lightSource import LightSource

class Scene:
    '''
    This is the main class for adrawing an OpenGL scene using the PyGame library
    '''
    def __init__(self, width=800, height=600, shaders=None):
        '''
        Initialises the scene
        '''

        self.window_size = (width, height)

        # by default, wireframe mode is off
        self.wireframe = False

        # the first two lines initialise the pygame window. You could use another library for this,
        # for example GLut or Qt
        pygame.init()
        screen = pygame.display.set_mode(self.window_size, pygame.OPENGL | pygame.DOUBLEBUF, 24)

        # Here we start initialising the window from the OpenGL side
        glViewport(0, 0, self.window_size[0], self.window_size[1])

        # this selects the background color
        glClearColor(0.7, 0.7, 1.0, 1.0)

        # enable back face culling (see lecture on clipping and visibility
        glEnable(GL_CULL_FACE)
        # depending on your model, or your projection matrix, the winding order may be inverted,
        # Typically, you see the far side of the model instead of the front one
        # uncommenting the following line should provide an easy fix.
        glCullFace(GL_BACK)

        # enable the vertex array capability
        glEnableClientState(GL_VERTEX_ARRAY)

        # Enable MSAA anti-aliasing

        # enable depth test for clean output (see lecture on clipping & visibility for an explanation
        glEnable(GL_DEPTH_TEST)

        # set the default shader program (can be set on a per-mesh basis)
        self.shaders = 'phong'

        # initialise the projective transform
        near = 1.0
        far = 50.0
        left = -1.0
        right = 1.0
        top = -1.0
        bottom = 1.0

        # cycle through models
        self.show_model = -1

        # to start with, we use an orthographic projection; change this.
        self.P = frustumMatrix(left, right, top, bottom, near, far)

        # initialises the camera object
        self.camera = Camera()

        # initialise the light source
        self.light = LightSource(self, position=[5., 5., 5.])

        # rendering mode for the shaders
        self.mode = 1  # initialise to full interpolated shading

        # This class will maintain a list of models to draw in the scene,
        self.models = []

    def add_model(self, model):
        '''
        This method just adds a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        '''

        # bind the default shader to the mesh
        # model.bind_shader(self.shaders)

        # and add to the list
        self.models.append(model)

    def add_models_list(self, models_list):
        '''
        This method just adds a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        '''
        for model in models_list:
            self.add_model(model)

    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        if not framebuffer:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # ensure that the camera view matrix is up to date
            self.camera.update()

        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        '''
        Method to process keyboard events. Check Pygame documentation for a list of key events
        :param event: the event object that was raised
        '''
        if event.key == pygame.K_q:
            self.running = False

        # flag to switch wireframe rendering
        elif event.key == pygame.K_0:
            if self.wireframe:
                print('--> Rendering using colour fill')
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                self.wireframe = False
            else:
                print('--> Rendering using colour wireframe')
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                self.wireframe = True

    def pygameEvents(self):
        '''
        Method to handle PyGame events for user interaction.
        '''
        # check whether the window has been closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # keyboard events
            elif event.type == pygame.KEYDOWN:
                self.keyboard(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mods = pygame.key.get_mods()

                # Events for the scroll wheel
                if event.button == 4:
                    if mods & pygame.KMOD_CTRL:
                        # Rotate the light source
                        self.light.position *= 1.1
                        self.light.update()
                    else:
                        # Zoom the camera in
                        self.camera.distance = max(1, self.camera.distance - 1)

                elif event.button == 5:
                    if mods & pygame.KMOD_CTRL:
                        # Rotate the light source
                        self.light.position *= 0.9
                        self.light.update()
                    else:
                        # Zoom the camera out
                        self.camera.distance += 1

            elif event.type == pygame.MOUSEMOTION:
                # If the mouse is pressed and in movement
                if pygame.mouse.get_pressed()[0]:
                    # Move the mouse along the X and Y axis if the left mouse button is clicked
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()
                        self.camera.center[0] += (float(self.mouse_mvt[0]) / self.window_size[0])
                        self.camera.center[1] -= (float(self.mouse_mvt[1]) / self.window_size[1])
                    else:
                        self.mouse_mvt = pygame.mouse.get_rel()

                elif pygame.mouse.get_pressed()[2]:
                    # Rotate the camera around the origin if the right-mouse button is pressed
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()
                        self.camera.phi -= (float(self.mouse_mvt[0]) / self.window_size[0])
                        self.camera.psi -= (float(self.mouse_mvt[1]) / self.window_size[1])
                    else:
                        # Get the mouse position
                        self.mouse_mvt = pygame.mouse.get_rel()
                else:
                    self.mouse_mvt = None

    def run(self):
        '''
        Draws the scene in a loop until exit.
        '''

        # We have a classic program loop
        self.running = True
        while self.running:

            self.pygameEvents()

            # otherwise, continue drawing
            self.draw()
