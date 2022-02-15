#Class to encapsulate all information needed to represent a 'state' node in our schedule optimization search.
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


class Action:
    def __init__(self):
        self.p = 'x'

#Just use to hold and get information about the state that needs to be memoized
@total_ordering
class State_Node:
    def __init__(self, state: dict, schedule: list[Action], schedule_likelihood: float, expected_utility: float):
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



