#!/usr/bin/python

import sys
from klampt import *
from klampt import vis
from klampt.vis.glrobotprogram import *

class MyGLViewer(GLSimulationPlugin):
    def __init__(self,files):
        #create a world from the given files
        world = WorldModel()
        for fn in files:
            res = world.readFile(fn)
            if not res:
                raise RuntimeError("Unable to load model "+fn)
        #initialize the simulation
        GLSimulationPlugin.__init__(self,world)

        #put custom action hooks here
        self.add_action(self.some_function,'Some random function','f')

    def some_function(self):
        print "The function is called"

    def control_loop(self):
        #Put your control handler here
        pass

    def mousefunc(self,button,state,x,y):
        #Put your mouse handler here
        #the current example prints out the list of objects clicked whenever
        #you right click
        print "mouse",button,state,x,y
        if button==2:
            if state==0:
                print [o.getName() for o in self.click_world(x,y)]
            return
        GLSimulationPlugin.mousefunc(self,button,state,x,y)

    def motionfunc(self,x,y,dx,dy):
        return GLSimulationPlugin.motionfunc(self,x,y,dx,dy)

if __name__ == "__main__":
    print "gltemplate.py: This example demonstrates how to simulate a world and read user input"
    if len(sys.argv)<=1:
        print "USAGE: gltemplate.py [world_file]"
        exit()

    viewer = MyGLViewer(sys.argv[1:])
    vis.run(viewer)
