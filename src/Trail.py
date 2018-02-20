# import copy
import Variable
import Domain
import copy

"""
    Represents the trail of changes made. This allows backtracking to occur.
"""

class Trail:

    # ==================================================================
    # Properties
    # ==================================================================
    numPush = 0
    numUndo = 0

    # ==================================================================
    # Constructor
    # ==================================================================

    def __init__ ( self ):
        self.trailStack  = []
        self.trailMarker = []

    # ==================================================================
    # Accessors
    # ==================================================================

    def size ( self ):
        return len( self.trailStack )

    def getPushCount ( self ):
        return Trail.numPush

    def getUndoCount ( self ):
        return Trail.numUndo

    # ==================================================================
    # Modifiers
    # ==================================================================

    # Places a marker in the trail
    def placeTrailMarker ( self ):
        self.trailMarker.append( len( self.trailStack ) )

    """
        Before you assign a variable in constraint propagation,
        use this function to save its initial domain on the
        backtrack trail. This way if the path you are on fails,
        you can restore propagated domains correctly.
    """
    def push ( self, v ):
        Trail.numPush += 1
        domainCopy = Domain.Domain( [i for i in v.getValues()] )
        vPair = [v, domainCopy]
        self.trailStack.append(vPair)

    # Pops and restores variables on the trail until the last trail marker
    def undo ( self ):
        Trail.numUndo += 1
        targetSize = self.trailMarker.pop() # targetSize target position on the trail to backtrack to
        size = len(self.trailStack)
        while size > targetSize:
            vPair = self.trailStack.pop()
            v = vPair[0]
            v.setDomain( vPair[1] )
            v.setModified( False )
            size -= 1

    # Clears the trail
    def clear ( self ):
        self.trailStack = []
        self.trailMarker = []
