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


#Just use to hold and get information about the state that needs to be memoized
@total_ordering
class State_Node:
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
        return State_Node(state=copy.deepcopy(self.state), schedule=copy.copy(self.schedule), schedule_likelihood=self.schedule_likelihood, expected_utility=self.expected_utility)

#All functionality for creating a new state node from a state and transaction
#Is a static, one-use object
class State_Generator:
    #TODO: Initialize with an init_state dict (initial state of the resources) AND a state quality function.
    #These will be used globally for calculations at all levels.



    #Takes in an initial state and 
    #TODO: simplify this logic. 
    def buildStateFromTransform(init_state: State_Node, transaction: actions.Action, scalar: int) -> State_Node:
        #Test out copy.copy instead of this
        newState = State_Node(state=copy.deepcopy(init_state.state), schedule= copy.copy(init_state.schedule), schedule_likelihood=init_state.schedule_likelihood, expected_utility=init_state.expected_utility )
        
        #check if valid first
        if isinstance(transaction, actions.Actionable_Transfer):

            #perform action on new state
            #transaction.perform(stateNode=newState, scalar=scalar)

            #persist action persistable on schedule
            persistable = transaction.convertToPersistable(scalar=scalar)
            newState.schedule.append(persistable)
            #calculate the likelihood of the new transaction, based on the discounted reward  of country2 put into sigmoid function
            transaction_likelihood  = .9 # should be sigmoid(discounted_reward(newState, country=transaction.country2, self.?initReward[country2], self.statequalfunc? ))
            #can multiply of sigmoid of country 1 as well, if it's not my_country!!!
            #use new transactio likelihood to set state likelihood
            newState.schedule_likelihood = newState.schedule_likelihood * transaction_likelihood

            #calculate expected utility, using country1 discounted reward and schedule likelihood
            newState.expected_utility = newState.expected_utility #should use current likelihood value * discounted_reward(newState, country=MY_COUNTRY,  self.initReward[my_country], self.statequalFunc)
            
            #return the new state
        if isinstance(transaction, actions.Actionable_Transform):

            #perform action on new state
            #transaction.perform(stateNode=newState, scalar=scalar)

            #persist action on schedule
            persistable = transaction.convertToPersistable(scalar=scalar)

            newState.schedule.append(persistable)

            #likelihood of transform is always 1; don't need to change schedule likelihood

            newState.expected_utility = newState.expected_utility #should use current likelihood value * discounted_reward(newState, country=MY_COUNTRY,  self.initReward[my_country], self.statequalFunc)

    #Calculates overall discounted reward for a state & country. Needs state quality function and init reward passed in.
    #Formula: 
    def calc_discounted_reward(state: State_Node, country: str):
        pass


def test_stateCopy():
    state1 = {'X1': {'poo': 4},
        'X2': {'pee': 5}, 
        'X3': {'fart': 6}
    }

    stateNode1 = State_Node(state=state1, schedule=[], schedule_likelihood=1, expected_utility=5)

    stateNode2 = copy.copy(stateNode1)

    stateNode2.state['X1']['poo'] = 12
    stateNode2.schedule.append(5)
    stateNode2.schedule_likelihood = .5
    stateNode2.expected_utility = 10

    print("DICT:\n------")
    print("\tS1:")
    print(stateNode1.state)
    print("\tS2:")
    print(stateNode2.state)

    print("SCHEDULE:\n------")
    print("\tS1:")
    print(stateNode1.schedule)
    print("\tS2:")
    print(stateNode2.schedule)

    print("LIKELIHOOD:\n------")
    print("\tS1:")
    print(stateNode1.schedule_likelihood)
    print("\tS2:")
    print(stateNode2.schedule_likelihood)

    print("UTIL:\n------")
    print("\tS1:")
    print(stateNode1.expected_utility)
    print("\tS2:")
    print(stateNode2.expected_utility)


test_stateCopy()