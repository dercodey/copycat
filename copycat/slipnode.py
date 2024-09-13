import math


def jump_threshold():
    return 55.0


class Slipnode:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, slipnet: "Slipnet", name: str, depth: int, length: float = 0.0):
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

    def __repr__(self):
        return "<Slipnode: %s>" % self.name

    def reset(self):
        self.buffer = 0.0
        self.activation = 0.0

    def clampHigh(self):
        self.clamped = True
        self.activation = 100.0

    def unclamp(self):
        self.clamped = False

    def unclamped(self):
        return not self.clamped

    def category(self):
        if not len(self.category_links):
            return None
        link = self.category_links[0]
        return link.destination

    def fully_active(self):
        """Whether this node has full activation"""
        float_margin = 0.00001
        return self.activation > 100.0 - float_margin

    def bondDegreeOfAssociation(self):
        linkLength = self.intrinsic_link_length
        if self.fully_active():
            linkLength = self.shrunk_link_length
        result = math.sqrt(100 - linkLength) * 11.0
        return min(100.0, result)

    def degreeOfAssociation(self):
        linkLength = self.intrinsic_link_length
        if self.fully_active():
            linkLength = self.shrunk_link_length
        return 100.0 - linkLength

    def linked(self, other):
        """Whether the other is among the outgoing links"""
        return any(l.points_at(other) for l in self.outgoing_links)

    def slipLinked(self, other):
        """Whether the other is among the lateral links"""
        return any(l.points_at(other) for l in self.lateral_slip_links)

    def related(self, other):
        """Same or linked"""
        return self == other or self.linked(other)

    def applySlippages(self, slippages):
        for slippage in slippages:
            if self == slippage.initialDescriptor:
                return slippage.targetDescriptor
        return self

    def getRelatedNode(self, relation):
        """Return the node that is linked to this node via this relation.

        If no linked node is found, return None
        """
        slipnet = self.slipnet
        if relation == slipnet.identity:
            return self
        destinations = [
            l.destination for l in self.outgoing_links if l.label == relation
        ]
        if destinations:
            return destinations[0]
        return None

    def getBondCategory(self, destination):
        """Return the label of the link between these nodes if it exists.

        If it does not exist return None
        """
        slipnet = self.slipnet
        if self == destination:
            return slipnet.identity
        else:
            for link in self.outgoing_links:
                if link.destination == destination:
                    return link.label
        return None

    def update(self):
        self.oldActivation = self.activation
        self.buffer -= self.activation * (100.0 - self.conceptual_depth) / 100.0

    def spread_activation(self):
        if self.fully_active():
            for link in self.outgoing_links:
                link.spread_activation()

    def addBuffer(self):
        if self.unclamped():
            self.activation += self.buffer
        self.activation = min(max(0, self.activation), 100)

    def jump(self, random):
        if self.clamped or self.activation <= jump_threshold():
            return
        value = (self.activation / 100.0) ** 3
        if random.coinFlip(value):
            self.activation = 100.0

    def get_name(self):
        if len(self.name) == 1:
            return self.name.upper()
        return self.name
