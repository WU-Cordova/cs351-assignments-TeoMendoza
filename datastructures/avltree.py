from __future__ import annotations
from collections import deque
from datastructures.iavltree import IAVLTree, K, V
from typing import Callable, Generic, List, Optional, Sequence, Tuple


class AVLNode(Generic[K, V]):
   def __init__(self, key: K, value: V, left: Optional[AVLNode[K, V]]=None, right: Optional[AVLNode[K, V]]=None):
      self._key = key
      self.value = value
      self.height = 1
      self.left = left
      self.right = right

   @property
   def key (self) -> K:
      return self._key
   
   @key.setter
   def key(self, new_key: K) -> None:
      self._key = new_key
      

class AVLTree(IAVLTree[K, V], Generic[K, V]):

   def __init__(self, starting_sequence: Optional[Sequence[Tuple]] = None):
      self.root = None
      self.size = 0

      for key, value in starting_sequence or []:
         self.insert(key, value)

   def insert(self, key: K, value: V) -> None:
      self.root = self.insert_helper(self.root, key, value)

   def insert_helper(self, node: Optional[AVLNode], key: K, value: V) -> AVLNode:
      if node is None:
         return AVLNode(key, value)
      elif key < node.key:
         node.left = self.insert_helper(node.left, key, value)
      else:
         node.right = self.insert_helper(node.right, key, value)

      node.height = 1 + max(node.left.height if node.left else 0, node.right.height if node.right else 0)

      if (node.left.height if node.left else 0) - (node.right.height if node.right else 0) > 1:
         left_child = node.left
         right_child = node.right
         if (left_child.left.height if node.left else 0) - (left_child.right.height if node.right else 0) >= 0:
            return self.rotate_right(node)
         else:
            node.left = self.rotate_left(left_child)
            return self.rotate_right(node)
         
      elif (node.left.height if node.left else 0) - (node.right.height if node.right else 0) < -1:
         left_child = node.left
         right_child = node.right
         if (right_child.left.height if node.left else 0) - (right_child.right.height if node.right else 0) <= 0:
            return self.rotate_left(node)
         else:
            node.right = self.rotate_right(right_child)
            return self.rotate_left(node)

      return node
   
   def rotate_right(self, node: AVLNode) -> AVLNode:
      left_child = node.left
      left_subtree = left_child.right
      left_child.right = node
      node.left = left_subtree

      left_child.height = 1 + max(
        (left_child.left.height if left_child.left is not None else 0), 
        (left_child.right.height if left_child.right is not None else 0)
      )

      node.height = 1 + max(
         (node.left.height if node.left is not None else 0), 
         (node.right.height if node.right is not None else 0)
      )

      return left_child
      
   def rotate_left(self, node: AVLNode) -> AVLNode:
      right_child = node.right
      right_subtree = right_child.left
      right_child.left = node
      node.right = right_subtree

      right_child.height = 1 + max(
        (right_child.left.height if right_child.left is not None else 0), 
        (right_child.right.height if right_child.right is not None else 0)
      )

      node.height = 1 + max(
         (node.left.height if node.left is not None else 0), 
         (node.right.height if node.right is not None else 0)
      )

      return right_child
   
   def search(self, key: K) -> Optional[V]:
      return self.search_helper(self.root, key)

   def search_helper(self, node: Optional[AVLNode], key: K) -> Optional[V]:
      if node is None:
         return None
      elif node.key == key:
         return node.value
      elif key < node.key:
         self.search_helper(node.left, key)
      else:
         self.search_helper(node.right, key)

   def delete(self, key: K) -> None:
      self.root = self.delete_helper(self.root, key)
        
   def delete_helper(self, node: Optional[AVLNode], key: K) -> AVLNode | None:
      if node is None:
         raise KeyError(f"Key {key} not found in the tree.")
      elif key < node.key:
         node.left = self.delete_helper(node.left, key)
      elif key > node.key:
         node.right = self.delete_helper(node.right, key)
      else:
         if node.left is None and node.right is None:
               return None
         elif node.left is None:
               node = node.right
         elif node.right is None:
               node = node.left
         else:
               successor = self.find_min(node.right)
               node.key = successor.key
               node.value = successor.value
               node.right = self.delete_helper(node.right, successor.key)

      node.height = max(node.left.height if node.left else 0, node.right.height if node.right else 0) - 1

      if (node.left.height if node.left else 0) - (node.right.height if node.right else 0) > 1:
         left_child = node.left
         right_child = node.right
         if (left_child.left.height if left_child.left else 0) - (left_child.right.height if left_child.right else 0) >= 0:
            return self.rotate_right(node)
         else:
            node.left = self.rotate_left(left_child)
            return self.rotate_right(node)
         
      elif (node.left.height if node.left else 0) - (node.right.height if node.right else 0) < -1:
         left_child = node.left
         right_child = node.right
         if (right_child.left.height if right_child.left else 0) - (right_child.right.height if right_child.right else 0) <= 0:
            return self.rotate_left(node)
         else:
            node.right = self.rotate_right(right_child)
            return self.rotate_left(node)
         
      return node 
   
   def find_min(self, node: AVLNode) -> AVLNode:
        while node.left is not None:
            node = node.left
        return node
   
   def inorder(self, visit: Optional[Callable[[V], None]]=None) -> List[K]:
      keys = []
      self.inorder_helper(self.root, keys)
      return keys
   
   def inorder_helper(self, node: Optional[AVLNode], keys: List[K]) -> None:
      if node is None:
         return None

      self.inorder_helper(node.left, keys)
      keys.append(node.key)
      self.inorder_helper(node.right, keys)

   def preorder(self, visit: Optional[Callable[[V], None]]=None) -> List[K]:
      keys = []
      self.preorder_helper(self.root, keys)
      return keys
   
   def preorder_helper(self, node: Optional[AVLNode], keys: List[K]) -> None:
      if node is None:
         return None

      keys.append(node.key)
      self.preorder_helper(node.left, keys)
      self.preorder_helper(node.right, keys)

   def postorder(self, visit: Optional[Callable[[V], None]]=None) -> List[K]:
      keys = []
      self.postorder_helper(self.root, keys)
      return keys

   def postorder_helper(self, node: Optional[AVLNode], keys: List[K]) -> None:
      if node is None:
         return None
        
      self.postorder_helper(node.left, keys)
      self.postorder_helper(node.right, keys)
      keys.append(node.key)

   def bforder(self, visit: Optional[Callable[[V], None]]=None) -> List[K]:
      keys = []
      dec = deque()
      self.bforder_helper(dec, self.root, keys)
      return keys
   
   def bforder_helper(self, dec: deque, node: Optional[AVLNode], keys: List[K]) -> None:
      if node is not None:
         dec.append(node)
      while dec:
         current = dec.popleft()
         keys.append(current.key)
         if current.left is not None:
            dec.append(current.left)
         if current.right is not None:
            dec.append(current.right)
      
   
   def size(self) -> int:
      return self.size_helper(self.root)
   
   def size_helper(self, node: Optional[AVLNode]) -> int:
      if node is None:
         return 0

      return 1 + self.size_helper(node.left) + self.size_helper(node.right)
   
   