from abc import ABC, abstractmethod
from state_node import State_Node

#list of these should be read in from input file or defined at start of serach
class Transform_Template:
    def __init__(self, input_resources: dict, output_resources: dict):
        self.input_resources = input_resources #form; {resource: value}
        self.output_resources = output_resources #form: {resource: value}

#all possible transfer ratios should be determined based on the resources file
class Transfer_Template:
    def __init__(self, resource1, resource1_amount, resource2, resource2_amount):
        self.resource1 = resource1
        self.resource1_amount = resource1_amount
        self.resource2 = resource2
        self.resource2_amount = resource2_amount

#base class for actions
class Action(ABC):
    @abstractmethod
    def isValidForState(state: State_Node, scalar: int) -> bool:
        pass

    @abstractmethod
    def perform(state: State_Node, scalar: int) -> State_Node: 
        pass


#TODO: abstract base class for persistable
#These are actually to be stored in the schedule for a new state, after performing the action template and scalar on the state
class Persistable_Transform:
    #resources in {}
    def __init__(self, transform_template: Transform_Template,  country: str):
        self.transform_template = transform_template
        self.country = country
        
    def debug(self):
        print("TRANSFORM: ")
        print("\tCountry: " + self.country)
        print("\tInput: {"  + ','.join([resource + ': ' + str(self.transform_template.input_resources[resource]) for resource in self.transform_template.input_resources]) + "}" )
        print("\tOutput: {"  + ','.join([resource + ': ' + str(self.transform_template.output_resources[resource]) for resource in self.transform_template.output_resources]) + "}\n" )

class Persistable_Transfer:
    def __init__(self, transfer: Transfer_Template, country1: str, country2: str):
        self.transfer = transfer
        self.country1 = country1
        self.country2 = country2

    def debug(self):
        print("TRANSFER:")
        print("\tCountry1: " + self.country1)
        print("\tResource1: {" + self.transfer.resource1 + ": " + str(self.transfer.resource1_amount) + "}")
        print("\tCountry2: " + self.country2)
        print("\tResource2: {" + self.transfer.resource2 + ": " + str(self.transfer.resource2_amount) + "}\n")


#These are created at the very start of the program, one for each transform template. These are to be used to determine whether a transform is possible on a state, and to actually make the transform on the state.
class Actionable_Transform(Action):
    def __init__(self, transform: Transform_Template, country: str):
        self.transform = transform
        self.country = country
    def isValidForState(state: State_Node, scalar: int) -> bool:
        pass #TODO: implement
    def perform(state: State_Node, scalar: int) -> State_Node:
        pass #TODO: implement
    def convertToPersistable(scalar: int):
        pass #TODO

#These are created at the very start of the program, one for each transfer template * country (country1 is always your own country). These are to be used to determine whether a transfer is possible on a state, and to actually make the transfer on the state.
class Actionable_Transfer(Action):
    def __init__(self, transfer_template: Transfer_Template, country1: str, country2: str):
        self.transfer_template = transfer_template
        self.country1 = country1
        self.country2 = country2

    def isValidForState(self, stateNode: State_Node, scalar: int) -> bool:
        #checks if both countries have enough of their respective resources in the state using transform template and scalar
       
       #resource and state in country: resource: value format
        
        if (self.transfer_template.resource1_amount * scalar) > stateNode.state[self.country1][self.transfer_template.resource1] or (self.transfer_template.resource2_amount * scalar) > stateNode.state[self.country1][self.transfer_template.resource2]:
            return False

        return True

    #subtract c1 loses r1 and gains r2, c2 loses r2 and gains r1 
    def perform(self, stateNode: State_Node, scalar: int) -> State_Node:
        if not self.isValidForState(stateNode, scalar) :
            return stateNode 

        stateNode.state[self.country1][self.transfer_template.resource1] = stateNode.state[self.country1][self.transfer_template.resource1] - (self.transfer_template.resource1_amount * scalar) 
        stateNode.state[self.country1][self.transfer_template.resource2] = stateNode.state[self.country1][self.transfer_template.resource2] + (self.transfer_template.resource2_amount * scalar)

        stateNode.state[self.country2][self.transfer_template.resource2] = stateNode.state[self.country2][self.transfer_template.resource2] - (self.transfer_template.resource2_amount * scalar) 
        stateNode.state[self.country2][self.transfer_template.resource2] = stateNode.state[self.country2][self.transfer_template.resource1] + (self.transfer_template.resource1_amount * scalar)

        return stateNode

        
    def convertToPersistable(self, scalar: int) -> Persistable_Transfer:
        return Persistable_Transfer(Transfer_Template(self.transfer_template.resource1, self.transfer_template.resource1_amount * scalar, self.transfer_template.resource2, self.transfer_template.resource2_amount * scalar), self.country1, self.country2)



    

def persistableTransformPrintTest():
    p = Persistable_Transform(transform_template=Transform_Template(input_resources={'r1': 4, 'r2': 8}, output_resources={'r3': 3}), country='Poopadovia')
    p.debug()
    
def persistableTransferPrintTest():
    a = Actionable_Transfer(transfer_template=Transfer_Template('poopsticks', 5, 'cheeseballs', 3), country1='Pooplantis', country2="Swagamerica")
    p = a.convertToPersistable(3)
    p.debug()

persistableTransformPrintTest()
persistableTransferPrintTest()