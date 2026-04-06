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
    res = []
    def dfs(node):
        if not node: return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res

# 层序遍历 BFS ⭐⭐⭐
def level_order(root):
    if not root: return []
    q, res = deque([root]), []
    while q:
        level = []
        for _ in range(len(q)):         # 每轮处理一层
            node = q.popleft()
            level.append(node.val)      # 记录当前层的所有节点
            if node.left:  q.append(node.left)      # 把该层节点的子节点加入队列，下一轮就能处理下一层了
            if node.right: q.append(node.right)
        res.append(level)
    return res

def rightSideView(root):
    """返回二叉树的右视图：每层最右边的节点"""
    # 与上面层序遍历的思路一致，res存放每层最右边的节点，按照层序遍历的方式访问
    if not root: return []
    q = deque([root])
    res = []

    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i == size - 1:
                res.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)

    return res

def build_tree(preorder, inorder):
    """根据前序和中序构建二叉树
    中序负责"划分左右"，前序负责"确定根节点"
    """
    # 核心步骤：1.利用前序获取根节点，2.利用中序获取左子树大小，3.递归构建左右子树
    idx_map = {v:i for i,v in enumerate(inorder)}

    def helper(pl, pr, il, ir):
        if pl > pr:
            return None

        root_val = preorder[pl]     # 前序的第一个元素是根节点
        root = TreeNode(root_val)   # 创建根节点
        idx = idx_map[root_val]     # 找到中序中根节点的位置
        left_size = idx - il        # 左子树的大小

        root.left = helper(pl+1, pl+left_size, il, idx-1)
        root.right = helper(pl+left_size+1, pr, idx+1, ir)

        return root

    return helper(0, len(preorder)-1, 0, len(inorder)-1)

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
    left = lowestCommonAncestor(root.left, p, q)    # 在左边找
    right = lowestCommonAncestor(root.right, p, q)  # 在右边找  

    if left and right:
        return root
    return left if left else right

def isValidBST(root):
    """判断二叉树是否为有效的二叉搜索树（BST）
    每个节点都必须在一个 (low, high) 范围内
    """
    def helper(node, low, high):
        if not node: return True
        if not (low < node.val < high):
            return False
        return (helper(node.left, low, node.val) and
                helper(node.right, node.val, high))
    return helper(root, float('-inf'), float('inf'))    # 从根节点开始，这里是初始范围

def kthSmallest(root, k):
    """寻找二叉搜索树中第 k 小的元素
    中序遍历有序二叉树
    """
    stack = []
    while True:
        while root:
            # 一直找到最左边的节点，沿途把节点都压入栈中
            stack.append(root)
            root = root.left
        root = stack.pop()
        k -= 1
        if k == 0:
            return root.val
        root = root.right   # 这一步也比较关键

def invertTree(root):
    """反转二叉树"""
    if not root: return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root

def hasPathSum(root, target):
    """判断二叉树是否存在从根节点到叶子节点的路径，使得路径上的节点值之和等于目标值"""
    if not root: return False
    if not root.left and not root.right:
        return target == root.val
    return (hasPathSum(root.left, target-root.val) or
            hasPathSum(root.right, target-root.val))

def binaryTreePaths(root):
    """返回二叉树中所有从根节点到叶子节点的路径"""
    res = []

    def dfs(node, path):
        if not node: return

        path.append(str(node.val))

        if not node.left and not node.right:
            # 左右子节点都为空，说明走到了终点，把 path 里的所有值用 -> 拼接起来，存进结果
            res.append("->".join(path))
        else:
            dfs(node.left, path)
            dfs(node.right, path)

        path.pop()   # 撤销当前节点，回到上一个节点，继续探索其他路径

    dfs(root, [])
    return res

def diameterOfBinaryTree(root):
    """计算二叉树的直径：任意节点的左右子树高度之和的最大值"""
    res = 0     # 记录最大直径，也就是到目前为止最大路径是多少

    def depth(node):
        nonlocal res        # 声明使用外部变量
        if not node: return 0
        l = depth(node.left)
        r = depth(node.right)
        res = max(res, l + r)
        return 1 + max(l, r)    # 返回当前节点的高度，供父节点计算直径使用

    depth(root)
    return res


"""参考模版"""
def dfs(root):
    """深度优先搜索（DFS）框架"""
    if not root:
        return

    # 前序位置（进节点）
    
    dfs(root.left)

    # 中序位置
    
    dfs(root.right)

    # 后序位置（离开节点）

def dfs(root):
    """深度优先搜索（DFS）框架"""
    if not root:
        return 0   # 根据题目定义

    left = dfs(root.left)
    right = dfs(root.right)

    # 在这里做逻辑（核心）
    
    return 某个值

def func(root):
    """全局变量+回传"""
    res = 0

    def dfs(node):
        nonlocal res
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)

        # 更新全局结果
        res = max(res, 某种计算)

        return 某个值

    dfs(root)
    return res


def bfs(root):
    """广度优先搜索（BFS）框架"""
    if not root:
        return []

    q = deque([root])
    res = []

    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)

            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        res.append(level)

    return res


