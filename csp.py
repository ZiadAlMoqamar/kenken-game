class ConstraintSpecificationProblem():

    def __init__(self, elements, domains, neighbors, constraints):
        elements = elements or list(domains.keys())

        self.elements = elements
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0

    def assignVarsToNewValues(self, currentVar, currentVal, assignment):
        assignment[currentVar] = currentVal
        self.nassigns += 1

    def removeVarsAssignment(tself, element, assignment):
        # Remove var from assignment
        if element in assignment:
            del assignment[element]
    
    def numberOfConflicts(self, currentVariable, currentValue, assignment):
        # Functions on Sequences and Iterables

        def count(seq):
            # Count the number of items in sequence that are interpreted as true.
            return sum(bool(x) for x in seq)
        # Return the number of conflicts var=val has with other elements.

        def checkForConflict(element):
            return (element in assignment and
                    not self.constraints(currentVariable, currentValue, element, assignment[element]))
        return count(checkForConflict(v) for v in self.neighbors[currentVariable])

    def checkIfVariablesAssignedWithConstraintsSatisfied(self, status):
        # The goal is to assign all variables, with all constraints satisfied
        assignment = dict(status)
        return (len(assignment) == len(self.elements)
                and all(self.numberOfConflicts(elements, assignment[elements], assignment) == 0
                        for elements in self.elements))


