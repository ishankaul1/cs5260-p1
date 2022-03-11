#really just prints our solutions in a helper func
import actions

def printScheduleUtilityPair(schedule: list[actions.PersistableAction], utility: float):
    print('SCHEDULE')
    print('--------')
    print('\tExpected Utility: {}', str(utility))
    print('\tActions:')
    for action in schedule:
        print(action.toString())
    print()

def printAllResults(results: list):
    for r in results:
        printScheduleUtilityPair(r)