#Unit testing for state and state generation
import unittest
import copy
import sys
sys.path.append('../src')

import state as st
import actions as actions

class TestState(unittest.TestCase):
    def setUp(self) -> None:
        state = {'X1': {'water': 4, 'earth': 3, 'fire': 2},
                  'X2': {'water': 3, 'earth': 5, 'fire': 3},
                  'X3': {'water': 8, 'earth': 7, 'fire': 6}
                  }
        self.statenode = st.StateNode(state=state, schedule=[], schedule_likelihood=1, expected_utility=5)
        self.stategenerator = st.StateGenerator()
    def resetStateNode(self):
        self.statenode.state = {'X1': {'water': 4},
                  'X2': {'earth': 5},
                  'X3': {'fire': 6}
                  }
        self.statenode.schedule = []
        self.statenode.schedule_likelihood=1
        self.statenode.expected_utility = 5

    #Ensures ordering is done purely based on expected utility value
    def test_ordering(self):
        state2 = {'X1': {'water': 4, 'earth': 3, 'fire': 2},
                  'X2': {'water': 3, 'earth': 5, 'fire': 3},
                  'X3': {'water': 8, 'earth': 7, 'fire': 6}
                  }
        statenode2 = st.StateNode(state=state2, schedule=[], schedule_likelihood=1, expected_utility=6)
        self.assertTrue(statenode2 > self.statenode)
        statenode2.expected_utility = 5
        self.assertTrue(statenode2 == self.statenode)

    #Ensures that shallow copy produces a new statenode where edits to the new state and schedule do not affect that of the old
    def test_copy(self):
        statenode2 = copy.copy(self.statenode)
        statenode2.state['X1']['water'] = 8
        statenode2.schedule.append(5)
        statenode2.schedule_likelihood = .5
        statenode2.expected_utility = 10

        #Subtest - state
        self.assertTrue(self.statenode.state['X1']['water'] == 4)
        self.assertTrue(statenode2.state['X1']['water'] == 8)
        #Subtest - schedule
        self.assertTrue(len(self.statenode.schedule) == 0)
        self.assertTrue(len(statenode2.schedule) == 1)
        #Subtest - schedule likelihood
        self.assertTrue(self.statenode.schedule_likelihood == 1)
        self.assertTrue(statenode2.schedule_likelihood == .5)
        #Subtest - expected utility
        self.assertTrue(self.statenode.expected_utility == 5)
        self.assertTrue(statenode2.expected_utility == 10)

    #Call these at the beginning of action-state tests
    def createGoodBadTransforms(self) -> list[actions.ActionableTransform]:
        transformtemplate = actions.TransformTemplate(input_resources={'water': 6, 'earth': 6}, output_resources={'fire': 12})
        goodtransform = actions.ActionableTransform(template=transformtemplate, country='X3')
        badtransform = actions.ActionableTransform(template=transformtemplate, country='X1')
        return [goodtransform, badtransform]

    def createGoodBadTransfers(self) -> list[actions.ActionableTransfer]:
        transfertemplate = actions.TransferTemplate(resource1='water', resource1_amount=5, resource2='earth', resource2_amount=3)
        goodtransfer = actions.ActionableTransfer(template=transfertemplate, country1='X3', country2='X1')
        badtransfer = actions.ActionableTransfer(template=transfertemplate, country1='X1', country2='X3')
        return [goodtransfer, badtransfer]

    def test_isvalidtransform(self):
        [goodtransform, badtransform] = self.createGoodBadTransforms()
        self.assertTrue(self.stategenerator.isvalidtransformforstate(goodtransform, self.statenode, 1))
        self.assertFalse(self.stategenerator.isvalidtransformforstate(badtransform, self.statenode, 1))

    def test_isvalidtransfer(self):
        [goodtransfer, badtransfer] = self.createGoodBadTransfers()
        self.assertTrue(self.stategenerator.isvalidtransferforstate(goodtransfer, self.statenode, 1))
        self.assertFalse(self.stategenerator.isvalidtransferforstate(badtransfer, self.statenode, 1))

    def test_performtransform(self):
        pass
    def test_performtransfer(self):
        pass

if __name__ == '__main__':
    unittest.main()
