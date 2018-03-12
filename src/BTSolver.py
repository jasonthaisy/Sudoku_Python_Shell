import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you change their domain
        Return: true is assignment is consistent, false otherwise
    """
    def forwardChecking ( self ):
        """
        #if variable is assigned value
        #   check surrounding neighbors
        #       if neighbor contains value of assigned variable
        #           remove from domain
        #   if all neighbors remove value return true, else false
        recentAssignment = self.trail.trailStack[self.trail.size() - 1][0] #recentAssignment is most recently assigned
        neighboring = self.network.getNeighborsOfVariable(recentAssignment) 
        
        for variable in neighboring: # n = Constraint (i think this should be variable), neighboring = list of constraints(variables) 
            for constraints in self.network.getConstraintsContainingVariable(variable):
                if constraints.contains(recentAssignment): #check if neighbor contains value of assigned variable
                    variable.removeValueFromDomain(recentAssignment) #remove from domain
            #according to piazza we have to use getModifiedConstraints() and above trail.push? 
            
        return self.assignmentsCheck() #c) #check consistency of network
        """
        for v in self.network.variables:
            if v.isAssigned():
        #v = self.trail.trailStack[self.trail.size() - 1][0] #recentAssignment is most recently assigned
                for v2 in self.network.getNeighborsOfVariable(v):
                    if v.getAssignment() == v2.getAssignment():
                        return False
                    if v.getAssignment() in v2.getValues():
                        self.trail.push(v2)
                        v2.removeValueFromDomain(v.getAssignment())
                    if (v2.size() == 0):
                        return False
        return True
    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you change their domain
        Return: true is assignment is consistent, false otherwise
    """
    def norvigCheck ( self ):
        #first strategy: if a variable is assigned, then eliminate that value from the square's neighbors
        for v in self.network.variables:
            if v.isAssigned():
                for v2 in self.network.getNeighborsOfVariable(v):
                    if v.getAssignment() == v2.getAssignment():
                        return False
                    if v.getAssignment() in v2.getValues():
                        self.trail.push(v2)
                        v2.removeValueFromDomain(v.getAssignment())
                    if v2.size() == 0:
                        return False
        #second: if a constraint has only one possible place for a value then put the value there.
        for constraint in self.network.getConstraints(): #for each unit in {rows, cols, blocks}
            counter = [0 for i in range(self.gameboard.N)]
            for i in range(self.gameboard.N):
                for value in constraint.vars[i].getValues():
                    counter[value-1] += 1
            for i in range(self.gameboard.N):
                if counter[i] == 1:
                    for var in constraint.vars:
                        if var.getDomain().contains(i+1):
                            self.trail.push(var)
                            var.assignValue(i+1)
                            #var.removeValueFromDomain(i+1)
            #print("next block...")
            
        return self.assignmentsCheck()

    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournCC ( self ):
        return None

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        smallest = 9999
        vMRV = None
        
        for v in self.network.variables:
            if not v.isAssigned():
                if v.size() < smallest:
                    smallest = v.size()
                    vMRV = v
            
        return vMRV

    """
        Part 2 TODO: Implement the Degree Heuristic

        Return: The unassigned variable with the most unassigned neighbors
    """
    def getDegree ( self ):
        dhVariable = None
        maxUnassigned = -1
        for v in self.network.variables:
            if not v.isAssigned():
                cc = self.network.getConstraintsContainingVariable(v)
                degC = []
                for constraint in cc:
                    varsC = constraint.vars
                    for item in varsC:
                        if not item.isAssigned():
                            degC.append(item)
                if len(degC) > maxUnassigned:
                    dhVariable = v
                    maxUnassigned = len(degC)
#                numUnassigned = 0
#                for v2 in self.network.getNeighborsOfVariable(v):
#                    if not v2.isAssigned():
#                        numUnassigned += 1
#                if numUnassigned > maxUnassigned:
#                    maxUnassigned = numUnassigned
#                    dhVariable = v
                                
        return dhVariable

    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with, first, the smallest domain
                and, second, the most unassigned neighbors
    """
    def MRVwithTieBreaker ( self ):
        
        vMRV = None
        smallest = 9999

        for v in self.network.variables:
            if not v.isAssigned():
                if v.size() <= smallest or vMRV == None:
                    if v.size() == smallest:
                        tb = [v, vMRV]
                        maxV = None
                        largest = -1
                        for var in tb:
                            cc = self.network.getConstraintsContainingVariable(var)
                            degC = []
                            for constraint in cc:
                                varsC = constraint.vars
                                for item in varsC:
                                    if not item.isAssigned():
                                        degC.append(item)
                            if len(degC) > largest:
                                maxV = var
                                maxSize = len(degC)
                        vMRV = maxV
                        smallest = maxSize
                    else:
                        vMRV = v
                        smallest = v.size()
                    
        return vMRV         

    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        return None

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        leastConstrainingValues = dict()
        
        if not v.isAssigned(): # check if v is assigned
            for n in v.getValues(): #get each value within domain
                sum = 0
                #"test" some variable assignment n in domain
                for n2 in self.network.getNeighborsOfVariable(v):
                    if n2.domain.contains(n): #check if domain value in surrounding variable domain
                        sum += 1 
                
                leastConstrainingValues.update({n:sum})
        
        return sorted(leastConstrainingValues) #returns sorted key (domain value) from least to greatest sum

    """
         Optional TODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        return None

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self ):
        if self.hassolution:
            return

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            for var in self.network.variables:

                # If all variables haven't been assigned
                if not var.isAssigned():
                    print ( "Error" )

            # Success
            self.hassolution = True
            return

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recurse
            if self.checkConsistency():
                self.solve()

            # If this assignment succeeded, return
            if self.hassolution:
                return

            # Otherwise backtrack
            self.trail.undo()

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "Degree":
            return self.getDegree()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)