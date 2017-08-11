import glfw
import numpy as np
from OpenGL.GL import *
import ctypes
import pyrr
import shaderloader
from PIL import Image
from math import sin
import textureloader
import time
import threading

from objloader import *


def showfps():
	title = ("FPS : {0:.0f}".format(1/(time.time()-t1)))
	glfw.set_window_title (window, title)

def main(instance_array,a,b,c):
	back = a+b+c
	global window
	global t1

	if not glfw.init():
		return
	w_width, w_height = 1280, 720


	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,3)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,2)
	glfw.window_hint(glfw.OPENGL_PROFILE,glfw.OPENGL_CORE_PROFILE)
	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

	window = glfw.create_window(w_width, w_height, "test",None,None)


	if not window:
		glfw.terminate()
		return

	glfw.make_context_current(window)

	cube = [-0.5, -0.5,  0.5, 0.0, 0.0,
			 0.5, -0.5,  0.5, 1.0, 0.0,
			 0.5,  0.5,  0.5, 1.0, 1.0,
			-0.5,  0.5,  0.5, 0.0, 1.0,

			-0.5, -0.5, -0.5, 0.0, 0.0,
			 0.5, -0.5, -0.5, 1.0, 0.0,
			 0.5,  0.5, -0.5, 1.0, 1.0,
			-0.5,  0.5, -0.5, 0.0, 1.0,

			 0.5, -0.5, -0.5, 0.0, 0.0,
			 0.5,  0.5, -0.5, 1.0, 0.0,
			 0.5,  0.5,  0.5, 1.0, 1.0,
			 0.5, -0.5,  0.5, 0.0, 1.0,

			-0.5,  0.5, -0.5, 0.0, 0.0,
			-0.5, -0.5, -0.5, 1.0, 0.0,
			-0.5, -0.5,  0.5, 1.0, 1.0,
			-0.5,  0.5,  0.5, 0.0, 1.0,

			-0.5, -0.5, -0.5, 0.0, 0.0,
			 0.5, -0.5, -0.5, 1.0, 0.0,
			 0.5, -0.5,  0.5, 1.0, 1.0,
			-0.5, -0.5,  0.5, 0.0, 1.0,

			 0.5,  0.5, -0.5, 0.0, 0.0,
			-0.5,  0.5, -0.5, 1.0, 0.0,
			-0.5,  0.5,  0.5, 1.0, 1.0,
			 0.5,  0.5,  0.5, 0.0, 1.0]

	cube = np.array(cube, dtype=np.float32)

	indices = [ 0,  1,  2,  2,  3,  0,
				4,  5,  6,  6,  7,  4,
				8,  9, 10, 10, 11,  8,
			   12, 13, 14, 14, 15, 12,
			   16, 17, 18, 18, 19, 16,
			   20, 21, 22, 22, 23, 20]

	indices = np.array(indices, dtype=np.uint32)


	VAO = glGenVertexArrays(1)
	glBindVertexArray(VAO)

	shader = shaderloader.compile_shader("second.vs","second.fs")
	
	VBO = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER,VBO)
	glBufferData(GL_ARRAY_BUFFER,cube.itemsize*len(cube),cube,GL_STATIC_DRAW)

	
	EBO = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)
	

	glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,cube.itemsize * 5,ctypes.c_void_p(0))
	glEnableVertexAttribArray(0)

	glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,cube.itemsize * 5,ctypes.c_void_p(12))
	glEnableVertexAttribArray(1)

	offset=1

	

	instance_array = np.array(instance_array,np.float32).flatten()


	instanceVBO = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER,instanceVBO)
	glBufferData(GL_ARRAY_BUFFER,instance_array.itemsize*len(instance_array),instance_array,GL_STATIC_DRAW)

	glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))
	glEnableVertexAttribArray(2)
	glVertexAttribDivisor(2,1)


	crate = textureloader.load_texture("crate.jpg")
	brick = textureloader.load_texture("brick.jpg")
	metal = textureloader.load_texture("metal.jpg")
	sq = textureloader.load_texture("sq.jpg")
	red = textureloader.load_texture("red.jpg")
	concrete = textureloader.load_texture("concrete-2.jpg")

	
	glUseProgram(shader)

	glClearColor(0.2,0.3,0.2,1.0)

	glEnable(GL_DEPTH_TEST)

	glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

	view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,0,0]))
	projection = pyrr.matrix44.create_perspective_projection_matrix(45.0,w_width/w_height,0.1,10000.0)
	model = pyrr.matrix44.create_from_translation(pyrr.Vector3([0,-20,-1.5*back]))

	
	vp = pyrr.matrix44.multiply(view,projection)
	

	vp_loc = glGetUniformLocation(shader,"vp")
	model_loc= glGetUniformLocation(shader,"model")
	glUniformMatrix4fv(model_loc,1,GL_FALSE,model)
	glBindTexture(GL_TEXTURE_2D, concrete)
	

	glUniformMatrix4fv(vp_loc,1,GL_FALSE,vp)


	t1 = time.time()
	while not glfw.window_should_close(window):
		t1 = time.time()
		glfw.poll_events()


		rot_x = pyrr.Matrix44.from_x_rotation(0.1 *glfw.get_time())
		rot_y = pyrr.Matrix44.from_y_rotation(0.2 *glfw.get_time())
		rot_z = pyrr.Matrix44.from_z_rotation(0.0 *glfw.get_time())

		rot = pyrr.matrix44.multiply(rot_x, rot_y)
		rot = pyrr.matrix44.multiply(rot, rot_z)
		rot = pyrr.matrix44.multiply(rot, model)

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		glUniformMatrix4fv(model_loc, 1, GL_FALSE,rot)
		
		glDrawElementsInstanced(GL_TRIANGLES,len(indices),GL_UNSIGNED_INT,None,len(instance_array))
		

		glfw.swap_buffers(window)
		showfps()

	glfw.terminate()

if __name__ == "__main__":
	main()
