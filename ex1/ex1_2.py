import math


class Node:
    def __init__(self, word, right, left):
        self.word = word
        self.left = left
        self.right = right


def lowestCommonAncestor(root, p, q):
    if not root:
        return None
    if root.word == p or root.word == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if right and left:
        return root
    return right or left
    return left_subtree


def get_word_frequency(word):
    file = open("./corpus_ex1.freq_list", "r")
    invalid_word = 1
    for line in file:
        line_data = line.split()
        if line_data[0] == word.lower():
            return int(line_data[1])
    return invalid_word


def create_tree():
    treasure = Node('treasure', None, None)
    muffin = Node('muffin', None, None)

    gem = Node('gem', treasure, muffin)

    capacity = Node('capacity', None, None)
    hell = Node('hell', None, None)
    fossa = Node('fossa', None, None)

    pit = Node('pit', capacity, hell)

    stone = Node('stone', pit, gem)

    debate = Node('debate', None, None)
    controversy = Node('controversy', None, None)

    disputation = Node('disputation', debate, controversy)

    joust = Node('joust', None, None)

    tilt = Node('tilt', disputation, joust)

    rock = Node('rock', stone, tilt)

    return rock


def Print_Tree(root):
    if root is None:
        return
    Print_Tree(root.left)
    print(root.data)
    Print_Tree(root.right)


def lin_on_node(node, node2, all_tree_size, root):
    if node2 is None:
        return
    lin_on_node(node, node2.left, all_tree_size, root)
    print("Lin on: " + str(node.word) + " & " + str(node2.word))
    print(sim_lin(node, node2, all_tree_size, root))
    print()
    lin_on_node(node, node2.right, all_tree_size, root)


def lin_on_tree(node, root, all_tree_size):
    if node is None:
        return
    lin_on_tree(node.left, root, all_tree_size)
    lin_on_node(node, root, all_tree_size, root)
    lin_on_tree(node.right, root, all_tree_size)


def get_p_c(current, all_tree_freq):
    return get_all_tree_frequency(current) / all_tree_freq


def sim_lin(node1, node2, all_tree_freq, root):
    lca = lowestCommonAncestor(root, node1.word, node2.word)
    up = 2 * math.log(get_p_c(lca, all_tree_freq))
    down = math.log(get_p_c(node1, all_tree_freq)) + \
        math.log(get_p_c(node2, all_tree_freq))
    if down == 0:
        return 0
    return up / down


def get_all_tree_frequency(root):
    if root is None:
        return 0
    return get_word_frequency(root.word) + get_all_tree_frequency(root.right) + get_all_tree_frequency(root.left)


if __name__ == '__main__':
    rock_root = create_tree()
    all_tree_freq = get_all_tree_frequency(rock_root)
    lin_on_tree(rock_root, rock_root, all_tree_freq)

# We took the tree written on create_tree function
# We applied lin similarity on every 2 nodes in the tree
# We will discus on 5 combinations:

# makes more sense:
# treasure & gem more similar than treasure & stone -> Gem is consider treasure but stone is not
#  controversy & disputation more similar than controversy & debate -> controversy & disputation are similar words, debate has different semantic field.
# hell & pit more similar than hell & stone -> Known prase is "pit of hell" and hell considered to be underground, stone is not something hell relative.
# stone & pit more similar pit & muffin -> Pit can be fills with stone, but not with muffins (and its a shame)
# muffin & gem more similar than muffin & hell -> Muffin is a gem, not hell.

# We asked Gaya, Literature and Psychology student, which really like psycholinguistics (If you looking for researcher and so) and she agree with me
# about all accept controversy & disputation VS controversy & debate. She think that debate is in the same semantic field and its looks strage that there is
# any difference in the similarities
