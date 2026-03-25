# - BFS **必须在入队时标记已访问**，不能在出队时标记（否则重复入队）
# - 循环队列判满：`(rear + 1) % cap == front`（留一个空位区分空和满）

from collections import deque

def bfs(start):
    """广度优先搜索（BFS）模板：用一个队列来维护"下一层要访问的节点"，每次访问一个节点时，把它的所有未访问过的邻居都加入队列。"""
    q = deque([start])
    visited = set([start])

    while q:
        cur = q.popleft()

        for nxt in neighbors(cur):
            if nxt not in visited:
                visited.add(nxt)
                q.append(nxt)

def multi_source_bfs(grid):
    """多源 BFS 模板：当 BFS 有多个起点时，可以把它们同时入队，距离矩阵 dist 中对应位置的值初始化为 0。"""
    m, n = len(grid), len(grid[0])
    dist = [[-1]*n for _ in range(m)]   # -1 表示未访问
    q = deque()

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                q.append((i, j))
                dist[i][j] = 0          # 起点距离为 0

    while q:
        x, y = q.popleft()
        for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if 0<=nx<m and 0<=ny<n and dist[nx][ny]==-1:  # ← 缺少的 visited 判断
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))

    return dist

from collections import deque

def orangesRotting(grid):
    m, n = len(grid), len(grid[0])
    dist = [[-1]*n for _ in range(m)]
    q = deque()
    fresh = 0

    # 1. 初始化：所有腐烂橘子同时入队
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:
                q.append((i, j))
                dist[i][j] = 0       # 腐烂起点，时间为 0
            elif grid[i][j] == 1:
                fresh += 1           # 统计新鲜橘子数量

    # 2. 多源 BFS 扩展
    while q:
        x, y = q.popleft()
        for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if 0<=nx<m and 0<=ny<n and dist[nx][ny]==-1:
                dist[nx][ny] = dist[x][y] + 1
                fresh -= 1           # 每感染一个，新鲜数 -1
                q.append((nx, ny))

    # 3. 判断结果
    if fresh > 0:
        return -1                    # 还有新鲜橘子无法感染（被空格隔断）
    return max(dist[i][j] for i in range(m) for j in range(n) if dist[i][j] >= 0)


# 滑动窗口最大值（单调队列）⭐⭐⭐
def max_sliding_window(nums, k):
    """给定一个数组 nums 和滑动窗口的大小 k，请找出所有滑动窗口里的最大值。
    用一个 单调递减队列（deque）来维护"当前窗口内可能成为最大值的候选下标"。"""
    dq = deque()          # 存下标，队列内值单调递减
    res = []
    for i, v in enumerate(nums):
        while dq and nums[dq[-1]] < v:  # 维护单调性
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:             # 队头超出窗口
            dq.popleft()
        if i >= k - 1:
            res.append(nums[dq[0]])    # 队头就是最大值
    return res


def zero_one_bfs(start):
    dq = deque([start])
    dist = {start: 0}

    while dq:
        cur = dq.popleft()

        for nxt, w in graph[cur]:
            if dist[cur] + w < dist.get(nxt, float('inf')):     # 如果通过 cur 到 nxt 的距离更短
                dist[nxt] = dist[cur] + w
                # 边权为 0 → nxt 与 cur 距离相同 → 插入队头，优先处理
                # 边权为 1 → nxt 距离更大 → 插入队尾，稍后处理
                if w == 0:
                    dq.appendleft(nxt)
                else:
                    dq.append(nxt)


def level_order(root):
    """给定一个二叉树，返回其节点值的层序遍历（即逐层地，从左到右访问所有节点）。"""
    if not root: return []

    q = deque([root])
    res = []

    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)

        res.append(level)

    return res

