#Module to hold all logic for representing and generating states, as well as doing calculations around states.

#Key variables:
#   state: DICT - representation of current world
#   schedule: array[Actions] - The schedule of actions up to this point
#   likelihood: float (0, 1) - Calculated likelihood of reaching this point
#   utility: (could just be a function?) - Expected utility calculated based on depth, likelihood, and state utility.
#   state_quality_function: function(input: state, country) - Passed in from the top scheduler program, which can use to use any state quality function it desires. Outputs raw state quality for that country based on the state.
#   init_qualities: DICT - quality of the initial state of each country for comparison & calculation of discounted reward
#Pass in: - on second thought, let state generator and scheduler handle this
#   prev_likelihood
#   state
#   schedule
#   state_quality_function
#Key functions
#   get_depth(): length of schedule
#   get_schedule(): returns the schedule
#   get_state(): returns the state
#   get_init_quality(input: (string) country): return the init state quality of the country
#   calc_state_quality(input: (string) country): calculates the raw state quality based on the node's state and state quality function, for the input country in question.
#   calc_undiscounted_reward(input: (string) country): subtracts results of calc_state_quality from initial state quality for the country in question
#   calc_discounted_reward(input: (string) country): multiplies results of calc_state_quality with a multiplier based on the depth of the schedule, then subtracts from the initial state quality for the country
#   calc_country_likelihood(input: (string) country, prev_discounted_reward: float): uses discounted reward for a country at this state and subtracts from that of the last to calculate how likely the country is to accept the proposal. Can pass in a function used to calculate to the state object. This should be used only on the receiving country of a transform to feed into calculation of the new likelihood.
#   calc_total_likelihood(): gives the final likelihood of this state. Multiplies init likelihood with likelihood of the new transaction
#   calc_expected_utility(): calculates expected utility based on total likelihood and discounted reward
#   get_utility(): return the calculated utility

from functools import total_ordering
from typing import Callable
import copy
import actions
#rom actions import Actionable_Transfer, Actionable_Transform
import actions

#Just use to hold and get information about the state that needs to be memoized
@total_ordering
class StateNode:
    def __init__(self, state: dict, schedule: list, schedule_likelihood: float, expected_utility: float):
        self.state = state
        self.schedule = schedule
        self.schedule_likelihood = schedule_likelihood
        self.expected_utility = expected_utility

    #need ordering for priority queueing
    def __lt__(self, other):
        return self.expected_utility < other.expected_utility

    def __eq__(self, other):
        return self.expected_utility == other.expected_utility

    #safely copy state st operations on the new copy will not affect the old state
    def __copy__(self):
        return StateNode(state=copy.deepcopy(self.state), schedule=copy.copy(self.schedule), schedule_likelihood=self.schedule_likelihood, expected_utility=self.expected_utility)

#All functionality for creating a new state node from a state and transaction
#Is a static, one-use object
class StateGenerator:
    #Initial state - state of the world at the very beginning. Used to calculate initial state qualities for later discounted reward calculation.
    #State quality function - takes in a dict of {resouce: value} mappings for ONE country, and outputs an int that represents the quality of the state for that country.
    def __init__(self, my_country: str, init_state: dict, state_quality_function: callable()):
        self.my_country = my_country
        self.state_quality_function = state_quality_function
        #For all state generation, we need to have access to the INITIAL utility of each country, so that we can determine
        #the final discounted reward of each transaction
        self.init_utilities: dict = self.calc_init_utilities(init_state)

    def calc_init_utilities(self, init_state: dict) -> dict:
        init_utilities = {}
        for country in init_state:
            init_utilities[country] = self.state_quality_function(init_state[country])

        return init_utilities


    # #Logic for validating a single action against a state
    def isvalidactionforstate(self, action: actions.Action, statenode: StateNode, scalar: int) -> bool:
        if isinstance(action, actions.ActionableTransfer):
            return self.isvalidtransferforstate(action, statenode, scalar)
        elif isinstance(action, actions.ActionableTransform):
            return self.isvalidtransformforstate(action, statenode, scalar)
        return False

    def isvalidtransferforstate(self, action: actions.ActionableTransfer, statenode: StateNode, scalar: int) -> bool:
        # #TODO: add resource validation
        if (action.template.resource1_amount * scalar) > statenode.state[action.country1][action.template.resource1] or (action.template.resource2_amount * scalar) > statenode.state[action.country1][action.template.resource2]:
            return False
        return True

    def isvalidtransformforstate(self, action: actions.ActionableTransform, statenode: StateNode, scalar: int) -> bool:
        # #TODO: add resource validation
        for resource in action.template.input_resources:
            if statenode.state[action.country][resource] < action.template.input_resources[resource] * scalar:
                return False
        return True

    # #Logic for performing a single action on a state
    def performactiononstate(self,action: actions.Action, statenode: StateNode, scalar: int ) -> StateNode:
        if isinstance(action, actions.ActionableTransfer):
            self.performtransferonnewstate(statenode=statenode, action=action, scalar=scalar)
        elif isinstance(action, actions.ActionableTransform):
            self.performtransformonnewstate(statenode=statenode, action=action, scalar=scalar)
        else:
            print("WARNING: performed null action on copied state")
        return statenode

    #Edits state with a transfer action
    def performtransferonnewstate(self, action: actions.ActionableTransfer, statenode: StateNode, scalar: int) -> StateNode:
        statenode.state[action.country1][action.template.resource1] = statenode.state[action.country1][action.template.resource1] - (action.template.resource1_amount * scalar)
        statenode.state[action.country1][action.template.resource2] = statenode.state[action.country1][action.template.resource2] + (action.template.resource2_amount * scalar)
        statenode.state[action.country2][action.template.resource2] = statenode.state[action.country2][action.template.resource2] - (action.template.resource2_amount * scalar)
        statenode.state[action.country2][action.template.resource1] = statenode.state[action.country2][action.template.resource1] + (action.template.resource1_amount * scalar)
        return statenode

    #Edits state with a transfer action
    def performtransformonnewstate(self, action: actions.ActionableTransform, statenode: StateNode, scalar: int) -> StateNode:
        for resource in action.template.input_resources:
            statenode.state[action.country][resource] = statenode.state[action.country][resource] - (action.template.input_resources[resource] * scalar)
        for resource in action.template.output_resources:
            statenode.state[action.country][resource] = statenode.state[action.country][resource] + (action.template.output_resources[resource] * scalar)
            return statenode

    #Function takes an init state and an action. If the action is valid on the state in the current context, it creates a new statenode with the new state after performing.
    #Then, builds ALL new properties of the state (schedule, schedule likelihood, and expected utility), and returns the state.
    #Returns none if the state was invalid
    #TODO
    def buildNewStateFromTransform(self, init_state: StateNode, transaction: actions.Action, scalar: int) -> StateNode or None:
        # #1. Check if action is valid (driver can do this too, might be better)
        if not self.isvalidactionforstate(action=transaction, statenode=init_state, scalar=scalar):
            return None

        # #2. Copy state, perform action, generate a new persistable action for schedule and calculations, and get your discounted reward
        newstate = copy.copy(init_state)
        self.performactiononstate(action=transaction, statenode=newstate, scalar=scalar)
        actionRecord = transaction.convertToPersistable(scalar)
        newstate.schedule.append(actionRecord)
        my_discountedreward = self.calc_discounted_reward(state=newstate, country=self.my_country, depth=len(newstate.schedule))

        # #3. If action was a transfer, get the discounted reward of second country to get the action likelihood. Then, multiply by
        # the newstate's current schedule_likelihood to get the new overall likelihood
        if isinstance(transaction, actions.ActionableTransfer): #likelihood only changes when another country is involved
            other_discountedreward = self.calc_discounted_reward(state=newstate, country=transaction.country2, depth=len(newstate.schedule)) #ASSUMPTION FOR THIS PROGRAM IS THAT COUNTRY2 IS ALWAYS THE OTHER
            action_likelihoood = self.calc_likelihood_from_reward(other_discountedreward)
            newstate.schedule_likelihood = newstate.schedule_likelihood * action_likelihoood

        # #5. Use country1 discounted reward and likelihood to calc expected utility
        newstate.expected_utility = newstate.schedule_likelihood * my_discountedreward

        # #Return!!
        return newstate

    #Calculates overall discounted reward for a state & country. Uses state quality function result of newstate, depth, and init_utility.
    #Formula: 
    def calc_discounted_reward(state: StateNode, country: str, depth: int)-> float:
        pass #TODO: implement, possibly in another file

    #Outputs [0, 1] likelihood of a country accepting a transaction based on discounted reward
    def calc_likelihood_from_reward(self, discounted_reward: float) -> float:
        pass #TODO: implement sigmoid generator, possibly in another file

