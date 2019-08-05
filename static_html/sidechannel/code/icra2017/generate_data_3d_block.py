
'''
This file generates data for 3D Block problem. 
It writes data chunk file into "data" folder. 
Each data chunk file includes 10000 examples. 
'''

from __future__ import division

import random, math
import numpy as np
from klampt import vectorops

robot_radius = 3
workspace_size = (20,20,20)
obstacle_min_size = 1
obstacle_max_size = 7
obstacle_num_min = 0
obstacle_num_max = 5

def random_environment_blocks():
	env = np.zeros(workspace_size)
	nobs = random.randint(obstacle_num_min,obstacle_num_max)
	for o in range(nobs):
		d = np.random.randint(obstacle_min_size,obstacle_max_size,(3,))
		p = np.array([random.randint(0,size-1) for size in workspace_size])
		q = np.minimum(p+d,np.array(workspace_size)-1)
		env[p[0]:q[0],p[1]:q[1],p[2]:q[2]] = 1
	return env

def sphere_collision(x,radius,grid):
	bmin = vectorops.sub(x,[radius]*len(x))
	bmax = vectorops.add(x,[radius]*len(x))
	imin = [max(0,int(v)) for v in bmin]
	imax = [min(int(v),b-1) for v,b in zip(bmax,workspace_size)]
	for i in range(imin[0],imax[0]):
		for j in range(imin[1],imax[1]):
			for k in range(imin[2],imax[2]):
				if vectorops.distanceSquared((i,j,k),x) < radius**2 and grid[i,j,k]:
					return True
	return False

def sphere_collision_tests(x,radius,grid):
	bmin = vectorops.sub(x,[radius]*len(x))
	bmax = vectorops.add(x,[radius]*len(x))
	imin = [max(0,int(v)) for v in bmin]
	imax = [min(int(v),b-1) for v,b in zip(bmax,workspace_size)]
	for i in range(imin[0],imax[0]):
		for j in range(imin[1],imax[1]):
			for k in range(imin[2],imax[2]):
				if vectorops.distanceSquared((i,j,k),x) < radius**2:
					yield (i,j,k)
	return

class Problem:
	def __init__(self,start=None,goal=None,env=None):
		self.start = start
		self.goal = goal
		self.env = env
	@staticmethod
	def random(s=None, g=None):
		if s is None:
			s = (random.randint(0,workspace_size[0]-1), random.randint(0,workspace_size[1]-1), 0)
		if g is None:
			g = (random.randint(0,workspace_size[0]-1), random.randint(0,workspace_size[1]-1), workspace_size[2]-1)
		e = random_environment_blocks()
		return Problem(s,g,e)

	@staticmethod
	def random2():
		s = (random.randint(0,workspace_size[0]-1), random.randint(0,workspace_size[1]-1), 0)
		g = (random.randint(0,workspace_size[0]-1), random.randint(0,workspace_size[1]-1), workspace_size[2]-1)
		e = random_environment_independent()
		return Problem(s,g,e)

	def features(problem): # compute x
		return list(problem.start)+list(problem.goal)+[int(v) for v in problem.env.flatten().tolist()]

	def concept(problem): # compute y
		d = vectorops.distance(problem.start,problem.goal)
		h = 0.2
		nsteps = int(math.ceil(d / h))
		collisions = 0
		#hacky "rasterization" by marching down segment
		for i in range(nsteps+1):
			if nsteps == 0:
				x = problem.start
			else:
				x = vectorops.interpolate(problem.start,problem.goal, i/nsteps)
			if sphere_collision(x,robot_radius,problem.env):
				# colliding
				return 0
		#collision free
		return 1

def save_data_chunk(idx, s=None, g=None, folder='data'):
	folder = folder.replace('/','') # remove trailing slash
	chunk_size = 10000
	X = np.zeros((chunk_size, 8006), dtype='float32')
	y = np.zeros(chunk_size, dtype='int32')
	for i in xrange(chunk_size):
		p = Problem.random(s, g)
		X[i,:] = Problem.features(p)
		y[i] = Problem.concept(p)
	np.savez_compressed('%s/data_%i.npz'%(folder, idx), X=X, y=y)
	print 'saved %s/data_%i.npz'%(folder, idx)

if __name__ == '__main__':
	ite = 0
	while True:
		save_data_chunk(ite)
		ite += 1
