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

    def print(self):
        print(str(self))

    def __lt__(self, other):
        return self.weight() < other.weight()

    def __str__(self) -> str:
        return f"Leaf: `{self.value}`"

class Node(TreeNodeTraits):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def weight(self):
        return self.left.weight() + self.right.weight()

    def __str__(self) -> str:
        return f"[ Node, left: {str(self.left)}; right: {str(self.right)} ]"

    def print(self):
        print(str(self))
        self.left.print()
        self.right.print()

    def __lt__(self, other):
        return self.weight() < other.weight()


def tree_from_list(occurence_list: list[TreeNodeTraits]) -> Node:
    occurence_list = sorted(occurence_list)

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

    def __str__(self) -> str:
        return f"Tree:\n\tleft: {str(self.root_node.left)}\n\tright: {str(self.root_node.right)}"

def climb(tree, trace="", result=[]):
    (_left, _right) = tree.children()
    left_none, right_none = False, False

    match _left:
        case Leaf():
            result.append((_left.value, trace))
            tree = None
        case Node():
            new_trace = trace + "0"
            climb(_left, new_trace, result)
        case None:
            left_none = True

    match _right:
        case Leaf():
            result.append((_right.value, trace))
            tree = None
        case Node():
            new_trace = trace + "1"
            climb(_right, new_trace, result)
        case None:
            right_none = True

    if left_none and right_none:
        tree = None

def clean_input(input) -> str:
    result = input.lower()
    # FIXME: da fehlen noch ein paar
    result = result.strip("-,!$^:;.?/\\|")
    return result

def input_from_file(path) -> str:
    file = open(path)
    contents = file.read()
    return clean_input(contents)

def main():
    input = input_from_file('./res/paragraph1.txt')
    tree = Tree(input)

    out = []
    climb(tree, result=out)
    print(out)

if __name__ == "__main__":
    main()
