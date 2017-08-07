#!/usr/bin/env python

'''
Makes the PDDL problem file ("problem.pddl")
SINGLE UAV VERSION

Written by Joseph Kim
'''


# Enter map coordinates
xy = dict()
xy['r2'] = [0,0]
xy['p2'] = [1,0]
xy['r1'] = [0,3]
xy['p1'] = [1,4]
xy['base'] = [3,2]
xy['packagecenter'] = [5,2]
xy['uav2'] = [4,0]
xy['p4'] = [5,0]
xy['p3'] = [5,4]
xy['uav1'] = [6,4]

# Enter parameters
fuel = 20
fuel_capacity = 20
package_capacity = 2
packagecount = 2
cost_surveil = 2
cost_intercept = 3
totalFuelLimit = 30


def getDistance(xy1, xy2):
	return abs(xy1[0]-xy2[0])+abs(xy1[1]-xy2[1])


# MAIN
with open('problem.pddl','w') as f:
	f.write('(define (problem uav1)\n')
	f.write('(:domain uav)\n')
	f.write('(:objects\n\t')

	# List objects
	for item in sorted(xy.keys()):
		f.write(item+' ')
	f.write('\n)')


	# Initial conditions
	f.write('\n\n(:init \n')
	f.write('\t(at base)\n') 
	f.write('\t(= (fuel) '+str(fuel)+')\n')
	f.write('\t(= (fuel_capacity) '+str(fuel_capacity)+')\n')
	f.write('\t(= (packagecount) '+str(packagecount)+')\n')
	f.write('\t(= (package_capacity) '+str(package_capacity)+')\n')
	f.write('\t(= (cost_surveil) '+str(cost_surveil)+')\n')
	f.write('\t(= (cost_intercept) '+str(cost_intercept)+')\n')
	f.write('\t(= (num_resolved) 0)\n');
	f.write('\t(= (totalFuelUsage) 0)\n');
	f.write('\n\n')


	# Input requirements
	f.write('\t(require_surveil r1)\n')
	f.write('\t(require_surveil r2)\n')
	f.write('\t(require_intercept uav1)\n')
	f.write('\t(require_intercept uav2)\n')
	f.write('\t(require_package p1)\n')
	f.write('\t(require_package p2)\n')
	f.write('\t(require_package p3)\n')
	f.write('\t(require_package p4)\n')
	f.write('\n\n')


	# Distances
	f.write('\t; DISTANCES\n')
	for pos1 in sorted(xy.keys()):
		for pos2 in sorted(xy.keys()):
			if pos1 != pos2:

				dist = getDistance(xy[pos1], xy[pos2])

				# Corrections due to uncrossable region
				if set([pos1,pos2]) == set(['r1','r2']):
					dist = dist + 4
				elif set([pos1,pos2]) == set(['r1','p2']):
					dist = dist + 2
				elif set([pos1,pos2]) == set(['p1','r2']):
					dist = dist + 2
				elif set([pos1,pos2]) == set(['p1','p2']):
					dist = dist + 2

				# Write out
				f.write('\t(= (distance '+pos1+' '+pos2+') '+str(dist)+')\n')


	f.write(')\n\n')

	# Goal Specification 
	f.write('(:goal (and \n')
	f.write('\t(<= (totalFuelUsage) '+str(totalFuelLimit)+')\n')
	f.write('\t(>= (num_resolved) 3)\n')
	f.write('))\n\n\n')

	# Metric
	f.write('(:metric minimize (totalFuelUsage)');
	f.write('\n))')
