
from lace.logging import trace
from flange import utils
from flange.primitives.ops import _operation


@trace.info("svg")
def create_path(path):
    rules = []
    for i, (ty, element) in enumerate(path):
        if i == 0 or i == len(path) - 1:
            rules.append((element, ""))
        if ty in ['node', 'function']:
            if ty == 'function':
                name, element, body = item
                rules.append((element, "register stream process - {}".format(name)))
        if i != 0 and i != len(path) - 1 and ty == 'node':
            rules.append((element, "l4_src: {}\nl4_dst: {}\nFORWARD\n> PORT {} TO {}".format(path[1][1].address.address,
                                                                                             path[-2][1].address.address,
                                                                                             path[i -1][1].index, path[i + 1][1].index)))
    return rules

@trace.info("svg")
def run(program):
    rules = []
    
    if not utils.runtime().graph.processing_level:
        utils.runtime().graph.spring(25, 50)
    
    for op in program:
        if not isinstance(op, _operation):
            raise SyntaxError("Operation cannot be resolved into graph")
        for delta in op.__fl_next__():
            for element in delta:
                if element[0] == "node":
                    if hasattr(element[1], "virtual") and element[1].virtual:
                        for n in element[1]._members:
                            rules.append([(n, "")])
                    else:
                        rules.append([(element[1], "")])
                elif element[0] == "flow":
                    rules.append(create_path(element[1:]))
                    
            break
    return utils.runtime().graph.svg(rules)
