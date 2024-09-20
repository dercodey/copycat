"""Workspace module.

This module defines the `Workspace` class and associated functions for managing and 
assessing the state of a workspace in the context of the Copycat project. The workspace 
tracks various strings, objects, and structures, and provides methods to calculate 
unhappiness metrics, update object states, and manage rules and descriptions.

Classes:
    Workspace: Represents the workspace, containing methods to manage strings, objects, 
               structures, and calculate various metrics.

Functions:
    __adjust_unhappiness(values: Iterable[float]) -> float: Adjusts the unhappiness value 
                                                           based on the provided iterable 
                                                           of float values.
"""

from typing import Any, Iterable, List, Optional
from . import formulas
from .bond import Bond
from .correspondence import Correspondence
from .letter import Letter
from .workspace_string import WorkspaceString


def __adjust_unhappiness(values: Iterable[float]) -> float:
    """
    Adjusts the unhappiness value based on the provided iterable of float values.

    This function calculates the sum of the provided values, divides the sum by 2,
    and ensures that the result does not exceed 100.0.

    Args:
        values (Iterable[float]): An iterable of float values representing unhappiness metrics.

    Returns:
        float: The adjusted unhappiness value, capped at a maximum of 100.0.
    """
    result = sum(values) / 2
    if result > 100.0:
        result = 100.0
    return result


class Workspace(object):
    """
    Workspace class represents the environment in which the Copycat algorithm operates.
    It maintains the state of the strings being analyzed and manipulated, as well as the
    various objects and structures within those strings.

    Attributes:
        ctx (Copycat): The Copycat context.
        total_unhappiness (float): The total unhappiness score.
        intra_string_unhappiness (float): The intra-string unhappiness score.
        inter_string_unhappiness (float): The inter-string unhappiness score.
        target_string (str): The target string.
        initial_string (str): The initial string.
        modified_string (str): The modified string.
        final_answer (Optional[Any]): The final answer.
        changed_object (Optional[Any]): The object that has changed.
        objects (List[Any]): The list of objects in the workspace.
        structures (List[Any]): The list of structures in the workspace.
        rule (Optional[Any]): The rule being applied.

    Methods:
        __init__(ctx: "Copycat"): Initializes the workspace with the given context.
        __repr__(): Returns a string representation of the workspace.
        reset_with_strings(initial, modified, target): Resets the workspace with the given strings.
        reset(): Resets the workspace to its initial state.
        assess_unhappiness(): Assesses the unhappiness scores.
        calculate_intra_string_unhappiness(): Calculates the intra-string unhappiness score.
        calculate_inter_string_unhappiness(): Calculates the inter-string unhappiness score.
        calculate_total_unhappiness(): Calculates the total unhappiness score.
        update_everything(): Updates all objects and structures in the workspace.
        get_updated_temperature(): Calculates the global tolerance towards irrelevance.
        number_of_unrelated_objects(): Computes the number of objects with open bond slots.
        number_of_ungrouped_objects(): Computes the number of ungrouped objects.
        number_of_unreplaced_objects(): Computes the number of unreplaced objects in the initial
            string.
        number_of_uncorresponding_objects(): Computes the number of uncorresponded objects in the
            initial string.
        number_of_bonds(): Computes the number of bonds in the workspace.
        correspondences(): Returns a list of correspondences in the workspace.
        slippages(): Returns a list of slippages in the workspace.
        build_rule(rule): Builds and activates a rule in the workspace.
        break_rule(): Breaks the current rule in the workspace.
        build_descriptions(objekt): Builds descriptions for the given object.
    """

    ctx: "Copycat"  # type: ignore  # noqa: F821
    total_unhappiness: float
    intra_string_unhappiness: float
    inter_string_unhappiness: float

    target_string: str
    initial_string: str
    modified_string: str
    final_answer: Optional[Any]
    changed_object: Optional[Any]
    objects: List[Any]
    structures: List[Any]
    rule: Optional[Any]

    initial: Optional[WorkspaceString] = None
    modified: Optional[WorkspaceString] = None
    target: Optional[WorkspaceString] = None

    def __init__(self, ctx: "Copycat"):  # type: ignore  # noqa: F821
        """To initialize the workspace."""
        self.ctx = ctx
        self.total_unhappiness = 0.0
        self.intra_string_unhappiness = 0.0
        self.inter_string_unhappiness = 0.0

        # LSaldyt: default initializations for GUI entry
        self.target_string = ""
        self.initial_string = ""
        self.modified_string = ""
        self.final_answer = None
        self.changed_object = None
        self.objects = []
        self.structures = []
        self.rule = None

    def __repr__(self) -> str:
        return (
            f"<Workspace trying {self.initial_string}:{self.modified_string}"
            + f"::{self.target_string}:?>"
        )

    def reset_with_strings(self, initial: str, modified: str, target: str) -> None:
        """
        Resets the workspace with the provided initial, modified, and target strings.

        Args:
            initial (str): The initial string to set.
            modified (str): The modified string to set.
            target (str): The target string to set.

        Returns:
            None
        """
        self.target_string = target
        self.initial_string = initial
        self.modified_string = modified
        self.reset()

    def reset(self) -> None:
        """
        Resets the workspace to its initial state.

        This method clears the final answer, changed object, objects list,
        structures list, and rule. It also reinitializes the initial, modified,
        and target workspace strings.
        """
        self.final_answer = None
        self.changed_object = None
        self.objects = []
        self.structures = []
        self.rule = None  # Only one rule? : LSaldyt
        self.initial = WorkspaceString(self.ctx, self.initial_string)
        self.modified = WorkspaceString(self.ctx, self.modified_string)
        self.target = WorkspaceString(self.ctx, self.target_string)

    # TODO: Extract method?
    def assess_unhappiness(self) -> None:
        """
        Assess and update the unhappiness metrics for the objects in the workspace.

        This method calculates three types of unhappiness:
        - Intra-string unhappiness
        - Inter-string unhappiness
        - Total unhappiness

        Each type of unhappiness is adjusted based on the relative importance of each object.

        Attributes:
            intra_string_unhappiness (float): Adjusted intra-string unhappiness.
            inter_string_unhappiness (float): Adjusted inter-string unhappiness.
            total_unhappiness (float): Adjusted total unhappiness.
        """
        self.intra_string_unhappiness = __adjust_unhappiness(
            objekt.relativeImportance * objekt.intraStringUnhappiness
            for objekt in self.objects
        )
        self.inter_string_unhappiness = __adjust_unhappiness(
            objekt.relativeImportance * objekt.interStringUnhappiness
            for objekt in self.objects
        )
        self.total_unhappiness = __adjust_unhappiness(
            objekt.relativeImportance * objekt.totalUnhappiness
            for objekt in self.objects
        )

    # TODO: these 3 methods seem to be the same... are they?  If so, Extract method.
    def calculate_intra_string_unhappiness(self) -> None:
        """
        Calculate and update the intra-string unhappiness for the current object.

        This method computes the intra-string unhappiness by summing the product
        of `relativeImportance` and `intraStringUnhappiness` for each object in
        `self.objects`, then dividing the result by 2.0. The computed value is
        then assigned to `self.intra_string_unhappiness`, ensuring it does not
        exceed 100.0.

        Returns:
            None
        """
        value = (
            sum(
                objekt.relativeImportance * objekt.intraStringUnhappiness
                for objekt in self.objects
            )
            / 2.0
        )
        self.intra_string_unhappiness = min(value, 100.0)

    def calculate_inter_string_unhappiness(self) -> None:
        """
        Calculates the inter-string unhappiness for the objects in the workspace.

        This method computes the inter-string unhappiness by summing the product
        of `relativeImportance` and `interStringUnhappiness` for each object in
        `self.objects`, then dividing the sum by 2.0. The result is assigned to
        `self.inter_string_unhappiness`, capped at a maximum value of 100.0.

        Returns:
            None
        """
        value = (
            sum(
                objekt.relativeImportance * objekt.interStringUnhappiness
                for objekt in self.objects
            )
            / 2.0
        )
        self.inter_string_unhappiness = min(value, 100.0)

    def calculate_total_unhappiness(self) -> None:
        """
        Calculate the total unhappiness for all objects and update the total_unhappiness attribute.

        The total unhappiness is computed as the sum of the product of each object's
        relative importance and total unhappiness, divided by 2. The result is then
        capped at a maximum value of 100.0.

        Returns:
            None
        """
        value = (
            sum(
                objekt.relativeImportance * objekt.totalUnhappiness
                for objekt in self.objects
            )
            / 2.0
        )
        self.total_unhappiness = min(value, 100.0)

    def update_everything(self) -> None:
        """
        Updates various attributes of the structures and objects within the workspace.

        This method performs the following updates:
        1. Calls `updateStrength` on each structure in `self.structures`.
        2. Calls `updateValue` on each object in `self.objects`.
        3. If `self.initial` is not None, calls `updateRelativeImportance` and
            `updateIntraStringUnhappiness` on it.
        4. If `self.target` is not None, calls `updateRelativeImportance` and
            `updateIntraStringUnhappiness` on it.
        """
        for structure in self.structures:
            structure.update_strength()
        for obj in self.objects:
            obj.updateValue()
        if self.initial is not None:
            self.initial.update_relative_importance()
        if self.target is not None:
            self.target.update_relative_importance()
        if self.initial is not None:
            self.initial.update_intra_string_unhappiness()
        if self.target is not None:
            self.target.update_intra_string_unhappiness()

    # TODO: use entropy
    def get_updated_temperature(self) -> float:
        """
        Calculation of global tolerance towards irrelevance.

        Calculates the updated temperature based on intra-string unhappiness,
        inter-string unhappiness, and the strength of a rule if it exists.

        The temperature is a weighted average of the total unhappiness and the
        rule's weakness. The weights are 0.8 for total unhappiness and 0.2 for
        rule weakness.

        Returns:
            float: The updated temperature.
        """
        self.calculate_intra_string_unhappiness()
        self.calculate_inter_string_unhappiness()
        self.calculate_total_unhappiness()
        if self.rule:
            self.rule.update_strength()
            rule_weakness = 100.0 - self.rule.total_strength
        else:
            rule_weakness = 100.0
        return formulas.weighted_average(
            ((self.total_unhappiness, 0.8), (rule_weakness, 0.2))
        )

    def number_of_unrelated_objects(self) -> int:
        """
        Computes the number of all objects in the workspace with >= 1 open bond slots.

        Computes the number of objects in the workspace that have at least one open bond slot.

        An object is considered if it belongs to either the initial or target string, does not
        span the entire string, and has at least one open bond slot on either the left or right
        side, unless it is the leftmost or rightmost object.

        Returns:
            int: The number of objects with at least one open bond slot.
        """
        objects = [
            objekt
            for objekt in self.objects
            if objekt.string == self.initial or objekt.string == self.target
        ]
        objects = [objekt for objekt in objects if not objekt.spansString()]
        objects = [
            objekt
            for objekt in objects
            if (not objekt.leftBond and not objekt.leftmost)
            or (not objekt.rightBond and not objekt.rightmost)
        ]
        return len(objects)

    def number_of_ungrouped_objects(self) -> int:
        """
        A list of all objects in the workspace that have no group.

        Calculate the number of objects in the workspace that are not part of any group.

        This method filters the objects in the workspace based on the following criteria:
        1. The object's string attribute matches either the initial or target string.
        2. The object does not span a string.
        3. The object is not part of any group.

        Returns:
            int: The number of ungrouped objects in the workspace.
        """
        objects = [
            objekt
            for objekt in self.objects
            if objekt.string == self.initial or objekt.string == self.target
        ]
        objects = [o for o in objects if not o.spansString()]
        objects = [o for o in objects if not o.group]
        return len(objects)

    def number_of_unreplaced_objects(self) -> int:
        """A list of all unreplaced objects in the initial string.

        Calculate the number of unreplaced objects in the initial string.

        This method filters the objects in the `self.objects` list to find those
        that match the initial string and are instances of the `Letter` class.
        It then further filters these objects to include only those that do not
        have a replacement.

        Returns:
            int: The number of unreplaced objects in the initial string.
        """
        objects = [
            objekt
            for objekt in self.objects
            if objekt.string == self.initial and isinstance(objekt, Letter)
        ]
        objects = [o for o in objects if not o.replacement]
        return len(objects)

    def number_of_uncorresponding_objects(self) -> int:
        """A list of all uncorresponded objects in the initial string.

        Calculate the number of objects that do not have a correspondence in the initial string.

        This method filters the objects associated with either the initial or target string
        and counts how many of these objects do not have a correspondence.

        Returns:
            int: The number of uncorresponded objects in the initial string.
        """
        objects = [
            objekt
            for objekt in self.objects
            if objekt.string == self.initial or objekt.string == self.target
        ]
        objects = [objekt for objekt in objects if not objekt.correspondence]
        return len(objects)

    def number_of_bonds(self) -> int:
        """The number of bonds in the workspace.

        Calculate the number of bonds in the workspace.

        Returns:
            int: The total number of Bond instances in the workspace's structures.
        """
        return sum(1 for structure in self.structures if isinstance(structure, Bond))

    def correspondences(self) -> List["WorkspaceStructure"]:  # type: ignore  # noqa: F821
        """
        Retrieve a list of structures that are instances of the Correspondence class.

        Returns:
            List[WorkspaceStructure]: A list of structures that are instances of the
                Correspondence class.
        """
        return [
            structure
            for structure in self.structures
            if isinstance(structure, Correspondence)
        ]

    def slippages(self) -> List["ConceptMapping"]:  # type: ignore  # noqa: F821
        """
        Computes and returns a list of ConceptMapping objects representing the slippages.

        Slippages are derived from the changed_object's correspondence and the initial objects'
        correspondences. If the changed_object has a correspondence, its concept mappings are
        added to the result. For each initial object with a correspondence, its slippages are
        computed and added to the result if they are not nearly contained by the current result.

        Returns:
            List[ConceptMapping]: A list of ConceptMapping objects representing the slippages.
        """
        result: List["ConceptMapping"] = []  # type: ignore  # noqa: F821
        if self.changed_object and self.changed_object.correspondence:
            result += self.changed_object.correspondence.conceptMappings
        if self.initial is not None:
            for objekt in self.initial.objects:
                if objekt.correspondence:
                    for mapping in objekt.correspondence.slippages():
                        if not mapping.isNearlyContainedBy(result):
                            result += [mapping]
        return result

    def build_rule(self, rule: "Rule") -> None:  # type: ignore  # noqa: F821
        """
        Replaces the current rule with a new one and updates the structures list.

        Args:
            rule (Rule): The new rule to be set and activated.

        Returns:
            None
        """
        if self.rule is not None:
            self.structures.remove(self.rule)
        self.rule = rule
        self.structures += [rule]
        rule.activateRuleDescriptions()

    def break_rule(self) -> None:
        """
        Breaks the current rule by removing it from the structures list and setting it to None.

        This method checks if there is an existing rule. If a rule exists, it removes the rule
        from the structures list and then sets the rule attribute to None.
        """
        if self.rule is not None:
            self.structures.remove(self.rule)
        self.rule = None

    def build_descriptions(self, objekt: "WorkspaceObject") -> None:  # type: ignore  # noqa: F821
        """
        Updates the buffer values of descriptions in the given WorkspaceObject and adds them to
            the structures list if not already present.

        Args:
            objekt (WorkspaceObject): The object containing descriptions to be processed.

        Returns:
            None
        """
        for description in objekt.descriptions:
            description.descriptionType.buffer = 100.0
            description.descriptor.buffer = 100.0
            if description not in self.structures:
                self.structures += [description]
