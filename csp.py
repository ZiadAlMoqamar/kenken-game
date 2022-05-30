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

    # functions for constraint propagation
    def make_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {
                v: list(self.domains[v]) for v in self.elements}

    def prune(self, element, value, toBeRemoved):
        # Remove value from domain of element
        self.curr_domains[element].remove(value)

        if toBeRemoved is not None:
            toBeRemoved.append((element, value))

    def suppose(self, element, value):
        self.make_pruning()
        toBeRemoved = [(element, a)
                       for a in self.curr_domains[element] if a != value]
        self.curr_domains[element] = [value]
        return toBeRemoved

    def not_removed_values(self, element):
        return (self.curr_domains or self.domains)[element]

    def undo_removal(self, toBeRemoved):
        for B, b in toBeRemoved:
            self.curr_domains[B].append(b)





# Constraint Propagation with Arc Consistency

def check_if_value_removed(csp, Xi, Xj, toBeRemoved):
    # Return true if we remove a value
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, toBeRemoved)
            revised = True
    return revised



