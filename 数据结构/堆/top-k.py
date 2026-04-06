import heapq

# 求最大的 K 个元素 → 维护大小为 K 的最小堆，也就是每次会弹出最小的元素，保留最大的 K 个元素
def top_k(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)         # 弹出最小，保留最大 K 个
    return heap

# 数据流中位数（大根堆 + 小根堆）⭐⭐⭐
"""
为了高效地求解数据流中的中位数，可以将数据流分成两部分：

大根堆（lo）：保存较小的一半数字。

小根堆（hi）：保存较大的一半数字。

通过这两种堆的结合，可以确保：

大根堆中存储的数字最大值始终小于等于小根堆中的最小值。

每当我们需要找中位数时，可以根据堆的大小来决定中位数：

如果两个堆的大小相同，中位数是两个堆顶元素的平均值。

如果大根堆比小根堆多一个元素，中位数就是大根堆的堆顶元素。
"""
class MedianFinder:
    def __init__(self):
        self.lo = []   # 最大堆（存较小半部分，取负模拟）
        self.hi = []   # 最小堆（存较大半部分）

    def add_num(self, num):
        # 由于 Python 的 heapq 默认是最小堆，因此通过将数字取负数来模拟最大堆的行为。
        # 也就是说，负数的堆顶相当于正数堆中的最大值。
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))    # 将 lo 的堆顶元素（即最大的那个）弹出并加入 hi，保持两边平衡
        if len(self.hi) > len(self.lo):
            # 如果 hi 的元素比 lo 多了一个，那么就把 hi 的堆顶元素（即最小的那个）弹出并加入 lo，保持两边平衡
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def find_median(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2