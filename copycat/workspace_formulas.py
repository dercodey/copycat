"""
This module provides functions for selecting WorkspaceObject instances from a list based on 
    specified attributes and weighted random choices.

Functions:
    __choose_object_from_list(
        ctx, objects: List[WorkspaceObject], attribute: str
    ) -> WorkspaceObject:
        Selects an object from a list of WorkspaceObject instances based on a specified 
            attribute and a weighted random choice.

    choose_unmodified_object(
        ctx, attribute: str, in_objects: List[WorkspaceObject]
    ) -> WorkspaceObject:

    choose_neighbor(ctx, source: WorkspaceObject) -> WorkspaceObject:
        Chooses a neighboring WorkspaceObject based on proximity to a source object.

    chooseDirectedNeighbor(ctx, source: WorkspaceObject, direction):
        Chooses a directed neighboring WorkspaceObject based on the specified direction 
            relative to the source object.
"""

from typing import List

from .slipnode import Slipnode
from .workspace_object import WorkspaceObject


def __choose_object_from_list(
    ctx, objects: List[WorkspaceObject], attribute: str
) -> WorkspaceObject:
    """
    Selects an object from a list of WorkspaceObject instances based on a specified attribute and a
        weighted random choice.

    Parameters:
        ctx: The context containing random and temperature attributes.
        objects (List[WorkspaceObject]): A list of WorkspaceObject instances to choose from.
        attribute (str): The attribute of the WorkspaceObject to be used for weighting the
            selection.

    Returns:
        WorkspaceObject: A randomly selected WorkspaceObject from the list, weighted by the
            specified attribute.
    """
    # TODO: use entropy
    random = ctx.random
    temperature = ctx.temperature
    weights = [
        temperature.getAdjustedValue(getattr(objekt, attribute)) for objekt in objects
    ]
    return random.weighted_choice(objects, weights)


def choose_unmodified_object(
    ctx, attribute: str, in_objects: List[WorkspaceObject]
) -> WorkspaceObject:
    """
    Chooses an unmodified object from a list of workspace objects based on a specified attribute.

    Parameters:
        ctx: The context containing the workspace.
        attribute (str): The attribute used to choose the object.
        in_objects (List[WorkspaceObject]): A list of WorkspaceObject instances to choose from.

    Returns:
        WorkspaceObject: An unmodified WorkspaceObject selected from the provided list.
    """
    workspace = ctx.workspace
    objects = [objekt for objekt in in_objects if objekt.string != workspace.modified]
    return __choose_object_from_list(ctx, objects, attribute)


def choose_neighbor(ctx, source: WorkspaceObject) -> WorkspaceObject:
    """
    Chooses a neighboring WorkspaceObject based on the provided source object.

    Args:
        ctx: The context containing the workspace.
        source (WorkspaceObject): The source object from which to find neighbors.

    Returns:
        WorkspaceObject: A neighboring object that is beside the source object,
                         selected based on the "intraStringSalience" criterion.
    """
    workspace = ctx.workspace
    objects = [objekt for objekt in workspace.objects if objekt.beside(source)]
    return __choose_object_from_list(ctx, objects, "intraStringSalience")


def choose_directed_neighbor(
    ctx, source: WorkspaceObject, direction: Slipnode
) -> WorkspaceObject:
    """
    Choose a directed neighbor of a given source object in the workspace.

    Parameters:
        ctx (Context): The context containing the slipnet and workspace.
        source (Object): The source object from which to find a neighbor.
        direction (str): The direction to search for the neighbor ('left' or 'right').

    Returns:
        Object: The chosen neighbor object based on the specified direction and salience.
    """
    slipnet = ctx.slipnet
    workspace = ctx.workspace
    if direction == slipnet.left:
        objects = [
            objekt
            for objekt in workspace.objects
            if objekt.string == source.string
            and source.leftIndex == objekt.rightIndex + 1
        ]
    else:
        objects = [
            objekt
            for objekt in workspace.objects
            if objekt.string == source.string
            and objekt.leftIndex == source.rightIndex + 1
        ]
    return __choose_object_from_list(ctx, objects, "intraStringSalience")
