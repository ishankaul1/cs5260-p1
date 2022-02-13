#Runs parses input files and runs one instance of schedule_optimizer from the command line
import resource
import sys
from os import path
import csv
from tokenize import String


def err(msg: String):
    print('ERROR: ' + msg)
    sys.exit(1)

usage = "driver.py <initial state filepath> <resource weight filepath> <output schedule filepath> <optimizing country name> <max depth> <# output schedules> <maximum frontier size>"

if len(sys.argv) != 8:
    print(usage)
    sys.exit(1)

state_filename, resources_filename, output_filename, my_country = sys.argv[1:5]
max_depth, num_output_schedules, max_frontier_size = [int(x) for x in sys.argv[5:]]

#sanity check the ints
if max_depth < 1:
    print("Max depth must be a number greater than 1")
    sys.exit(1)
if num_output_schedules < 1:
    print("Number of output schedules must be a number greater than 1")
    sys.exit(1)
if max_frontier_size < 1:
    print("Max frontier size must be a number greater than 1")
    sys.exit(1)

#sanity check the filepaths
if not path.isfile(state_filename):
    err("INIT STATE file '" + state_filename + "' does not exist")
    
elif not len(state_filename) > 4 and state_filename[-4:] == '.csv':
    err("INIT STATE file '" + state_filename + "' is not a csv")


if not path.isfile(resources_filename):
    err("RESOURCE file '" + resources_filename + "' does not exist")
    
elif not len(resources_filename) > 4 and resources_filename[-4:] == '.csv':
    err("INIT STATE file '" + resources_filename + "' is not a csv")
    

resources_file = open(resources_filename)
state_file = open(state_filename)

#parse resources and init state
#resources: DICT {key='resource_name', val=(int)'weight'}
#init_state: DICT {key='country_name', val={key='resource_name': val=(int)current_amount}}
resources = {}
init_state = {}

#read resource file
resources_reader = csv.reader(resources_file)
resources_header = [x.strip() for x in next(resources_reader)]
resources_rows = []

for row in resources_reader:
    resources_rows.append(row)

#print(resources_header) #debug
#print(resources_rows) #debug statement

if len(resources_rows) != 1:
    err('Should only be one row in resource weight file ' + resources_filename)

#build resource dict
for i in range(len(resources_header)):
    try:
        resources[resources_header[i].strip()] = int(resources_rows[0][i])
    except:
        if resources_rows[0][i].strip() != 'x':
            err('Resource weights can only be int or "x"')
        else:
            resources[resources_header[i].strip()] = resources_rows[0][i].strip()

#print(resources) #debug

#read init state file
state_reader = csv.reader(state_file)
state_header = [x.strip() for x in next(state_reader)]
state_rows = []

for row in state_reader:
    state_rows.append(row)

print('state header')
print(state_header)
print('resource header')
print(resources_header)

#Ensure state file and resource file resources are the same
if (set(state_header[1:]) != set(resources_header)):
    err('Please ensure resources in resources file "' + resources_filename + '" and state file "' + state_filename + '" match.')



#build state dict: TODO
for row in state_rows:
    country = row[0].strip()
    init_state[country] = {}
    for i in range(1, len(row)):
        try:
            init_state[country][state_header[i].strip()] = int(row[i].strip())
        except:
            err('Please ensure all resource state values in state input file "' + state_filename + '" are integers')
         

#sanity check - country name exists in state structure
if my_country not in init_state:
    err('Please ensure ' + my_country + ' is included in the state file ' + state_filename)

print('\n\n')
print(init_state)

#initialize and run scheduler
print('ALL INPUTS INITIALIZED! BUILDING SCHEDULER')
