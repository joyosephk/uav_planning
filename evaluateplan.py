#!/usr/bin/env python

'''
Evaluates an existing plan for the uav scenario

-Requires domain and problem pddl files
-Requires VAL PDDL validator

Written by Joseph Kim
'''

from subprocess import Popen, PIPE, call
import re
import os


def validatePlan(domainfile, problemfile, plan):
    """ Using VAL validator """

    # If existing file with already in solution read format:
    if type(plan) is str and os.path.exists(plan):
        process = Popen(['validate',domainfile,problemfile,plan], stdout=PIPE)
        (output, err) = process.communicate()
    else:
        print 'Wrong setting for validate. Check input'

    # Process output and return
    valid = 1 - process.wait()
    if valid:
    	fuelusage = int(re.search(r'Final value: ([\d]+)',output).group(1))
    	return valid, fuelusage
    else:
    	print 'Plan invalid.  Check plan'



#################################################################
############### MAIN ############################################
#################################################################


# Read and preprocess a "raw" plan
with open('sampleplan_raw','r') as f:
	plan_raw = f.read().lower()
	plan_raw = plan_raw.replace('go to', 'goto')
	plan_raw = plan_raw.replace('drop package', 'drop')
	plan_raw = plan_raw.replace('region1', 'r1')
	plan_raw = plan_raw.replace('region2', 'r2')
	plan_raw = plan_raw.replace('main base', 'base')
	plan_raw = plan_raw.replace('package center', 'packagecenter')
	plan_raw = plan_raw.splitlines()

# Add ?from waypoints for "goto" actions
# Count number of resolved tasks
plan = []
loc1 = 'base'
numResolved = 0
for i,action in enumerate(plan_raw):
	if 'goto' in action:
		loc2 = action.split(' ')[1]
		goto_new = 'goto '+loc1+' '+loc2
		plan.append(goto_new)
		loc1 = loc2
	else:
		plan.append(action)
		numResolved += 1

# Write processed plan
planfile = 'sampleplan_processed'
with open(planfile,'w') as f:
	for action in plan:
		f.write('(%s)\n' % action)


# Call validator
domainfile = 'domain.pddl'
problemfile = 'problem.pddl'
valid, fuelusage = validatePlan(domainfile, problemfile, planfile)
print 'Plan valid:', valid
print 'Number of resolved tasks =', numResolved
print 'Total fuel usage =', fuelusage