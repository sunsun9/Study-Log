class MinHeap:
    def __init__(self):
        self.h = []

    def push(self, val):
        """向堆中添加元素，保持堆的性质"""
        self.h.append(val)      # 先添加到末尾，即堆的底层的最右边
        self._sift_up(len(self.h) - 1)      # 调用 _sift_up 操作来将新插入的元素上浮到正确的位置

    def pop(self):
        """从堆中删除并返回最小元素（堆顶），保持堆的性质"""
        self.h[0], self.h[-1] = self.h[-1], self.h[0]   # 将堆顶元素与堆底元素交换
        val = self.h.pop()   # 删除堆底元素（原堆顶元素），并保存要返回的值
        if self.h: self._sift_down(0)   # 如果堆不空了，调用 _sift_down 操作来将新的堆顶元素下沉到正确的位置
        return val

    def _sift_up(self, i):
        """从下到上调整堆，使得堆的性质得到满足"""
        while i > 0:
            p = (i - 1) // 2    # 父节点的索引
            if self.h[p] > self.h[i]:
                # 插入的值比父节点小，交换它们，即上浮
                self.h[p], self.h[i] = self.h[i], self.h[p]
                i = p
            else: break

    def _sift_down(self, i):
        """从上到下调整堆，使得堆的性质得到满足"""
        n = len(self.h)
        while True:
            smallest = i
            for c in [2*i+1, 2*i+2]:
                # 遍历堆顶节点的左右子节点，找到最小的那个
                if c < n and self.h[c] < self.h[smallest]:
                    smallest = c    # 记录最小元素的索引
            if smallest == i: break
            self.h[i], self.h[smallest] = self.h[smallest], self.h[i]   # 交换堆顶元素与最小元素，即下沉
            i = smallest