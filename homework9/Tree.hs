module Tree where

import Prelude hiding(lookup)

data BinaryTree k v = None | Node{
	key		:: k
  ,	value	:: v
  ,	l		:: BinaryTree k v
  ,	r		:: BinaryTree k v
}

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k None = Nothing
lookup k t = if k == (key t)
	then Just (value t)
	else if k < (key t)
		then (lookup k (l t))
		else (lookup k (r t))

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v None = Node k v None None
insert k v t = if k == (key t)
	then Node k v (l t) (r t)
	else if k < (key t)
		then Node (key t) (value t) (insert k v (l t)) (r t)
		else Node (key t) (value t) (l t) (insert k v (r t))

delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k None = None
delete k t = if k == (key t)
	then merge (l t) (r t)
	else if k < (key t)
		then Node (key t) (value t) (delete k (l t)) (r t)
		else Node (key t) (value t) (l t) (delete k (r t))
 

merge :: BinaryTree k v -> BinaryTree k v -> BinaryTree k v
merge None b = b
merge a None = a
merge a b = Node (key b) (value b) (merge a (l b)) (r b)
