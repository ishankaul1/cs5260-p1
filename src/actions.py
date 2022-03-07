from abc import ABC, abstractmethod


#list of these should be read in from input file or defined at start of serach
class TransformTemplate:
    def __init__(self, input_resources: dict, output_resources: dict):
        self.input_resources = input_resources #form; {resource: value}
        self.output_resources = output_resources #form: {resource: value}

#all possible transfer ratios should be determined based on the resources file
class TransferTemplate:
    def __init__(self, resource1, resource1_amount, resource2, resource2_amount):
        self.resource1 = resource1
        self.resource1_amount = resource1_amount
        self.resource2 = resource2
        self.resource2_amount = resource2_amount

#base class for actions
class Action(ABC):
    def __init__(self, template):
        self.template = template

    def convertToPersistable(self, scalar: int):
        pass

class PersistableAction(ABC):
    #just print out what's happening
    @abstractmethod
    def debug(self):
        pass



#These are actually to be stored in the schedule for a new state, after successfully performing the action template and scalar on the state
class PersistableTransform(PersistableAction):
    #resources in {}
    def __init__(self, template: TransformTemplate,  country: str):
        self.template = template
        self.country = country
        
    def debug(self):
        print("TRANSFORM: ")
        print("\tCountry: " + self.country)
        print("\tInput: {"  + ','.join([resource + ': ' + str(self.template.input_resources[resource]) for resource in self.template.input_resources]) + "}" )
        print("\tOutput: {"  + ','.join([resource + ': ' + str(self.template.output_resources[resource]) for resource in self.template.output_resources]) + "}\n" )

    def toString(self) -> str:
        format_str = "TRANSFORM:\n\tCountry: {}\n\tInput: [{}]\n\tOutput: [{}]\n"
        return format_str.format(self.country, ','.join([resource + ': ' + str(self.template.input_resources[resource]) for resource in self.template.input_resources]), ','.join([resource + ': ' + str(self.template.output_resources[resource]) for resource in self.template.output_resources]) )

class PersistableTransfer(PersistableAction):
    def __init__(self, template: TransferTemplate, country1: str, country2: str):
        self.template = template
        self.country1 = country1
        self.country2 = country2

    def debug(self):
        print("TRANSFER:")
        print("\tCountry1: " + self.country1)
        print("\tResource1: {" + self.template.resource1 + ": " + str(self.template.resource1_amount) + "}")
        print("\tCountry2: " + self.country2)
        print("\tResource2: {" + self.template.resource2 + ": " + str(self.template.resource2_amount) + "}\n")

    def toString(self) -> str:
        format_str = "TRANSFER:\n\tCountry1: {}, Resource1: {}, Amount1: {}\n\tCountry2: {}, Resource2: {}, Amount2: {}\n"
        return format_str.format(self.country1, self.template.resource1, self.template.resource1_amount, self.country2, self.template.resource2, self.template.resource2_amount)



#These are created at the very start of the program, one for each transform template. These are to be used to determine whether a transform is possible on a state, and to actually make the transform on the state.
class ActionableTransform(Action):
    def __init__(self, template: TransformTemplate, country: str):
        # self.transform_template = transform_template
        super().__init__(template=template)
        self.country = country

    def convertToPersistable(self, scalar: int):
        newinputresources = {}
        newoutputresources = {}
        for resource in self.template.input_resources:
            newinputresources[resource] = self.template.input_resources[resource] * scalar
        for resource in self.template.output_resources:
            newoutputresources[resource] = self.template.output_resources[resource] * scalar
        return PersistableTransform(template=TransformTemplate(input_resources=newinputresources, output_resources=newoutputresources), country=self.country)

#These are created at the very start of the program, one for each transfer template * country (country1 is always your own country). These are to be used to determine whether a transfer is possible on a state, and to actually make the transfer on the state.
class ActionableTransfer(Action):
    def __init__(self, template: TransferTemplate, country1: str, country2: str):
        super().__init__(template=template)
        self.country1 = country1
        self.country2 = country2
        
    def convertToPersistable(self, scalar: int) -> PersistableTransfer:
        return PersistableTransfer(TransferTemplate(self.template.resource1, self.template.resource1_amount * scalar, self.template.resource2, self.template.resource2_amount * scalar), self.country1, self.country2)
