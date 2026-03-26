from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

# 迭代中序遍历（面试最常考）⭐⭐⭐
def inorder(root):
    stack, res, curr = [], [], root
    while curr or stack:
        while curr:                     # 一路向左
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.val)
        curr = curr.right               # 转向右子树
    return res

# 递归写法
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# 层序遍历 BFS ⭐⭐⭐
def level_order(root):
    if not root: return []
    q, res = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):         # 每轮处理一层
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res

def build_tree(preorder, inorder):
    """根据前序和中序构建二叉树
    中序负责"划分左右"，前序负责"确定根节点"
    """
    if not preorder: return None
    root_val = preorder[0]
    idx = inorder.index(root_val)       # 中序中根的位置
    root = TreeNode(root_val)
    root.left  = build_tree(preorder[1:1+idx], inorder[:idx])
    root.right = build_tree(preorder[1+idx:],  inorder[idx+1:])
    return root


def dfs(root):
    """DFS（深度优先搜索）框架"""
    if not root:
        return

    # 1. 处理当前节点（前序）
    
    dfs(root.left)

    # 2. 处理中间（中序）

    dfs(root.right)

    # 3. 处理当前节点（后序）

def isBalanced(root):
    """判断二叉树是否平衡：任意节点的左右子树高度差不超过1"""
    def height(node):
        if not node: return 0
        l = height(node.left)
        r = height(node.right)
        if l == -1 or r == -1 or abs(l - r) > 1:
            return -1
        return 1 + max(l, r)
    return height(root) != -1


def lowestCommonAncestor(root, p, q):
    """寻找二叉树的最近公共祖先：
    如果当前节点是p或q，直接返回；
    否则在左右子树中分别寻找，如果两边都找到了，说明当前节点就是最近公共祖先；
    如果只找到一边，说明最近公共祖先在那一边。"""
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    if left and right:
        return root
    return left if left else right