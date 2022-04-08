class Model:

    def __init__(self, context, cost, number, optimality_proven, model_type):
        self.context = context
        self.cost = cost
        self.number = number
        self.optimality_proven = optimality_proven
        self.model_type = model_type
        self.model = []


    
    def from_model(model):
        m =  Model(
            context=model.context,
            cost = model.cost,
            number = model.number,
            optimality_proven=model.optimality_proven,
            model_type=model.type
        )

        m.model = model.symbols(atoms=True)

        return m
