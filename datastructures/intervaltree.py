from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Any, Optional
from datastructures.avltree import AVLTree


class IntervalNode:
    def __init__(self, key: int, max_end: int, value: str):
        self.key: int = key # high
        self.value: Any = value
        self.max_end: int = max_end
        self.duplicates: AVLTree = AVLTree()
    

class IntervalTree:
    def __init__(self):
        self._tree = AVLTree()

    def insert(self, low: int, high: int, value: str):
        node: IntervalNode = self._tree.search(low)
        if node:
            node.duplicates.insert(high, value)
        else:
            new_node = IntervalNode(high, high, value)
            new_node.duplicates.insert(high, value)
            self._tree.insert(low, new_node)
        
        self.update_max_end(self._tree.root)
    
    def update_max_end(self, node) -> int:
        if not node:
            return 0
        left_max = self.update_max_end(node.left)
        right_max = self.update_max_end(node.right)
        node.value.max_end = max(left_max, right_max, node.value.key)
        return node.value.max_end
    
    def delete(self, low, high):
        self.delete_helper(node = self._tree.root, low=low, high=high)

    def delete_helper(self, node, low, high):
        if not node:
            return
        if node.key == low: # have found area in tree where node is
            if node.value.key == high: # is primary node?
                if node.value.duplicates.root is None: # check duplicates empty
                    self._tree.delete(low)
                else: # if not empty
                    duplicate = node.value.duplicates.root # get root
                    node.value.duplicates.root = node.value.duplicates.delete(duplicate.key)
                    node.value = IntervalNode(duplicate.key, duplicate.key, duplicate.value) # set primary node value to root value
            else:
                node.value.duplicates.delete(high) # otherwise, its in duplicates, so delete from duplicates, if not, itll just return none and be fine

        elif node.key > low:
            self.delete_helper(node.left, low, high)
        else:
            self.delete_helper(node.right, low, high)

        self.update_max_end(node)
        
    def top_k(self, k: int):
        
        return self.top_k_helper(k)

    def top_k_helper(self, k: int):
        result = self._tree.inorder()
        return result[-k:]

    def bottom_k(self, k: int):
        return self.bottom_k_helper(k)
    
    def bottom_k_helper(self, k: int):
        result = self._tree.inorder()
        return result[:k]
            
    def range_query(self, low: int, high: int):
        result = []
        self.range_query_helper(self._tree.root, low, high, result)
        return result

    def range_query_helper(self, node, low: int, high: int, result: list):
        if not node:
            return

        # Early return conditions
        if node.value.max_end < low:  # If the maximum end is less than low, skip this subtree
            return

        # Check if the current node overlaps with the range
        if node.key <= high and node.value.key >= low:
            self.range_query_helper(node.left, low, high, result)
            result.append(node.value.value)  # List will be inorder
            self.range_query_helper(node.right, low, high, result)
        
        if node.left and node.left.value.max_end >= low:
            self.range_query_helper(node.left, low, high, result)
        
        if node.key <= high:
            self.range_query_helper(node.right, low, high, result)

        

    


        
        