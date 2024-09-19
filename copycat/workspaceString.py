from .group import Group
from .letter import Letter


class WorkspaceString(object):
    def __init__(self, ctx, s):
        slipnet = ctx.slipnet
        workspace = ctx.workspace
        self.ctx = ctx
        self.string = s
        self.bonds = []
        self.objects = []
        self.letters = []
        self.length = len(s)
        self.intraStringUnhappiness = 0.0

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

    def __repr__(self):
        return "<WorkspaceString: %s>" % self.string

    def __str__(self):
        return "%s with %d letters, %d objects, %d bonds" % (
            self.string,
            len(self.letters),
            len(self.objects),
            len(self.bonds),
        )

    def __len__(self):
        return len(self.string)

    def __getitem__(self, i):
        return self.string[i]

    def updateRelativeImportance(self):
        """Update the normalised importance of all objects in the string."""
        total = sum(objekt.rawImportance for objekt in self.objects)
        if not total:
            for objekt in self.objects:
                objekt.relativeImportance = 0.0
        else:
            for objekt in self.objects:
                objekt.relativeImportance = objekt.rawImportance / total

    def updateIntraStringUnhappiness(self):
        if not len(self.objects):
            self.intraStringUnhappiness = 0.0
            return
        total = sum(o.intraStringUnhappiness for o in self.objects)
        self.intraStringUnhappiness = total / len(self.objects)

    def equivalentGroup(self, sought):
        for objekt in self.objects:
            if isinstance(objekt, Group):
                if objekt.sameGroup(sought):
                    return objekt
        return None
