"""
    Represents the domain of a variable, i.e. the possible values that each
    variable may assign.
"""

class Domain:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, value_or_values ):
        self.values = []
        if type( value_or_values ) is int:
            self.values.append( value_or_values )

        else:
            self.values = value_or_values

        self.modified = False

    def copy ( self, values ):
        self.values = values

    # ==================================================================
    # Accessors
    # ==================================================================

    # Checks if value exists within the domain
    def contains ( self, v ):
        return v in self.values

    # Returns number of values in the domain
    def size ( self ):
        return len(self.values)

    # Returns true if no values are contained in the domain
    def isEmpty ( self ):
        return not self.values

    # Returns whether or not the domain has been modified
    def isModified ( self ):
        return self.modified

    # ==================================================================
    # Modifiers
    # ==================================================================

    # Adds a value to the domain
    def add ( self, num ):
        if num not in self.values:
            self.values.append( num )

    # Remove a value from the domain
    def remove ( self, num ):
        if num in self.values:
            self.modified = True
            self.values.remove( num )
            return True

        else:
            return False

    # Sets the modified flag
    def setModified ( self, modified ):
        self.modified = modified

    # ==================================================================
    # String representation
    # ==================================================================

    def __str__ ( self ):
        output = "{"
        for i in range(len(self.values) - 1):
            output += str(self.values[i]) + ", "
        try:
            output += str(self.values[-1])
        except:
            pass

        output += "}"
        return output
