

class Model:

    def __init__(self, model, persistant=False):
        self.persistant = persistant
        if not persistant : self._model = model
        else : self._model = PersistantModel(model)

    @property
    def context(self):
        return self.model.context

    @property
    def cost(self):
        return self.model.cost

    @property
    def number(self):
        return self.model.number

    @property
    def optimality_proven(self):
        return self.model.optimality_proven

    @property
    def type(self):
        return self.model.type

    @property
    def model(self):
        return self._model

    def persist(self):
        if not self.persist:
            if not self._model:
                raise Exception("Out of scope persist, psersist method should be called in the scope of its creation")
            self._model = PersistantModel(self._model)
            self.persistant = True

    def symbols(self):
        if self.persistant:
            return self._model.model
        else:
            return self._model.symbols(atoms=True)


class PersistantModel:
    def __init__(self, model):
        self.cost = model.cost
        self.number = model.number
        self.context = model.context
        self.optimality_proven = model.optimality_proven
        self.type = model.type
        self.model = model.symbols(atoms=True)
