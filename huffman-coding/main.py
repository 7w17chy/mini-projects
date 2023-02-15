from abc import ABC, abstractmethod

class TreeNodeTraits(ABC):
    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def weight(self):
        pass

    def __lt__(self, other):
        return self.weight() < other.weight()

class Leaf(TreeNodeTraits):
    def __init__(self, value, weight):
        self.value = value
        self._weight = weight

    def weight(self):
        return self._weight

    def __str__(self) -> str:
        return "%s" % self.value

    def print(self):
        print(str(self))

    def __lt__(self, other):
        return self.weight() < other.weight()

class Node(TreeNodeTraits):
    def __init__(self, left, right):
        # minimum
        self.left = left
        # second minimum
        self.right = right

    def children(self):
        return (self.left, self.right)

    def weight(self):
        return self.left.weight() + self.right.weight()

    def __str__(self) -> str:
        return "%_%" % (self.left, self.right)

    def print(self):
        print(str(self))
        self.left.print()
        self.right.print()

    def __lt__(self, other):
        return self.weight() < other.weight()


def tree_from_list(occurence_list: list[TreeNodeTraits]) -> Node:
    occurence_list = sorted(occurence_list, reverse=True)

    if len(occurence_list) >= 3:
        left, right, *rest = occurence_list
        new_node = Node(left, right) 
        rest.append(new_node)
        return tree_from_list(rest)
    else:
        # Those are the final two nodes that make up the tree root
        left, right = occurence_list
        return Node(left, right)

def count_occurences(input) -> dict[str, int]:
    occurence_count = dict()
    for element in input:
        if element in occurence_count:
            occurence_count.update({element: occurence_count[element] + 1})
        else:
            occurence_count[element] = 0

    return occurence_count

def make_leafs(occurrence_map) -> list[TreeNodeTraits]:
   result: list[TreeNodeTraits] = []
   for element, occurrence in occurrence_map.items():
       new_node = Leaf(element, occurrence)
       result.append(new_node)

   return result

class Tree:
    def __init__(self, input):
        self.occurences = count_occurences(input)
        tree_construction_list = make_leafs(self.occurences.copy())
        self.root_node = tree_from_list(tree_construction_list)

    def children(self):
        return self.root_node.children()

def climb(tree, result = ("", "")) -> tuple[str, str]:
    (element, trace) = result
    match tree:
        case Leaf():
            element = tree.value
            tree = None
            return (element, trace)
        case Node():
            (_left, _right) = tree.children()

            match _left:
                case Node():
                    trace = trace + "0"
                    return climb(_left.left, result = ("", trace))
                case Leaf():
                    element = _left.value
                    tree.left = None
                    return (element, trace)
                case None:
                    pass

            match _right:
                case Node():
                    trace = trace + "1"
                    return climb(_right.right, result = ("", trace))
                case Leaf():
                    element = _right.value
                    tree.right = None
                    return (element, trace)
                case None:
                    pass

            if tree.left == None and tree.right == None:
                tree = None

    return result

def tree_to_table(tree) -> dict[str, str]:
    work_queue = list(tree.occurences)
    result = dict()

    while work_queue:
        (element, trace) = climb(tree)
        result[element] = trace

        if not element in work_queue:
            print(f"Atempting to remove element `${element}` which is not in work_queue")
        work_queue.remove(element)

    return result

def main():
    input = 'aaaabbbcccdde'
    tree = Tree(input)
    table = tree_to_table(tree)
    print(table["a"])

main()
