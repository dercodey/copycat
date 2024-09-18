"""
This module defines the Slipnet class, which represents a network of Slipnodes and Sliplinks.
The Slipnet class includes methods for initializing, resetting, and updating the network.

Classes:
    Slipnet:
        A class that encapsulates the Slipnet, including its nodes and links, and provides methods
        for managing the network's state and behavior.
"""

from typing import List, Optional

from .randomness import Randomness
from .slipnode import Slipnode
from .sliplink import Sliplink


class Slipnet(object):
    """
    Slipnet class represents a network of slipnodes that facilitates the activation and interaction of various elements such as letters, numbers, and their relationships.
    Attributes:
        number_of_updates (int): The count of updates performed on the Slipnet.
        slipnodes (List[Slipnode]): A list of all slipnodes in the Slipnet.
        letters (List[Slipnode]): A list of slipnodes representing letters.
        numbers (List[Slipnode]): A list of slipnodes representing numbers.
        leftmost, rightmost, middle, single, whole (Slipnode): Slipnodes representing string positions.
        first, last (Slipnode): Slipnodes representing alphabetic positions.
        left, right (Slipnode): Slipnodes representing directions.
        predecessor, successor, sameness (Slipnode): Slipnodes representing bond types.
        predecessor_group, successor_group, sameness_group (Slipnode): Slipnodes representing group types.
        identity, opposite (Slipnode): Slipnodes representing other relations.
        letter, group (Slipnode): Slipnodes representing objects.
        letter_category, string_position_category, alphabetic_position_category, direction_category, bond_category, group_category, length, object_category, bond_facet (Slipnode): Slipnodes representing various categories.
        initially_clamped_slipnodes (List[Slipnode]): A list of slipnodes that are initially clamped.
    Methods:
        __init__: Initializes the Slipnet instance and sets up the initial nodes and links.
        reset: Resets the Slipnet by resetting all nodes and clamping the initially clamped nodes.
        update: Updates the Slipnet by spreading activation and updating the state of each node.
        is_distinguishing_descriptor: Determines if a given descriptor is unique among its type.
        __add_initial_nodes: Initializes the slipnet with a set of predefined nodes.
        __add_initial_links: Establishes connections between various elements in the slipnet.
        __add_link: Adds a link between two Slipnodes.
        __add_slip_link: Adds a lateral slip link between two Slipnodes.
        __add_non_slip_link: Adds a non-slip link between two Slipnodes.
        __add_bidirectional_link: Adds a bidirectional link between two Slipnodes.
    """

    number_of_updates: int
    slipnodes: List[Slipnode]

    letters: List[Slipnode]
    numbers: List[Slipnode]

    # string positions
    leftmost: Slipnode
    rightmost: Slipnode
    middle: Slipnode
    single: Slipnode
    whole: Slipnode

    # alphabetic positions
    first: Slipnode
    last: Slipnode

    # directions
    left: Slipnode
    right: Slipnode

    # bond types
    predecessor: Slipnode
    successor: Slipnode
    sameness: Slipnode

    # group types
    predecessor_group: Slipnode
    successor_group: Slipnode
    sameness_group: Slipnode

    # other relations
    identity: Slipnode
    opposite: Slipnode

    # objects
    letter: Slipnode
    group: Slipnode

    # categories
    letter_category: Slipnode
    string_position_category: Slipnode
    alphabetic_position_category: Slipnode
    direction_category: Slipnode
    bond_category: Slipnode
    group_category: Slipnode
    length: Slipnode
    object_category: Slipnode
    bond_facet: Slipnode

    initially_clamped_slipnodes: List[Slipnode]

    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        """Initializes the Slipnet instance and sets up the initial nodes and links."""
        self.__add_initial_nodes()
        self.__add_initial_links()
        self.reset()

    def reset(self) -> None:
        """Resets the Slipnet by resetting all nodes and clamping the initially clamped nodes."""
        self.number_of_updates = 0
        for node in self.slipnodes:
            node.reset()
        for node in self.initially_clamped_slipnodes:
            node.clamp_high()

    def update(self, random: Randomness) -> None:
        """
        Updates the Slipnet by spreading activation and updating the state of each node.

        Args:
            random (Randomness): An instance of the Randomness class for random operations.
        """
        self.number_of_updates += 1
        if self.number_of_updates == 50:
            for node in self.initially_clamped_slipnodes:
                node.unclamp()
        for node in self.slipnodes:
            node.update()
        for node in self.slipnodes:
            node.spread_activation()
        for node in self.slipnodes:
            node.add_buffer()
            node.jump(random)
            node.buffer = 0.0

    def is_distinguishing_descriptor(self, descriptor: Slipnode) -> bool:
        """Whether no other object of the same type has the same descriptor"""
        if descriptor == self.letter:
            return False
        if descriptor == self.group:
            return False
        if descriptor in self.numbers:
            return False
        return True

    def __add_initial_nodes(self) -> None:
        """
        Initializes the slipnet with a set of predefined nodes representing
        letters, numbers, string positions, directions, bond types, group types,
        relations, objects, and categories. Each node is created with a specific
        weight and may have associated codelets for further processing.

        The method performs the following actions:
        - Adds nodes for each letter in the alphabet with a weight of 10.0.
        - Adds nodes for numbers 1 to 5 with a weight of 30.0.
        - Adds nodes for various string positions (leftmost, rightmost, middle,
            single, whole) with a weight of 40.0.
        - Adds nodes for alphabetic positions (first, last) with a weight of 60.0.
        - Adds directional nodes (left, right) with a weight of 40.0 and
            associated codelets.
        - Adds bond type nodes (predecessor, successor, sameness) with weights of
            50.0 and 80.0, along with associated codelets.
        - Adds group type nodes (predecessorGroup, successorGroup, samenessGroup)
            with weights of 50.0 and 80.0, along with associated codelets.
        - Adds relation nodes (identity, opposite) with weights of 90.0.
        - Adds object nodes (letter, group) with weights of 20.0 and 80.0.
        - Adds category nodes for letters, string positions, alphabetic positions,
            directions, bonds, groups, length, and objects with varying weights.
        - Initializes a list of initially clamped slipnodes for relevant categories.

        Returns:
                None
        """
        # pylint: disable=too-many-statements
        self.slipnodes = []
        self.letters = []
        for c in "abcdefghijklmnopqrstuvwxyz":
            slipnode = self.__add_node(c, 10.0)
            self.letters += [slipnode]
        self.numbers = []
        for c in "12345":
            slipnode = self.__add_node(c, 30.0)
            self.numbers += [slipnode]

        # string positions
        self.leftmost = self.__add_node("leftmost", 40.0)
        self.rightmost = self.__add_node("rightmost", 40.0)
        self.middle = self.__add_node("middle", 40.0)
        self.single = self.__add_node("single", 40.0)
        self.whole = self.__add_node("whole", 40.0)

        # alphabetic positions
        self.first = self.__add_node("first", 60.0)
        self.last = self.__add_node("last", 60.0)

        # directions
        self.left = self.__add_node("left", 40.0)
        self.left.codelets += ["top-down-bond-scout--direction"]
        self.left.codelets += ["top-down-group-scout--direction"]
        self.right = self.__add_node("right", 40.0)
        self.right.codelets += ["top-down-bond-scout--direction"]
        self.right.codelets += ["top-down-group-scout--direction"]

        # bond types
        self.predecessor = self.__add_node("predecessor", 50.0, 60)
        self.predecessor.codelets += ["top-down-bond-scout--category"]
        self.successor = self.__add_node("successor", 50.0, 60)
        self.successor.codelets += ["top-down-bond-scout--category"]
        self.sameness = self.__add_node("sameness", 80.0)
        self.sameness.codelets += ["top-down-bond-scout--category"]

        # group types
        self.predecessor_group = self.__add_node("predecessorGroup", 50.0)
        self.predecessor_group.codelets += ["top-down-group-scout--category"]
        self.successor_group = self.__add_node("successorGroup", 50.0)
        self.successor_group.codelets += ["top-down-group-scout--category"]
        self.sameness_group = self.__add_node("samenessGroup", 80.0)
        self.sameness_group.codelets += ["top-down-group-scout--category"]

        # other relations
        self.identity = self.__add_node("identity", 90.0)
        self.opposite = self.__add_node("opposite", 90.0, 80.0)

        # objects
        self.letter = self.__add_node("letter", 20.0)
        self.group = self.__add_node("group", 80.0)

        # categories
        self.letter_category = self.__add_node("letterCategory", 30.0)
        self.string_position_category = self.__add_node("stringPositionCategory", 70.0)
        self.string_position_category.codelets += ["top-down-description-scout"]
        self.alphabetic_position_category = self.__add_node(
            "alphabeticPositionCategory", 80.0
        )
        self.alphabetic_position_category.codelets += ["top-down-description-scout"]
        self.direction_category = self.__add_node("directionCategory", 70.0)
        self.bond_category = self.__add_node("bondCategory", 80.0)
        self.group_category = self.__add_node("groupCategory", 80.0)
        self.length = self.__add_node("length", 60.0)
        self.object_category = self.__add_node("objectCategory", 90.0)
        self.bond_facet = self.__add_node("bondFacet", 90.0)

        # some factors are considered "very relevant" a priori
        self.initially_clamped_slipnodes = [
            self.letter_category,
            self.string_position_category,
        ]

    def __add_initial_links(self):
        """
        Initializes the slip links between various elements in the slipnet.

        This method establishes connections between letters, numbers, and their respective
        categories, properties, and groups. It creates links for opposites, bonds, and relationships
        between different categories, ensuring that the slipnet structure is properly configured for
        further operations.

        The following types of links are created:
        - Instance links between letters and their categories.
        - Non-slip links between groups and lengths.
        - Opposite links between pairs of elements.
        - Property links for specific letters to their first and last counterparts.
        - Bidirectional links between directional and positional elements.
        - Slip links between letters and groups.

        This method does not return any value but modifies the internal state of the slipnet by
        adding the necessary links.
        """
        self.sliplinks = []
        self.__link_items_to_their_neighbors(self.letters)
        self.__link_items_to_their_neighbors(self.numbers)
        # letter categories
        for letter in self.letters:
            self.__add_instance_link(self.letter_category, letter, 97.0)
        self.__add_category_link(self.sameness_group, self.letter_category, 50.0)
        # lengths
        for number in self.numbers:
            self.__add_instance_link(self.length, number)
        groups = [self.predecessor_group, self.successor_group, self.sameness_group]
        for group in groups:
            self.__add_non_slip_link(group, self.length, length=95.0)
        opposites = [
            (self.first, self.last),
            (self.leftmost, self.rightmost),
            (self.left, self.right),
            (self.successor, self.predecessor),
            (self.successor_group, self.predecessor_group),
        ]
        for a, b in opposites:
            self.__add_opposite_link(a, b)
        # properties
        self.__add_property_link(self.letters[0], self.first, 75.0)
        self.__add_property_link(self.letters[-1], self.last, 75.0)
        links = [
            # object categories
            (self.object_category, self.letter),
            (self.object_category, self.group),
            # string positions,
            (self.string_position_category, self.leftmost),
            (self.string_position_category, self.rightmost),
            (self.string_position_category, self.middle),
            (self.string_position_category, self.single),
            (self.string_position_category, self.whole),
            # alphabetic positions,
            (self.alphabetic_position_category, self.first),
            (self.alphabetic_position_category, self.last),
            # direction categories,
            (self.direction_category, self.left),
            (self.direction_category, self.right),
            # bond categories,
            (self.bond_category, self.predecessor),
            (self.bond_category, self.successor),
            (self.bond_category, self.sameness),
            # group categories
            (self.group_category, self.predecessor_group),
            (self.group_category, self.successor_group),
            (self.group_category, self.sameness_group),
            # bond facets
            (self.bond_facet, self.letter_category),
            (self.bond_facet, self.length),
        ]
        for a, b in links:
            self.__add_instance_link(a, b)
        # link bonds to their groups
        self.__add_non_slip_link(
            self.sameness, self.sameness_group, label=self.group_category, length=30.0
        )
        self.__add_non_slip_link(
            self.successor, self.successor_group, label=self.group_category, length=60.0
        )
        self.__add_non_slip_link(
            self.predecessor,
            self.predecessor_group,
            label=self.group_category,
            length=60.0,
        )
        # link bond groups to their bonds
        self.__add_non_slip_link(
            self.sameness_group, self.sameness, label=self.bond_category, length=90.0
        )
        self.__add_non_slip_link(
            self.successor_group, self.successor, label=self.bond_category, length=90.0
        )
        self.__add_non_slip_link(
            self.predecessor_group,
            self.predecessor,
            label=self.bond_category,
            length=90.0,
        )
        # letter category to length
        self.__add_slip_link(self.letter_category, self.length, length=95.0)
        self.__add_slip_link(self.length, self.letter_category, length=95.0)
        # letter to group
        self.__add_slip_link(self.letter, self.group, length=90.0)
        self.__add_slip_link(self.group, self.letter, length=90.0)
        # direction-position, direction-neighbor, position-neighbor
        self.__add_bidirectional_link(self.left, self.leftmost, 90.0)
        self.__add_bidirectional_link(self.right, self.rightmost, 90.0)
        self.__add_bidirectional_link(self.right, self.leftmost, 100.0)
        self.__add_bidirectional_link(self.left, self.rightmost, 100.0)
        self.__add_bidirectional_link(self.leftmost, self.first, 100.0)
        self.__add_bidirectional_link(self.rightmost, self.first, 100.0)
        self.__add_bidirectional_link(self.leftmost, self.last, 100.0)
        self.__add_bidirectional_link(self.rightmost, self.last, 100.0)
        # other
        self.__add_slip_link(self.single, self.whole, length=90.0)
        self.__add_slip_link(self.whole, self.single, length=90.0)

    def __add_link(
        self,
        source: Slipnode,
        destination: Slipnode,
        label: Optional[Slipnode] = None,
        length: float = 0.0,
    ) -> Sliplink:
        """
        Adds a link between two Slipnodes.

        Parameters:
            source (Slipnode): The source Slipnode for the link.
            destination (Slipnode): The destination Slipnode for the link.
            label (Optional[Slipnode], optional): An optional label for the link. Defaults to None.
            length (float, optional): The length of the link. Defaults to 0.0.

        Returns:
            Sliplink: The created Sliplink object connecting the source and destination Slipnodes.
        """
        link = Sliplink(source, destination, label=label, length=length)
        self.sliplinks += [link]
        return link

    def __add_slip_link(
        self,
        source: Slipnode,
        destination: Slipnode,
        label: Optional[Slipnode] = None,
        length: float = 0.0,
    ) -> None:
        """
        Adds a lateral slip link between two Slipnodes.

        Parameters:
            source (Slipnode): The source Slipnode from which the link originates.
            destination (Slipnode): The destination Slipnode to which the link points.
            label (Optional[Slipnode], optional): An optional label for the link. Defaults to None.
            length (float, optional): The length of the link. Defaults to 0.0.

        Returns:
            None
        """
        link = self.__add_link(source, destination, label, length)
        source.lateral_slip_links += [link]

    def __add_non_slip_link(
        self,
        source: Slipnode,
        destination: Slipnode,
        label: Optional[Slipnode] = None,
        length: float = 0.0,
    ) -> None:
        """
        Adds a non-slip link between two Slipnode instances.

        Parameters:
            source (Slipnode): The source Slipnode from which the link originates.
            destination (Slipnode): The destination Slipnode to which the link points.
            label (Optional[Slipnode], optional): An optional label for the link. Defaults to None.
            length (float, optional): The length of the link. Defaults to 0.0.

        Returns:
            None: This method does not return a value.
        """
        link = self.__add_link(source, destination, label, length)
        source.lateral_non_slip_links += [link]

    def __add_bidirectional_link(
        self,
        source: Slipnode,
        destination: Slipnode,
        length: float = 0.0,
    ) -> None:
        """
        Adds a bidirectional link between two Slipnode instances.

        This method creates a link from the source Slipnode to the destination Slipnode
        and vice versa, effectively establishing a two-way connection. The length of the
        link can be specified, with a default value of 0.0.

        Parameters:
            source (Slipnode): The starting node of the link.
            destination (Slipnode): The ending node of the link.
            length (float, optional): The length of the link. Defaults to 0.0.

        Returns:
            None
        """
        self.__add_non_slip_link(source, destination, length=length)
        self.__add_non_slip_link(destination, source, length=length)

    def __add_category_link(
        self,
        source: Slipnode,
        destination: Slipnode,
        length: float = 0.0,
    ) -> None:
        """
        Adds a category link between two Slipnode instances.

        Parameters:
            source (Slipnode): The source Slipnode from which the link originates.
            destination (Slipnode): The destination Slipnode to which the link points.
            length (float, optional): The length of the link. Defaults to 0.0.

        Returns:
            None
        """
        # noinspection PyArgumentEqualDefault
        link = self.__add_link(source, destination, None, length)
        source.category_links += [link]

    def __add_instance_link(
        self, source: Slipnode, destination: Slipnode, length: float = 100.0
    ) -> None:
        """
        Adds an instance link between two Slipnode objects.

        Parameters:
            source (Slipnode): The source Slipnode from which the link originates.
            destination (Slipnode): The destination Slipnode to which the link points.
            length (float, optional): The length of the link. Defaults to 100.0.

        Returns:
            None: This method does not return a value.

        Notes:
            This method calculates the category length based on the conceptual depth
            of the source and destination nodes and adds a category link before creating
            the instance link.
        """
        category_length = source.conceptual_depth - destination.conceptual_depth
        self.__add_category_link(destination, source, category_length)
        # noinspection PyArgumentEqualDefault
        link = self.__add_link(source, destination, None, length)
        source.instance_links += [link]

    def __add_property_link(
        self, source: Slipnode, destination: Slipnode, length: float
    ) -> None:
        """
        Adds a property link between two Slipnode instances.

        Parameters:
            source (Slipnode): The source Slipnode from which the link originates.
            destination (Slipnode): The destination Slipnode to which the link points.
            length (float): The length of the property link.

        Returns:
            None
        """
        # noinspection PyArgumentEqualDefault
        link = self.__add_link(source, destination, None, length)
        source.property_links += [link]

    def __add_opposite_link(self, source: Slipnode, destination: Slipnode) -> None:
        """
        Adds an opposite link between two Slipnodes.

        This method creates a bidirectional link between the source and destination Slipnodes.
        It adds a slip link from the source to the destination and another from the destination
        back to the source, both labeled as 'opposite'.

        Parameters:
            source (Slipnode): The starting Slipnode for the link.
            destination (Slipnode): The ending Slipnode for the link.

        Returns:
            None
        """
        self.__add_slip_link(source, destination, label=self.opposite)
        self.__add_slip_link(destination, source, label=self.opposite)

    def __add_node(self, name: str, depth: float, length: float = 0.0) -> Slipnode:
        """
        Adds a new Slipnode to the slipnet.

        Parameters:
            name (str): The name of the Slipnode to be added.
            depth (int): The depth level of the Slipnode.
            length (float, optional): The length associated with the Slipnode. Defaults to 0.0.

        Returns:
            Slipnode: The newly created Slipnode instance.
        """
        slipnode = Slipnode(self, name, depth, length)
        self.slipnodes += [slipnode]
        return slipnode

    def __link_items_to_their_neighbors(self, items: List[Slipnode]) -> None:
        """
        Links each item in the provided list to its neighboring items.

        This method iterates through a list of items and establishes non-slip links
        between each item and its predecessor and successor. The links are created
        using the `__add_non_slip_link` method, which is called twice for each
        pair of neighboring items.

        Parameters:
            items (list): A list of items to be linked. It is expected that the list
                          contains at least one item.

        Returns:
            None
        """
        previous = items[0]
        for item in items[1:]:
            self.__add_non_slip_link(previous, item, label=self.successor)
            self.__add_non_slip_link(item, previous, label=self.predecessor)
            previous = item
