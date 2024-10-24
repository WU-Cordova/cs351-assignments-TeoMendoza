import pytest

from datastructures.intervaltree import IntervalTree
from datastructures.avltree import AVLTree
from datastructures.avltree import AVLNode
from datastructures.intervaltree import IntervalNode

class TestIntervalTree:
    @pytest.fixture
    def intervaltree(self) -> IntervalTree:
        tree = IntervalTree()

    def test_insert(self, intervaltree):
        tree = IntervalTree()
        tree.insert(7,10, "A")
        tree.insert(5,15, "B")
        tree.insert(10,20, "C")
        tree.insert(7,15, "D")
        assert tree._tree.size_avl() == 3
        assert tree._tree.root.value.duplicates.size_avl()==2

    def test_find_nodes_between(self, intervaltree):
        tree = IntervalTree()
        tree.insert(7,10, "A")
        tree.insert(5,15, "B")
        tree.insert(10,20, "C")
        tree.insert(7,15, "D")
        nodes_selected = tree.range_query(5,15)
        assert set(nodes_selected) == set(["A","B","C"])

    def test_find_nodes_overlapping(self, intervaltree):
        tree = IntervalTree()
        tree.insert(7,10, "A")
        tree.insert(5,15, "B")
        tree.insert(10,20, "C")
        tree.insert(7,15, "D")
        tree.insert(40,50, "E")
        nodes_selected = tree.range_query(15,30)

        assert set(nodes_selected) == set(["C","B"])

    def test_top_k(self, intervaltree):
        tree = IntervalTree()
        tree.insert(7,10, "A")
        tree.insert(5,15, "B")
        tree.insert(10,20, "C")
        tree.insert(7,15, "D")
        tree.insert(40,50, "E")
        top_k = tree.top_k(2)
        assert top_k == [10,40]

    def test_bottom_k(self, intervaltree):
        tree = IntervalTree()
        tree.insert(7,10, "A")
        tree.insert(5,15, "B")
        tree.insert(10,20, "C")
        tree.insert(7,15, "D")
        tree.insert(40,50, "E")
        bottom_k = tree.bottom_k(2)
        assert bottom_k == [5, 7]
    
    def test_delete(self, intervaltree):
        tree = IntervalTree()
        tree.insert(7,10, "A")
        tree.insert(5,15, "B")
        tree.insert(10,20, "C")
        tree.insert(7,15, "D")

        tree.delete(7,10)
        assert tree._tree.size_avl() == 3
        assert tree._tree.root.value.duplicates.size_avl()==0