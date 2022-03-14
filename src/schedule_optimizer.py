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
        self.state_generator = state.StateGenerator(my_country=my_country, init_state=init_state, state_quality_function=state_quality_fn, k=likelihood_param, gamma=depth_penalty)

        #stuff needed to start optimizing
        init_statenode = state.StateNode(state=init_state, schedule=[], schedule_likelihood=1, expected_utility=0)
        self.best_states = DEPQ(maxlen=num_outputs)
        self.frontier = DEPQ(maxlen=max_frontier)
        self.frontier.insert(init_statenode, init_statenode.expected_utility)

    def findschedules(self) -> list: #list of schedules & utilities; i never made a data type for it (hehe)
        while len(self.frontier) > 0:
            #print('FRONTIERLEN: {}', str(len(self.frontier))) #debug
            curstatenode = self.frontier.popfirst()[0]
            #curstatenode.debug() #debug
            #save to best outputs if top n haven't been found, or if better than the worst so far
            if len(self.best_states) < self.num_outputs or curstatenode.expected_utility > self.best_states.low():
                self.best_states.insert(curstatenode, curstatenode.expected_utility)
            self.generatesuccessors(curstatenode) #implement

        #loop done; convert best_output states into schedules
        return self.extractschedulesfrombeststates()

    #really just adds directly to frontier (memory concerns) but I'll return them because ~clean code~
    def generatesuccessors(self, statenode: state.StateNode):
        #don't generate at depth level
        if len(statenode.schedule) >= self.max_depth:
            return
        self.generatesuccessorsfromlistofactions(statenode=statenode, actions=self.actionable_transforms)
        self.generatesuccessorsfromlistofactions(statenode=statenode, actions=self.actionable_transfers)
        #try every transform, and try to scale each up. Break out of the scaling loop if isValid is false
        # for transform in self.actionable_transforms:
        #     scalar = 1
        #
        #
        #     while self.state_generator.isvalidactionforstate(action=transform, statenode=statenode, scalar=scalar):
        #         #print(self.state_generator.isvalidactionforstate(action=transform, statenode=statenode, scalar=scalar))
        #         #idea: totally prune right here if state is not better than the worst of the frontier. saves tons of memory but may get stuck in small areas of search space
        #         newstate = self.state_generator.buildNewStateFromAction(transaction=transform, init_state=statenode, scalar=scalar)
        #         if (len(newstate.schedule) > 0):
        #             print('plz')
        #         if len(newstate.schedule) <= self.max_depth: #cut search at max depth
        #             self.frontier.insert(newstate, newstate.expected_utility)
        #             successors.append(newstate)
        #         else:
        #             del newstate
        #         scalar = scalar + 1

        # for transfer in self.actionable_transfers:
        #     scalar = 1
        #     while self.state_generator.isvalidactionforstate(action=transfer, statenode=statenode, scalar=scalar):
        #         #idea: totally prune right here if state is not better than the worst of the frontier. saves tons of memory but may get stuck in small areas of search space
        #         newstate = self.state_generator.performactiononstate(action=transfer, statenode=statenode, scalar=scalar)
        #         if len(newstate.schedule) <= self.max_depth:
        #             self.frontier.insert(newstate, newstate.expected_utility)
        #             successors.append(newstate)
        #         else:
        #             del newstate
        #         scalar = scalar + 1
        #TODO: ^extract above into a generalized function, so we can play around with frontier insertion


    def generatesuccessorsfromlistofactions(self, statenode: state.StateNode, actions: list[actions.Action]) -> list[actions]:
        successors = []  #TODO: rethink if this is necessary
        for action in actions:
            scalar = 1
            while self.state_generator.isvalidactionforstate(action=action, statenode=statenode, scalar=scalar):
                newstate = self.state_generator.buildNewStateFromAction(transaction=action, init_state=statenode,
                                                                        scalar=scalar)
                print('frontier len: ', str(len(self.frontier)))
                #newstate.debug() #debug
                if len(newstate.schedule) <= self.max_depth: #cut search at max depth
                    self.frontier.insert(newstate, newstate.expected_utility)
                    successors.append(newstate)  #TODO: rethink if this is necessary
                else:
                    del newstate
                scalar = scalar + 1
        return successors

    def extractschedulesfrombeststates(self) -> list:
        schedules = []
        for stateutilitypair in self.best_states:
            schedules.append((stateutilitypair[0].schedule, stateutilitypair[1]))

        return schedules







