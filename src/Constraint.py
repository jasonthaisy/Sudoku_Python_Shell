import Variable

"""
    Constraint represents a NotEquals constraint on a set of variables.
    Used to ensure none of the variables contained in the constraint have the same assignment.
"""

class Constraint:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self ):
        self.vars = []

    # ==================================================================
    # Modifiers
    # ==================================================================

    def addVariable ( self, v ):
        self.vars.append( v )

    # ==================================================================
    # Accessors
    # ==================================================================

    def size ( self ):
        return len(self.vars)

    # Returns true if v is in the constraint, false otherwise
    def contains ( self, v ):
        return v in self.vars

    # Returns whether or not the a variable in the constraint has been modified
    def isModified ( self ):
        for var in self.vars:
            if var.isModified():
                return True

        return False

    # Returns true if constraint is consistent, false otherwise
    def isConsistent ( self ):
        for var in self.vars:
            if not var.isAssigned():
                continue

            for otherVar in self.vars:
                if var == otherVar:
                    continue

                if otherVar.isAssigned() and otherVar.getAssignment() == var.getAssignment():
                    return False

        return True

    # ==================================================================
    # String representation
    # ==================================================================

    def __str__ ( self ):
        output = "{"
        delim = ""

        for v in self.vars:
            output += delim + v.name
            delim = ","

        output += "}"
        return output
