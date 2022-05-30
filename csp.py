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


