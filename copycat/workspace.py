"""Workspace module."""


from . import formulas
from .bond import Bond
from .correspondence import Correspondence
from .letter import Letter
from .workspaceString import WorkspaceString


def __adjustUnhappiness(values):
    result = sum(values) / 2
    if result > 100.0:
        result = 100.0
    return result


class Workspace(object):
    def __init__(self, ctx):
        """To initialize the workspace."""
        self.ctx = ctx
        self.totalUnhappiness = 0.0
        self.intraStringUnhappiness = 0.0
        self.interStringUnhappiness = 0.0

        # LSaldyt: default initializations for GUI entry
        self.targetString = ''
        self.initialString = ''
        self.modifiedString = ''
        self.finalAnswer = None
        self.changedObject = None
        self.objects = []
        self.structures = []
        self.rule = None

    def __repr__(self):
        return '<Workspace trying %s:%s::%s:?>' % (
            self.initialString, self.modifiedString, self.targetString,
        )

    def resetWithStrings(self, initial, modified, target):
        self.targetString = target
        self.initialString = initial
        self.modifiedString = modified
        self.reset()

    def reset(self):
        self.finalAnswer = None
        self.changedObject = None
        self.objects = []
        self.structures = []
        self.rule = None # Only one rule? : LSaldyt
        self.initial = WorkspaceString(self.ctx, self.initialString)
        self.modified = WorkspaceString(self.ctx, self.modifiedString)
        self.target = WorkspaceString(self.ctx, self.targetString)

    '''
    # TODO: Initial part of refactoring in this method
    def getAssessedUnhappiness(self, unhappiness):
        o.Unhappiness = __adjustUnhappiness(
            o.relativeImportance * o.Unhappiness
            for o in self.objects)
        pass
    '''

    # TODO: Extract method?
    def assessUnhappiness(self):
        self.intraStringUnhappiness = __adjustUnhappiness(
            o.relativeImportance * o.intraStringUnhappiness
            for o in self.objects)
        self.interStringUnhappiness = __adjustUnhappiness(
            o.relativeImportance * o.interStringUnhappiness
            for o in self.objects)
        self.totalUnhappiness = __adjustUnhappiness(
            o.relativeImportance * o.totalUnhappiness
            for o in self.objects)

    # TODO: these 3 methods seem to be the same... are they?  If so, Extract method.
    def calculateIntraStringUnhappiness(self):
        value = sum(
            o.relativeImportance * o.intraStringUnhappiness
            for o in self.objects
        ) / 2.0
        self.intraStringUnhappiness = min(value, 100.0)

    def calculateInterStringUnhappiness(self):
        value = sum(
            o.relativeImportance * o.interStringUnhappiness
            for o in self.objects
        ) / 2.0
        self.interStringUnhappiness = min(value, 100.0)

    def calculateTotalUnhappiness(self):
        value = sum(
            o.relativeImportance * o.totalUnhappiness
            for o in self.objects
        ) / 2.0
        self.totalUnhappiness = min(value, 100.0)

    def updateEverything(self):
        for structure in self.structures:
            structure.updateStrength()
        for obj in self.objects:
            obj.updateValue()
        self.initial.updateRelativeImportance()
        self.target.updateRelativeImportance()
        self.initial.updateIntraStringUnhappiness()
        self.target.updateIntraStringUnhappiness()

    # TODO: use entropy
    def getUpdatedTemperature(self):
        '''
        Calculation of global tolerance towards irrelevance
        '''
        self.calculateIntraStringUnhappiness()
        self.calculateInterStringUnhappiness()
        self.calculateTotalUnhappiness()
        if self.rule:
            self.rule.updateStrength()
            ruleWeakness = 100.0 - self.rule.totalStrength
        else:
            ruleWeakness = 100.0
        return formulas.weighted_average((
            (self.totalUnhappiness, 0.8),
            (ruleWeakness, 0.2)
        ))

    def numberOfUnrelatedObjects(self):
        """Computes the number of all objects in the workspace with >= 1 open bond slots."""
        objects = [o for o in self.objects
                   if o.string == self.initial or o.string == self.target]
        objects = [o for o in objects if not o.spansString()]
        objects = [o for o in objects
                   if (not o.leftBond and not o.leftmost) or
                   (not o.rightBond and not o.rightmost)]
        return len(objects)

    def numberOfUngroupedObjects(self):
        """A list of all objects in the workspace that have no group."""
        objects = [o for o in self.objects if
                   o.string == self.initial or o.string == self.target]
        objects = [o for o in objects if not o.spansString()]
        objects = [o for o in objects if not o.group]
        return len(objects)

    def numberOfUnreplacedObjects(self):
        """A list of all unreplaced objects in the initial string."""
        objects = [o for o in self.objects
                   if o.string == self.initial and isinstance(o, Letter)]
        objects = [o for o in objects if not o.replacement]
        return len(objects)

    def numberOfUncorrespondingObjects(self):
        """A list of all uncorresponded objects in the initial string."""
        objects = [o for o in self.objects
                   if o.string == self.initial or o.string == self.target]
        objects = [o for o in objects if not o.correspondence]
        return len(objects)

    def numberOfBonds(self):
        """The number of bonds in the workspace."""
        return sum(1 for o in self.structures if isinstance(o, Bond))

    def correspondences(self):
        return [s for s in self.structures if isinstance(s, Correspondence)]

    def slippages(self):
        result = []
        if self.changedObject and self.changedObject.correspondence:
            result += self.changedObject.correspondence.conceptMappings
        for o in self.initial.objects:
            if o.correspondence:
                for mapping in o.correspondence.slippages():
                    if not mapping.isNearlyContainedBy(result):
                        result += [mapping]
        return result

    def buildRule(self, rule):
        if self.rule is not None:
            self.structures.remove(self.rule)
        self.rule = rule
        self.structures += [rule]
        rule.activateRuleDescriptions()

    def breakRule(self):
        if self.rule is not None:
            self.structures.remove(self.rule)
        self.rule = None

    def buildDescriptions(self, objekt):
        for description in objekt.descriptions:
            description.descriptionType.buffer = 100.0
            description.descriptor.buffer = 100.0
            if description not in self.structures:
                self.structures += [description]
