from typing import Callable, List, Tuple, Iterable
from .conceptMapping import ConceptMapping


def weighted_average(values: Iterable[Tuple[float, float]]) -> float:
    """
    Calculates the weighted average of a list of values.

    Args:
        values (Iterable[Tuple[float, float]]): An iterable of tuples where each tuple contains
            a value and its corresponding weight.

    Returns:
        float: The weighted average of the values.
    """
    total = 0.0
    total_weights = 0.0
    for value, weight in values:
        total += value * weight
        total_weights += weight
    if not total_weights:
        return 0.0
    return total / total_weights


def __local_relevance(
    string: "WorkspaceString",  # type: ignore  # noqa: F821
    is_relevant: Callable[["WorkspaceObject"], bool],  # type: ignore  # noqa: F821
):
    """
    Calculates the local relevance of objects in a string based on a relevance function.

    Args:
        string (WorkspaceString): The string containing the objects.
        is_relevant (Callable[["WorkspaceObject"], bool]): A function that determines
            if an object is relevant.

    Returns:
        float: The local relevance score.
    """
    number_of_objects_not_spanning: int = 0
    number_of_matches: int = 0
    for o in string.objects:
        if not o.spansString():
            number_of_objects_not_spanning += 1
            if is_relevant(o):
                number_of_matches += 1
    if number_of_objects_not_spanning == 1:
        return 100.0 * number_of_matches
    return 100.0 * number_of_matches / (number_of_objects_not_spanning - 1.0)


def local_bond_category_relevance(
    string: "WorkspaceString",  # type: ignore  # noqa: F821
    category: "Slipnode",  # type: ignore  # noqa: F821
):
    """
    Calculates the relevance of local bond categories within a given workspace string.

    Parameters:
        string (WorkspaceString): The workspace string containing objects to evaluate.
        category (str): The category of the bond to check for relevance.

    Returns:
        float: A relevance score, where a score of 0.0 indicates no relevance.

    Notes:
        If the workspace string contains only one object, the function will return 0.0.
    """

    def is_relevant(o: "WorkspaceObject") -> bool:  # type: ignore  # noqa: F821
        return o.rightBond and o.rightBond.category == category

    if len(string.objects) == 1:
        return 0.0
    return __local_relevance(string, is_relevant)


def local_direction_category_relevance(
    string: "WorkspaceString",  # type: ignore  # noqa: F821
    direction: "Slipnode",  # type: ignore  # noqa: F821
):
    """
    Determines the relevance of local direction categories within a given workspace string.

    Args:
        string (WorkspaceString): The workspace string to analyze.
        direction (str): The direction category to check for relevance.

    Returns:
        Relevance score or a relevant subset based on the specified direction category.
    """

    def is_relevant(o):
        return o.rightBond and o.rightBond.directionCategory == direction

    return __local_relevance(string, is_relevant)


def get_mappings(
    object_from_initial: "WorkspaceObject",  # type: ignore  # noqa: F821
    object_from_target: "WorkspaceObject",  # type: ignore  # noqa: F821
    initial_descriptions: List["Description"],  # type: ignore  # noqa: F821
    target_descriptions: List["Description"],  # type: ignore  # noqa: F821
):
    """
    Generates a list of mappings between initial and target descriptions based on their types
    and descriptors.

    Args:
        object_from_initial (WorkspaceObject): The initial workspace object.
        object_from_target (WorkspaceObject): The target workspace object.
        initial_descriptions (List[Description]): A list of descriptions from the initial workspace.
        target_descriptions (List[Description]): A list of descriptions from the target workspace.

    Returns:
        List[ConceptMapping]: A list of ConceptMapping objects that represent the mappings between
        the initial and target descriptions.
    """

    mappings: List[ConceptMapping] = []
    for initial in initial_descriptions:
        for target in target_descriptions:
            if initial.descriptionType == target.descriptionType:
                if (
                    initial.descriptor == target.descriptor
                    or initial.descriptor.slip_linked(target.descriptor)
                ):
                    mapping = ConceptMapping(
                        initial.descriptionType,
                        target.descriptionType,
                        initial.descriptor,
                        target.descriptor,
                        object_from_initial,
                        object_from_target,
                    )
                    mappings += [mapping]
    return mappings
