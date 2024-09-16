"""
This module defines the Sliplink class, which represents a link between two nodes
with an optional label and fixed length. The class provides methods to calculate
the degree of association and spread activation between nodes.
"""

from typing import Optional
from .slipnode import Slipnode


class Sliplink:
    """
    Represents a link between two nodes with an optional label and fixed length.
    """

    source: Slipnode
    destination: Slipnode
    label: Optional[Slipnode]
    fixed_length: float

    def __init__(
        self,
        source: Slipnode,
        destination: Slipnode,
        label: Optional[Slipnode] = None,
        length: float = 0.0,
    ):
        """
        Initializes a Sliplink instance.

        Args:
            source: The source node.
            destination: The destination node.
            label: An optional label for the link.
            length: The fixed length of the link.
        """
        self.source = source
        self.destination = destination
        self.label = label
        self.fixed_length = length
        source.outgoing_links += [self]
        destination.incoming_links += [self]

    def degree_of_association(self) -> float:
        """
        Calculates the degree of association for the link.

        Returns:
            float: The degree of association.
        """
        if self.fixed_length > 0 or not self.label:
            return 100.0 - self.fixed_length
        return self.label.degree_of_association()

    def intrinsic_degree_of_association(self) -> float:
        """
        Calculates the intrinsic degree of association for the link.

        Returns:
            float: The intrinsic degree of association.
        """
        if self.fixed_length > 1:
            return 100.0 - self.fixed_length
        if self.label:
            return 100.0 - self.label.intrinsic_link_length
        return 0.0

    def spread_activation(self) -> None:
        """
        Spreads activation to the destination node based on the intrinsic degree of association.
        """
        self.destination.buffer += self.intrinsic_degree_of_association()

    def points_at(self, other: Slipnode) -> bool:
        """
        Checks if the link points at the given node.

        Args:
            other: The node to check.

        Returns:
            bool: True if the link points at the given node, False otherwise.
        """
        return self.destination == other
