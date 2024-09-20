"""
This module defines the WorkspaceStructure class, which represents a structure within a workspace.
The WorkspaceStructure class includes methods to update and calculate the strengths of the 
structure.

Classes:
    WorkspaceStructure:
        A base class representing a structure within a workspace, including methods to update and
        calculate the strengths of the structure.

Modules:
    formulas:
        A module that provides utility functions for calculations related to the workspace 
        structures.
"""

from . import formulas


class WorkspaceStructure(object):
    """
    WorkspaceStructure is a base class representing a structure within a workspace.
    It includes methods to update and calculate the strengths of the structure.

    Attributes:
        ctx (Copycat): The context in which this structure exists.
        string (str): A string representation of the structure.
        internal_strength (float): The internal strength of the structure.
        external_strength (float): The external strength of the structure.
        total_strength (float): The total strength of the structure.

    Methods:
        __init__(ctx):
            Initializes the WorkspaceStructure with the given context.

        update_strength():
            Updates the internal, external, and total strengths of the structure.

        update_total_strength():
            Recalculates the total strength from internal and external strengths.

        total_weakness():
            Calculates and returns the total weakness of the structure.

        update_internal_strength():
            Abstract method to update the internal strength. Must be implemented by subclasses.

        update_external_strength():
            Abstract method to update the external strength. Must be implemented by subclasses.

        break_the_structure():
            Abstract method to break the structure. Must be implemented by subclasses.
    """

    ctx: "Copycat"  # type: ignore # noqa: F821
    string = None
    internal_strength: float
    external_strength: float
    total_strength: float

    def __init__(self, ctx):
        self.ctx = ctx
        self.string = None
        self.internal_strength = 0.0
        self.external_strength = 0.0
        self.total_strength = 0.0

    def update_strength(self) -> None:
        """
        Updates the strength attributes of the object by calling internal, external,
        and total strength update methods.

        This method performs the following steps:
        1. Updates the internal strength of the object.
        2. Updates the external strength of the object.
        3. Updates the total strength of the object based on the internal and external strengths.
        """
        self.update_internal_strength()
        self.update_external_strength()
        self.update_total_strength()

    def update_total_strength(self) -> None:
        """
        Recalculate the strength from internal and external strengths.
        Recalculate and update the total strength attribute.

        This method calculates the total strength by computing a weighted average
        of the internal and external strengths. The internal strength is used twice
        in the calculation, while the external strength is weighted by the
        complement of the internal strength (i.e., 100 - internal strength).

        The calculated total strength is then assigned to the `total_strength` attribute.
        """
        weights = (
            (self.internal_strength, self.internal_strength),
            (self.external_strength, 100 - self.internal_strength),
        )
        strength = formulas.weighted_average(weights)
        self.total_strength = strength

    def total_weakness(self) -> float:
        """
        Calculate the total weakness of the entity.

        The total weakness is computed as 100 minus the total strength raised to the power of 0.95.

        Returns:
            float: The calculated total weakness.
        """
        return 100 - self.total_strength**0.95

    def update_internal_strength(self) -> None:
        """
        Updates the internal strength of the object.

        This method should be implemented by subclasses to define how the internal
        strength of the object is updated. It raises a NotImplementedError if not
        overridden.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError()

    def update_external_strength(self) -> None:
        """
        Updates the external strength of the current object.

        This method is intended to be overridden in subclasses to provide
        specific functionality for updating external strength. If not
        overridden, it will raise a NotImplementedError.

        Raises:
            NotImplementedError: If the method is not overridden in a subclass.
        """
        raise NotImplementedError()

    def break_the_structure(self) -> None:
        """
        Break this workspace structure (Bond, Correspondence, or Group)

        This method should be implemented by subclasses to define the specific
        behavior for breaking down the workspace structure, which could be a
        Bond, Correspondence, or Group.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError()
