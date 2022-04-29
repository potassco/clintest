import clintest
from pympler import asizeof

def GetHumanReadable(size, precision=2):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1  # increment the index of the suffix
        size = size/1024.0  # apply the division
    return "%.*f%s" % (precision, size, suffixes[suffixIndex])

w = clintest.Worker()
w.load('examples/pathfinding/tests.json')
w.run()

# print(GetHumanReadable(asizeof.asizeof (w.tests[0].solvers[0].persistant_model)))
