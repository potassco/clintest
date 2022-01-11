from clorm import Predicate, ConstantField, IntegerField
from clorm.clingo import Control
from clorm import FactBase


class Driver(Predicate):
    name=ConstantField

class Item(Predicate):
    name=ConstantField

class Assignment(Predicate):
    item=ConstantField
    driver=ConstantField
    time=IntegerField


ctrl = Control(unifier=[Driver, Item, Assignment])
ctrl.load("example.lp")



drivers = [ Driver(name=n) for n in ["dave", "morri", "michael" ] ]
items = [ Item(name="item{}".format(i)) for i in range(1,6) ]
instance = FactBase(drivers + items)


print(drivers[0])
print(items)
print(instance)


