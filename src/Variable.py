import Trail
import Domain

"""
    Represents a variable in a CSP
"""

STATIC_NAMING_COUNTER = 1

class Variable:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, possible_Values, row, col, block ):
        global STATIC_NAMING_COUNTER
        self.name = "v" + str(STATIC_NAMING_COUNTER)
        STATIC_NAMING_COUNTER += 1

        self.domain = Domain.Domain( possible_Values )
        self.row = row
        self.col = col
        self.block = block
        if self.size() == 1:
            self.modified = True
            self.changeable = False
        else:
            self.modified = False
            self.changeable = True

    def copy ( self, v ):
        self.domain = v.domain
        self.row = v.row
        self.col = v.col
        self.block = v.block
        self.modified = v.modified
        self.name = v.name

    # ==================================================================
    # Accessors
    # ==================================================================

    def isChangeable ( self ):
        return self.changeable

    def isAssigned ( self ):
        return self.size() == 1

    def isModified ( self ):
        return self.modified

    def size ( self ):
        return self.domain.size()

    # Returns the assigned value or 0 if unassigned
    def getAssignment ( self ):
        if not self.isAssigned():
            return 0
        else:
            return self.domain.values[0]

    def getDomain ( self ):
        return self.domain

    def getName ( self ):
        return self.name

    def getValues ( self ):
        return self.domain.values

    # ==================================================================
    # Modifiers
    # ==================================================================

    def setModified ( self, mod ):
        self.modified = mod
        self.domain.modified = mod

    # Assign a value to the variable
    def assignValue ( self, val ):
        if not self.changeable:
            return

        self.setDomain( Domain.Domain( val ) )

    # Sets the domain of the variable
    def setDomain ( self, d ):
        if not self.changeable:
            return

        if self.domain != d:
            self.domain = d
            self.modified = True

    # Removes a value from the domain
    def removeValueFromDomain ( self, val ):
        if not self.changeable:
            return

        self.domain.remove( val )
        self.modified = self.domain.isModified()

    # ==================================================================
    # String representation
    # ==================================================================

    def __str__ ( self ):
        # "print node stats"
        output = ""
        output += " Name: " + self.name
        output += " domain: {"
        for i in self.domain.values:
            output += str(i) + ","
        output = output.rstrip()
        output = output[:-1]
        output += "}"
        return output
