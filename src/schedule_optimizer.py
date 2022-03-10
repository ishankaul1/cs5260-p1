import actions
import state
from depq import DEPQ

class Schedule_Optimizer:
    #requirements: init_state, actionable_transforms, actionable_transfers, state_quality_func, my_country, max_depth, max_frontier, num_outputs
    def __init__(self, init_state: dict, actionable_transforms: list[actions.ActionableTransform], actionable_transfers: list[actions.ActionableTransfer], state_quality_fn, my_country: str, max_depth: int, max_frontier: int, num_outputs: int, depth_penalty: float, likelihood_param: float ):
        self.init_state = init_state
        self.actionable_transforms = actionable_transforms
        self.actionable_transfers = actionable_transfers
        self.state_quality_fn = state_quality_fn
        self.my_country = my_country
        self.max_depth = max_depth
        self.max_frontier = max_frontier
        self.num_outputs = num_outputs
        self.state_generator = state.StateGenerator(my_country=my_country, init_state=init_state, k=likelihood_param, gamma=depth_penalty)

        #stuff needed to start optimizing
        init_statenode = state.StateNode(state=init_state, schedule=[], schedule_likelihood=1, expected_utility=0)
        self.best_states = DEPQ(maxlen=num_outputs)
        self.frontier = DEPQ(maxlen=max_frontier)
        self.frontier.insert(init_statenode, init_statenode.expected_utility)

    def findschedules(self) -> list: #list of schedules & utilities; i never made a data type for it (hehe)
        while len(self.frontier) > 0:
            curstatenode = self.frontier.popfirst()[0]
            #save to best outputs if top n haven't been found, or if better than the worst so far
            if len(self.best_states) < self.num_outputs or curstatenode.expected_utility > self.best_outputs.low():
                self.best_states.insert(curstatenode, curstatenode.expected_utility)
            self.generatesuccessors(curstatenode) #implement

        #loop done; convert best_output states into schedules
        return self.convertbeststatestoschedules()

    #really just adds directly to frontier (memory concerns) but I'll return them because ~clean code~
    def generatesuccessors(self, statenode: state.StateNode) -> list[state.StateNode]:
        #TODO
        pass

    def convertbeststatestoschedules(self) -> list:
        schedules = []
        for stateutilitypair in self.best_states:
            schedules.append((stateutilitypair[0].schedule, stateutilitypair[1])) #so digusting, I know

        return schedules







