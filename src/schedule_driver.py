#Runs parses input files and runs one instance of schedule_optimizer from the command line
import sys

usage = "driver.py <initial state filepath> <resource weight filepath> <output schedule filepath> <optimizing country name> <max depth> <# output schedules> <maximum frontier size>"

if len(sys.argv) != 8:
    print(usage)
    sys.exit(1)

state_file, resource_file, output_file, my_country = sys.argv[1:5]
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

#sanity check the filepaths and country name


#initialize and run scheduler
