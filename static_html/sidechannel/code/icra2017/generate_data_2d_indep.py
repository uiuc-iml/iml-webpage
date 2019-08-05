
'''
This file generates data for 2D Indep problem. 
It writes data chunk file into "data" folder. 
Each data chunk file includes 5000 examples. 
'''

from __future__ import division

import random, math
import numpy as np
from klampt import vectorops

W = 20
H = 20

obstacle_min_size = 3
obstacle_max_size = 6
obstacle_num_min = 0
obstacle_num_max = 5
label_obstacle_threshold = 1


def purely_random_environment():
	return np.random.random((W,H))>0.97

def random_environment_blocks():
	env = np.zeros((W,H))
	nobs = random.randint(obstacle_num_min,obstacle_num_max)
	for o in range(nobs):
		w = random.randint(obstacle_min_size,obstacle_max_size)
		h = random.randint(obstacle_min_size,obstacle_max_size)
		x = random.randint(0,W-1)
		y = random.randint(0,H-1)
		if x+w > W: 
			w=W-x
		if y+h > H: 
			h=H-y
		env[x:x+w,y:y+h] = 1
	return env

random_environment = purely_random_environment

class Problem:
	def __init__(self,start=None,goal=None,env=None):
		self.start = start
		self.goal = goal
		self.env = env
	def __str__(self):
		return 'Start '+str(self.start)+' goal '+str(self.goal) 
	@staticmethod
	def random():
		s = (random.randint(0,W-1),0)
		g = (random.randint(0,W-1),H-1)
		e = random_environment()
		return Problem(s,g,e)

def features(problem): # computing x
	return list(problem.start)+list(problem.goal)+[int(v) for v in problem.env.flatten().tolist()]

def concept(problem): # computing y
	d = vectorops.distance(problem.start, problem.goal)
	h = 0.2
	nsteps = int(math.ceil(d / h))
	collisions = 0
	#hacky "rasterization" by marching down segment
	for i in range(nsteps+1):
		if nsteps == 0:
			x = problem.start
		else:
			x = vectorops.interpolate(problem.start,problem.goal,i/nsteps)
		if problem.env[int(round(x[0])),int(round(x[1]))]:
			collisions += 1
			if collisions >= label_obstacle_threshold:
				# colliding
				return 0
	#collision free
	return 1

def generate_one_example():
	p = Problem.random()
	x = np.array(features(p))
	y = concept(p)
	return x, y

if __name__ == '__main__':
	N = 5000 # number of instances per data chunk file
	ite = 0
	while True:
		X = np.zeros((N, 404)).astype('float32')
		y = np.zeros(N).astype('int32')
		for i in xrange(N):
			cur_x, cur_y = generate_one_example()
			X[i,:] = cur_x
			y[i] = cur_y
		np.savez_compressed('data/data_%i.npz'%ite, X=X, y=y)
		print 'Done data chunk file %i'%ite
		ite += 1
