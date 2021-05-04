import math


class Node:
    def __init__(self, word, lst):
        self.word = word
        self.children = lst


def get_tree_size(root):
    if root.children is None:
        return 1
    node = 1
    for child in root.children:
        node = node + get_tree_size(child)
    return node


def create_tree():
    treasure = Node('treasure', None)
    muffin = Node('muffin', None)

    gem = Node('gem', [treasure, muffin])

    capacity = Node('capacity', None)
    hell = Node('hell', None)
    fossa = Node('fossa', None)

    pit = Node('pit', [capacity, fossa, hell])

    stone = Node('stone', [pit, gem])

    debate = Node('debate', None)
    controversy = Node('controversy', None)

    disputation = Node('disputation', [debate, controversy])

    joust = Node('joust', None)

    tilt = Node('tilt', [disputation, joust])

    rock = Node('rock', [stone, tilt])

    return rock


def get_p_c(current, root):
    return get_tree_size(current) / get_tree_size(root)


def get_i_c(current, root):
    return -math.log(get_p_c(current, root))


def sim_lin(current, root):
    pass


if __name__ == '__main__':
    root = create_tree()
    print(get_tree_size(root))
