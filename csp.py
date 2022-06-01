class Problem(object):
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal




class ConstraintSpecificationProblem(Problem):

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
                v: list(self.domains[v]) for v in self.elements
                }

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


def check_arc_consistency(csp, queue=None, toBeRemoved=None):
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.elements for Xk in csp.neighbors[Xi]]

    csp.make_pruning()

    while queue:
        (Xi, Xj) = queue.pop()

        if check_if_value_removed(csp, Xi, Xj, toBeRemoved):
            if not csp.curr_domains[Xi]:

                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    
                    queue.append((Xk, Xi))
    return True


def first(iterable, default=None):
    # Return the first element of an iterable or the next element of a generator
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)


def first_unassigned_variable(assignment, csp):
    return first([var for var in csp.elements if var not in assignment])


# Value ordering
def unordered_domain_values(element, assisment, csp):
    return csp.not_removed_values(element)

# Inference


def no_inference(csp, var, value, assignment, toBeRemoved):
    return True


def forward_checking(csp, element, value, assignment, toBeRemoved):
    csp.make_pruning()
    for B in csp.neighbors[element]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(element, value, B, b):
                    csp.prune(B, b, toBeRemoved)
            if not csp.curr_domains[B]:
                return False
    return True


def make_arc_consistency(csp, element, value, assignment, toBeRemoved):
    return check_arc_consistency(csp, [(X, element) for X in csp.neighbors[element]], toBeRemoved)


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):

    def backtrack(assignment):
        if len(assignment) == len(csp.elements):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.numberOfConflicts(var, value, assignment):
                csp.assignVarsToNewValues(var, value, assignment)
                toBeRemoved = csp.suppose(var, value)
                if inference(csp, var, value, assignment, toBeRemoved):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.undo_removal(toBeRemoved)
        csp.removeVarsAssignment(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.checkIfVariablesAssignedWithConstraintsSatisfied(
        result)
    return result



