from abc import ABC, abstractmethod
from state_node import State_Node

#list of these should be read in from input file or defined at start of serach
class Transform_Template:
    def __init__(self, input_resources: dict, output_resources: dict):
        self.input_resources = input_resources
        self.output_resources = output_resources

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
    def __init__(self, transfer: Transfer_Template, country1: str, country2: str):
        self.transfer = transfer
        self.country1 = country1
        self.country2 = country2
    def isValidForState(state: State_Node, scalar: int) -> bool:
        pass #TODO: implement
    def perform(state: State_Node, scalar: int) -> State_Node:
        pass #TODO: implement
    def convertToPersistable(scalar: int):
        pass #TODO

#TODO: abstract base class for persistable
#These are actually to be stored in the schedule for a new state, after performing the action template and scalar on the state
class Persistable_Transform:
    def __init__(self, transform, country, scalar):
        self.transform = transform
        self.country = country
        self.scalar = scalar
    
class Persistable_Transfer:
     def __init__(self, transfer: Transfer_Template, country1: str, country2: str, scalar: int):
        self.transfer = transfer
        self.country1 = country1
        self.country2 = country2
        self.scalar = scalar