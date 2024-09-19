"""
This module defines the WorkspaceString class, which represents a string within the Copycat 
workspace.  The WorkspaceString class includes attributes for the string, its bonds, objects, 
letters, and methods for manipulation and analysis.

Classes:
    WorkspaceString:
        A class that encapsulates a string within the Copycat workspace, along with its 
        associated properties and methods for manipulation and analysis.
"""

from typing import Any, List, Optional
from .group import Group
from .letter import Letter


class WorkspaceString(object):
    """
    WorkspaceString class represents a string within the Copycat workspace,
    along with its associated properties and methods for manipulation and analysis.

    Attributes:
        ctx (Copycat): The Copycat context.
        string (str): The string being represented.
        bonds (List[Any]): List of bonds within the string.
        objects (List[Any]): List of objects within the string.
        letters (List[Any]): List of letters within the string.
        length (int): Length of the string.
        intraStringUnhappiness (float): Measure of unhappiness within the string.

    Methods:
        __init__(ctx: Copycat, s: str):
            Initializes a WorkspaceString instance with the given context and string.

        __repr__() -> str:
            Returns a string representation of the WorkspaceString instance.

        __str__() -> str:
            Returns a formatted string describing the WorkspaceString instance.

        __len__() -> int:
            Returns the length of the string.

        __getitem__(i: int) -> str:
            Returns the character at the specified index in the string.

        update_relative_importance():
            Updates the normalized importance of all objects in the string.

        update_intra_string_unhappiness():
            Updates the intra-string unhappiness based on the objects in the string.

        equivalent_group(sought: Any) -> Optional[Group]:
            Checks if there is an equivalent group to the sought group within the objects.
    """

    ctx: "Copycat"  # type: ignore # noqa: F821
    string: str
    bonds: List[Any]
    objects: List[Any]
    letters: List[Any]
    length: int
    intra_string_unhappiness: float

    def __init__(self, ctx: "Copycat", s: str):  # type: ignore ## noqa: F821
        slipnet = ctx.slipnet
        workspace = ctx.workspace
        self.ctx = ctx
        self.string = s
        self.bonds = []
        self.objects = []
        self.letters = []
        self.length = len(s)
        self.intra_string_unhappiness = 0.0

        for position, c in enumerate(self.string.upper(), 1):
            value = ord(c) - ord("A")
            letter = Letter(self, position, self.length)
            ## letter.workspaceString = self        ## TODO: check if this is needed
            ## assert letter.workspaceString == letter.string
            letter.addDescription(slipnet.object_category, slipnet.letter)
            letter.addDescription(slipnet.letter_category, slipnet.letters[value])
            letter.describe(position, self.length)
            workspace.build_descriptions(letter)
            self.letters += [letter]

    def __repr__(self) -> str:
        return f"<WorkspaceString: {self.string}>"

    def __str__(self) -> str:
        return (
            f"{self.string} "
            f"with {len(self.letters)} letters, "
            f"{len(self.objects)} objects, "
            f"{len(self.bonds)} bonds"
        )

    def __len__(self) -> int:
        return len(self.string)

    def __getitem__(self, i) -> str:
        return self.string[i]

    def update_relative_importance(self) -> None:
        """
        Update the normalized importance of all objects in the string.

        This method calculates the total raw importance of all objects in the 
        string. If the total raw importance is zero, it sets the relative 
        importance of each object to 0.0. Otherwise, it normalizes the 
        importance of each object by dividing its raw importance by the total 
        raw importance.

        Attributes:
            self.objects (list): A list of objects, each having 'rawImportance' 
                                 and 'relativeImportance' attributes.
        """
        total = sum(objekt.rawImportance for objekt in self.objects)
        if not total:
            for objekt in self.objects:
                objekt.relativeImportance = 0.0
        else:
            for objekt in self.objects:
                objekt.relativeImportance = objekt.rawImportance / total

    def update_intra_string_unhappiness(self) -> None:
        """
        Updates the intra-string unhappiness metric for the current object.

        This method calculates the average intra-string unhappiness of all
        objects contained within the current object. If there are no objects,
        it sets the intra-string unhappiness to 0.0.
        """
        if len(self.objects) == 0:
            self.intra_string_unhappiness = 0.0
            return
        total = sum(objekt.intraStringUnhappiness for objekt in self.objects)
        self.intra_string_unhappiness = total / len(self.objects)

    def equivalent_group(self, sought) -> Optional[Group]:
        """
        Finds and returns an equivalent group from the list of objects.

        Args:
            sought: The group to be matched against the objects.

        Returns:
            Optional[Group]: The matching group if found, otherwise None.
        """
        for objekt in self.objects:
            if isinstance(objekt, Group):
                if objekt.sameGroup(sought):
                    return objekt
        return None
