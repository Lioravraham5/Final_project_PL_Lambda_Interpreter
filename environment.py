class Environment:
    def __init__(self, parent=None, variables=None):
        self.parent = parent
        self.variables = variables if variables is not None else {}

    def define(self, name, value):
        self.variables[name] = value

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Undefined identifier: {name}")
