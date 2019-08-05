#!/usr/bin/python

import sys
from klampt import *
from klampt import vis
from klampt.vis.glrobotprogram import *
from klampt.model import trajectory
class MyGLViewer(GLSimulationPlugin):
    def __init__(self,world,path_file):
        GLSimulationPlugin.__init__(self,world)
        self.world = world
        #The trajectory is loaded here
        self.trajectory=trajectory.Trajectory()
        self.trajectory.load(path_file)
        # if vectorops.distance(self.sim.controller(0).getSensedConfig(),self.trajectory.milestones[0])>0.1:
        #     self.sim.controller(0).addLinear(self.trajectory.milestones[0],3)     
        # speed=1
        # for i in range(len(self.trajectory.times)):
        #     self.sim.controller(0).addLinear(self.trajectory.milestones[i+1],(self.trajectory.times[i+1]-self.trajectory.times[i])/speed)


    def control_loop(self):
        sim = self.sim
        traj = self.trajectory
        starttime = 2
        robotController = self.sim.controller(0)
        if sim.getTime() > starttime:
            (q,dq) = (traj.eval(self.sim.getTime()-starttime),traj.deriv(self.sim.getTime()-starttime))
            robotController.setPIDCommand(q,dq)
        else:
            robotController.setPIDCommand(traj.milestones[0],[0]*7)
        pass


    def mousefunc(self,button,state,x,y):
        #Put your mouse handler here
        #the current example prints out the list of objects clicked whenever
        #you right click
        if button==2:
            if state==0:
                print [o.getName() for o in self.click_world(x,y)]
                return
        GLSimulationPlugin.mousefunc(self,button,state,x,y)


    def keyboardfunc(self,c,x,y):
        #Put your keyboard handler here
        #the current example toggles simulation / movie mode
     
        GLSimulationPlugin.keyboardfunc(self,c,x,y)
        self.refresh()


if __name__ == "__main__":
    if len(sys.argv)<=1:
        print "USAGE: trajectory.py [world_file] [path_file]"
        exit()
    world = WorldModel()
    for fn in sys.argv[1:]:
        res = world.readFile(fn)
        break
        if not res:
            raise RuntimeError("Unable to load model "+fn)

    
    viewer = MyGLViewer(world,sys.argv[2])
    vis.run(viewer)
