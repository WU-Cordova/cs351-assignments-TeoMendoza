import pytest
from datastructures.avltree import AVLTree

class TestAVLDeletes():
    @pytest.fixture
    def avltree(self) -> AVLTree: return AVLTree[int, int]([(8, 8), (9, 9), (10, 10), (2, 2), (1, 1), (5, 5), (3, 3), (6, 6), (4, 4), (7, 7)])

    def test_delete_root(self, avltree: AVLTree) -> None:
        avltree.delete(5)
        assert avltree.inorder() == [1, 2, 3, 4, 6, 7, 8, 9, 10]

    def test_delete_leaf(self, avltree: AVLTree) -> None:
        avltree.delete(10)
        assert avltree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_delete_node_with_one_child(self, avltree: AVLTree) -> None:
        avltree.delete(3)
        assert avltree.inorder() == [1, 2, 4, 5, 6, 7, 8, 9, 10]

    def test_delete_node_with_two_children(self, avltree: AVLTree) -> None:
        avltree.delete(2)
        assert avltree.inorder() == [1, 3, 4, 5, 6, 7, 8, 9, 10]
        