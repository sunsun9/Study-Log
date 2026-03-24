class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    # ① 翻转链表（迭代，三指针）⭐⭐⭐
    def reverse(head):
        prev, curr = None, head
        while curr:
            nxt = curr.next   # 先存 next，防断链！
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    # ② 快慢指针：找中点 ⭐⭐⭐
    def find_mid(head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow  # 偶数长度时返回前半段末尾

    # ③ 判断环 + 找入口（Floyd 算法）⭐⭐⭐
    def detect_cycle(head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:          # 相遇，有环
                ptr = head
                while ptr != slow:    # 两指针同速，再次相遇即入口
                    ptr = ptr.next
                    slow = slow.next
                return ptr
        return None

    # ④ 合并两个有序链表 ⭐⭐⭐
    def merge_two(l1, l2):
        dummy = ListNode(0)
        cur = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                cur.next = l1; l1 = l1.next
            else:
                cur.next = l2; l2 = l2.next
            cur = cur.next
        cur.next = l1 or l2
        return dummy.next

    # ⑤ 删除倒数第 N 个节点（双指针）⭐⭐
    def remove_nth(head, n):
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n + 1):        # fast 先走 n+1 步
            fast = fast.next
        while fast:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next    # 跳过目标节点
        return dummy.next
    
    # 注：上述写的dummy是一种哑节点，这样不论后面怎么操作，最后返回dummy.next都能得到正确的链表头，避免了删除头节点等特殊情况的处理。


    def reverseKGroup(head, k):
        """每 k 个节点一组翻转链表，最后不足 k 个的保持原样。"""
        def reverse(a, b):
            prev, cur = None, a
            while cur != b:
                nxt = cur.next
                cur.next = prev
                prev = cur
                cur = nxt
            return prev

        a = b = head
        for _ in range(k):
            if not b:
                # 当剩余节点不足 k 个时（也就是还没走到k个，b就为None了），保持原样，直接返回当前 head
                return head
            b = b.next

        new_head = reverse(a, b)
        a.next = ListNode.reverseKGroup(b, k)
        return new_head


def swapPairs(head):
    """两两交换链表中的节点。要求只能修改节点本身，不能修改节点值。"""
    dummy = ListNode(0, head)
    cur = dummy

    while cur.next and cur.next.next:
        a = cur.next
        b = cur.next.next

        cur.next = b
        a.next = b.next
        b.next = a

        cur = a

    return dummy.next

def sortList(head):
    """对链表进行排序，要求时间复杂度 O(n log n)，空间复杂度 O(1)。
    核心思想：把链表分成两半，之后合并。分半用快慢指针，合并用 merge_two。（合并和排序是同时进行的）
    """
    if not head or not head.next:
        return head

    slow = fast = head
    prev = None
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next

    prev.next = None  # 断开

    l1 = sortList(head)
    l2 = sortList(slow)

    return ListNode.merge_two(l1, l2)


def isPalindrome(head):
    """判断链表是否是回文。要求时间复杂度 O(n)，空间复杂度 O(1)。"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 翻转后半段
    prev = None
    while slow:
        nxt = slow.next
        slow.next = prev
        prev = slow
        slow = nxt

    # 对比
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next

    return True


# LRU 缓存（最近最少使用）⭐⭐⭐
# 也就是一个固定容量的哈希表，超过容量时淘汰最久未使用的键值对。要求 get 和 put 都是 O(1)。
class LRUCache:
    """双向链表维护顺序，哈希表 O(1) 定位节点
    key 是"查询条件"，value 是"查询结果"
    用户输入 → 程序把输入处理成 key → 去缓存里查 → 返回 value 给用户
    """
    class Node:
        def __init__(self, k=0, v=0):
            self.key = k; self.val = v
            self.prev = self.next = None

    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}                 # key -> Node
        self.head = self.Node()         # 哑节点（最近使用端）
        self.tail = self.Node()         # 哑节点（最久未使用端）
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """删除链表中的 node"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):         # 插入到 head 后（最近）
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """访问一个键时，如果存在，则返回其值，并将该键提升为最近使用；如果不存在，则返回 -1。"""
        if key not in self.cache: return -1
        node = self.cache[key]
        self._remove(node)
        self._add_front(node)           # 移到最近位置
        return node.val

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = self.Node(key, value)
        self._add_front(node)
        self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.tail.prev        # 淘汰最久未使用
            self._remove(lru)
            del self.cache[lru.key]

from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.capacity  = capacity
        self.min_freq  = 0
        self.key_val   = {}     # key -> value
        self.key_freq  = {}     # key -> freq
        self.freq_keys = defaultdict(OrderedDict)       # freq -> keys（有序字典，保持访问顺序）

    def get(self, key):
        if key not in self.key_val:
            return -1
        self._inc_freq(key)
        return self.key_val[key]

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.key_val:
            self.key_val[key] = value
            self._inc_freq(key)
        else:
            if len(self.key_val) >= self.capacity:
                self._evict()
            self.key_val[key]      = value
            self.key_freq[key]     = 1
            self.freq_keys[1][key] = None   # 频率为 1 的键集合里添加新键
            self.min_freq          = 1

    def _inc_freq(self, key):
        freq = self.key_freq[key]
        del self.freq_keys[freq][key]
        if not self.freq_keys[freq] and self.min_freq == freq:
            # 如果当前频率的键没有，并且这个频率是最小频率，那么最小频率加 1
            self.min_freq += 1
        self.key_freq[key]             = freq + 1
        self.freq_keys[freq + 1][key]  = None

    def _evict(self):
        oldest_key, _ = self.freq_keys[self.min_freq].popitem(last=False)
        del self.key_val[oldest_key]
        del self.key_freq[oldest_key]
