import math


class Node:
    def __init__(self, word, right, left):
        self.word = word
        self.left = left
        self.right = right


def tree_size(node):
    if node is None:
        return 0
    else:
        return (tree_size(node.left) + 1 + tree_size(node.right))


def findPath(root, path, k):
    # Baes Case
    if root is None:
        return False

    # Store this node is path vector. The node will be
    # removed if not in path from root to k
    path.append(root.key)

    # See if the k is same as root's key
    if root.key == k:
        return True

    # Check if k is found in left or right sub-tree
    if ((root.left != None and findPath(root.left, path, k)) or
            (root.right != None and findPath(root.right, path, k))):
        return True

    # If not present in subtree rooted with root, remove
    # root from path and return False

    path.pop()
    return False


def findLCA(root, n1, n2):
    # To store paths to n1 and n2 fromthe root
    path1 = []
    path2 = []

    # Find paths from root to n1 and root to n2.
    # If either n1 or n2 is not present , return -1
    if (not findPath(root, path1, n1) or not findPath(root, path2, n2)):
        return -1

    # Compare the paths to get the first different value
    i = 0
    while (i < len(path1) and i < len(path2)):
        if path1[i] != path2[i]:
            break
        i += 1
    return path1[i - 1]


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


def get_p_c(current, root):
    return tree_size(current) / tree_size(root)


def sim_lin(node1, node2, root):
    return (
            2 * get_p_c(findLCA(root, node1, node2), root) /
            (math.log(get_p_c(node1, root)) + math.log(get_p_c(node2, root)))
            )


if __name__ == '__main__':
    rock_root = create_tree()
