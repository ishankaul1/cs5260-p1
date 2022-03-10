#Implementations of various state quality function possibilities
#All state quality functions should take in a dict of {resource: value} pairs that represent how much of each resource
#one country has at the time. The state quality function should output a value representative of how 'good' the current
#state of that country is based on the resources

#the most naive version possible
def state_quality_basic(resources: dict)-> float:
    return sum(resources.values())
