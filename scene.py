# pygame is just used to create a window with the operating system on which to draw.
import pyglet.window
from pyglet.gl import *
from pyglet.window import key, mouse
# imports all openGL functions

# import the camera class
from camera import Camera
from pywavefront import visualization
# and we import a bunch of helper functions
from matutils import *
import ctypes
from lightSource import LightSource


class Scene(pyglet.window.Window):
    '''
    This is the main class for adrawing an OpenGL scene using the PyGame library
    '''
    def __init__(self, width=1280, height=720, shaders=None):
        '''
        Initialises the scene
        '''
        super(Scene, self).__init__(width, height)

        # by default, wireframe mode is off
        self.wireframe = False
        self.alive = True
        self.window_size = [width, height]
        self.lightfv = ctypes.c_float * 4

        # initialise the camera variables
        self.camera = Camera()
        self.fov = 45
        self.dragging = False
        # This class will maintain a list of models to draw in the scene,
        self.models = []

    def on_resize(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Define the frustum matrix
        gluPerspective(45, float(width) / height, 1., 100.)
        glMatrixMode(GL_MODELVIEW)
        return True

    def add_model(self, model, M):
        '''
        This method just adds a model to the scene.
        :param model: The model object to add to the scene and its position matrix
        :return: None
        '''

        # bind the default shader to the mesh
        # model.bind_shader(self.shaders)

        # and add to the list
        self.models.append([model, M])

    def draw(self):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear
        # the scene, we also clear the depth buffer to handle occlusions

        self.clear()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Define the frustum matrix
        gluPerspective(self.camera.zoom, float(self.window_size[0]) / float(self.window_size[1]), 0.1, 100.)
        self.camera.getViewMatrix()
        glMatrixMode(GL_MODELVIEW)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glLightfv(GL_LIGHT0, GL_POSITION, self.lightfv(-1.0, 1.0, 1.0, 0.0))

        # ensure that the camera view matrix is up to date
        # self.camera.update()

        # then we loop over all models in the list and draw them
        for model in self.models:
            M = model[1]
            glLoadIdentity()

            # Apply the model matrix to the object
            glTranslatef(M[0][0], M[0][1], M[0][2])
            glRotatef(M[1][0], M[1][1], M[1][2], M[1][3])
            glScalef(M[2][0], M[2][1], M[2][2])

            # Draw the model to the screen
            visualization.draw(model[0])

        self.flip()

    def on_key_press(self, symbol, modifiers):
        '''
        Method to process keyboard events. Check Pygame documentation for a list of key events
        :param event: the event object that was raised
        '''
        if symbol == key.Q:
            self.alive = False

        # flag to switch wireframe rendering
        elif symbol == key._0:
            if self.wireframe:
                print('--> Rendering using colour fill')
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                self.wireframe = False
            else:
                print('--> Rendering using colour wireframe')
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                self.wireframe = True


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # Mouse drag events
        if buttons & mouse.LEFT:
            if modifiers == key.LCTRL and dy > 0:
                # Brighten the scene
                self.light.position *= 1.1
                self.light.update()
            elif modifiers == key.LCTRL and dy < 0:
                # Dim the scene
                self.light.position *= 0.9
                self.light.update()
            else:
                # Translate the camera
                if self.dragging:
                    self.camera.mouse_movement(dx, dy)
                else:
                    self.dragging = True

        if buttons & mouse.RIGHT:
            self.camera.mouse_turn(dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        self.dragging = False

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera.scroll(scroll_y)


    def on_draw(self):
        self.draw()


    def run(self):
        while self.alive:
            self.dispatch_events()
            self.draw()
