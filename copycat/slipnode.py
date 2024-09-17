"""
This module defines the Slipnode class, which represents a node in the Slipnet.
The Slipnode class includes attributes for activation, links to other nodes, and
methods for managing these attributes.
"""

import math
from typing import List, Optional
from .randomness import Randomness


def jump_threshold() -> float:
    """Returns the jump threshold value."""
    return 55.0


class Slipnode:
    """
    Represents a node in the Slipnet.

    Attributes:
        slipnet (Slipnet): The Slipnet to which this node belongs.
        name (str): The name of the node.
        conceptual_depth (float): The conceptual depth of the node.
        intrinsic_link_length (float): The intrinsic link length of the node.
        shrunk_link_length (float): The shrunk link length of the node.
        activation (float): The activation level of the node.
        buffer (float): The buffer value for the node.
        clamped (bool): Indicates if the node's activation is clamped.
        category_links (List[Sliplink]): List of category links from this node.
        instance_links (List[Sliplink]): List of instance links from this node.
        property_links (List[Sliplink]): List of property links from this node.
        lateral_slip_links (List[Sliplink]): List of lateral slip links from this node.
        lateral_non_slip_links (List[Sliplink]): List of lateral non-slip links from this node.
        incoming_links (List[Sliplink]): List of incoming links to this node.
        outgoing_links (List[Sliplink]): List of outgoing links from this node.
        codelets (List[Codelet]): List of codelets associated with this node.
    """

    slipnet: "Slipnet"  # type: ignore  # noqa: F821
    name: str
    conceptual_depth: float
    intrinsic_link_length: float
    shrunk_link_length: float

    activation: float = 0.0
    old_activation: Optional[float] = None
    buffer: float = 0.0
    clamped: bool = False
    category_links: List["Sliplink"] = []  # type: ignore  # noqa: F821
    instance_links: List["Sliplink"] = []  # type: ignore  # noqa: F821
    property_links: List["Sliplink"] = []  # type: ignore  # noqa: F821
    lateral_slip_links: List["Sliplink"] = []  # type: ignore  # noqa: F821
    lateral_non_slip_links: List["Sliplink"] = []  # type: ignore  # noqa: F821
    incoming_links: List["Sliplink"] = []  # type: ignore  # noqa: F821
    outgoing_links: List["Sliplink"] = []  # type: ignore  # noqa: F821
    codelets: List["Codelet"] = []  # type: ignore  # noqa: F821

    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        slipnet: "Slipnet",  # type: ignore  # noqa: F821
        name: str,
        depth: float,
        length: float = 0.0,
    ):
        self.slipnet = slipnet
        self.name = name
        self.conceptual_depth = depth
        self.intrinsic_link_length = length
        self.shrunk_link_length = length * 0.4

        self.activation = 0.0
        self.buffer = 0.0
        self.clamped = False
        self.category_links = []
        self.instance_links = []
        self.property_links = []
        self.lateral_slip_links = []
        self.lateral_non_slip_links = []
        self.incoming_links = []
        self.outgoing_links = []
        self.codelets = []

    def __repr__(self) -> str:
        return f"<Slipnode: {self.name}>"

    def reset(self) -> None:
        """Resets the buffer and activation of the Slipnode."""
        self.buffer = 0.0
        self.activation = 0.0

    def clamp_high(self) -> None:
        """Clamps the activation of the Slipnode to a high value."""
        self.clamped = True
        self.activation = 100.0

    def unclamp(self) -> None:
        """Unclamps the activation of the Slipnode."""
        self.clamped = False

    def unclamped(self) -> bool:
        """
        Checks if the Slipnode is unclamped.

        Returns:
            bool: True if the Slipnode is unclamped, False otherwise.
        """
        return not self.clamped

    def category(self) -> Optional["Slipnode"]:
        """
        Returns the category of the Slipnode based on its category links.

        Returns:
            Optional[Slipnode]: The category Slipnode if it exists, otherwise None.
        """
        if len(self.category_links) == 0:
            return None
        link = self.category_links[0]
        return link.destination

    def fully_active(self) -> bool:
        """
        Whether this node has full activation

        Returns:
            bool: True if the Slipnode has full activation, False otherwise.
        """
        float_margin = 0.00001
        return self.activation > 100.0 - float_margin

    def bond_degree_of_association(self) -> float:
        """
        Calculates the bond degree of association for the Slipnode.

        Returns:
            float: The bond degree of association.
        """
        link_length: float = self.intrinsic_link_length
        if self.fully_active():
            link_length = self.shrunk_link_length
        result = math.sqrt(100 - link_length) * 11.0
        return min(100.0, result)

    def degree_of_association(self) -> float:
        """
        Calculates the degree of association for the Slipnode.

        Returns:
            float: The degree of association.
        """
        link_length = self.intrinsic_link_length
        if self.fully_active():
            link_length = self.shrunk_link_length
        return 100.0 - link_length

    def linked(self, other: "Slipnode") -> bool:
        """
        Checks if the Slipnode is linked to another Slipnode.

        Args:
            other (Slipnode): The other Slipnode to check.

        Returns:
            bool: True if the Slipnode is linked to the other Slipnode, False otherwise.
        """
        return any(link.points_at(other) for link in self.outgoing_links)

    def slip_linked(self, other: "Slipnode") -> bool:
        """
        Checks if the Slipnode is slip-linked to another Slipnode.

        Args:
            other (Slipnode): The other Slipnode to check.

        Returns:
            bool: True if the Slipnode is slip-linked to the other Slipnode, False otherwise.
        """
        return any(link.points_at(other) for link in self.lateral_slip_links)

    def related(self, other: "Slipnode") -> bool:
        """
        Checks if the Slipnode is the same as or linked to another Slipnode.

        Args:
            other (Slipnode): The other Slipnode to check.

        Returns:
            bool: True if the Slipnode is the same as or linked to the other Slipnode,
                False otherwise.
        """
        return self == other or self.linked(other)

    def apply_slippages(
        self, slippages: List["ConceptMapping"]  # type: ignore  # noqa: F821
    ) -> "Slipnode":
        """
        Applies slippages to the Slipnode.

        Args:
            slippages (list): A list of slippages to apply.
        """
        for slippage in slippages:
            if self == slippage.initialDescriptor:
                return slippage.targetDescriptor
        return self

    def get_related_node(self, relation: "Slipnode") -> Optional["Slipnode"]:
        """Return the node that is linked to this node via this relation.

        If no linked node is found, return None
        """
        slipnet: "Slipnet" = self.slipnet  # type: ignore  # noqa: F821
        if relation == slipnet.identity:
            return self
        destinations = [
            link.destination for link in self.outgoing_links if link.label == relation
        ]
        if destinations:
            return destinations[0]
        return None

    def get_bond_category(self, destination: "Slipnode") -> Optional["Slipnode"]:
        """Return the label of the link between these nodes if it exists.

        If it does not exist return None
        """
        slipnet: "Slipnet" = self.slipnet  # type: ignore  # noqa: F821
        if self == destination:
            return slipnet.identity
        else:
            for link in self.outgoing_links:
                if link.destination == destination:
                    return link.label
        return None

    def update(self) -> None:
        """Updates the activation buffer of the Slipnode."""
        self.old_activation = self.activation
        self.buffer -= self.activation * (100.0 - self.conceptual_depth) / 100.0

    def spread_activation(self) -> None:
        """Spreads activation to outgoing links if the Slipnode is fully active."""
        if self.fully_active():
            for link in self.outgoing_links:
                link.spread_activation()

    def add_buffer(self) -> None:
        """Adds the buffer value to the activation and clamps it between 0 and 100."""
        if self.unclamped():
            self.activation += self.buffer
        self.activation = min(max(0, self.activation), 100)

    def jump(self, random: Randomness) -> None:
        """
        Determines if the Slipnode should jump to full activation based on a random value.

        Args:
            random: An object with a coinFlip method to determine randomness.
        """
        if self.clamped or self.activation <= jump_threshold():
            return
        value = (self.activation / 100.0) ** 3
        if random.coin_flip(value):
            self.activation = 100.0

    def get_name(self) -> str:
        """returns the node name"""
        if len(self.name) == 1:
            return self.name.upper()
        return self.name
