# 单调栈 —— 下一个更大元素 ⭐⭐⭐
def next_greater(nums):
    n = len(nums)
    res = [-1] * n
    stack = []                          # 存下标，维护单调递减
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            res[stack.pop()] = nums[i]  # 找到了更大元素
        stack.append(i)
    return res

def nextGreaterElements(nums):
    # 环形数组的单调栈解法：遍历两轮，第一轮正常压栈，第二轮只找答案，不压栈
    n = len(nums)
    res = [-1] * n
    stack = []  # 存下标

    for i in range(2 * n):
        num = nums[i % n]
        while stack and nums[stack[-1]] < num:
            idx = stack.pop()
            res[idx] = num
        # 第二圈不用再压栈了，只需要帮第一圈的元素找答案
        if i < n:
            stack.append(i)

    return res


class MyQueue:
    """用两个栈实现一个队列。队列的声明如下，请实现它的两个函数 appendTail 和 deleteHead ，
    分别完成在队列尾部插入整数和在队列头部删除整数的功能。(若队列中没有元素，deleteHead 操作返回 -1 )
    关键思想：只有当 out_st 为空时，才把 in_st 全部倒进去
    """
    def __init__(self):
        self.in_st, self.out_st = [], []

    def push(self, x):
        self.in_st.append(x)

    def pop(self):
        if not self.out_st:             # out_st 空时才倒
            while self.in_st:
                self.out_st.append(self.in_st.pop())
        return self.out_st.pop()

    def peek(self):
        """查看队头"""
        val = self.pop(); self.out_st.append(val); return val
    

def is_valid(s):
    stack = []
    mp = {')':'(', ']':'[', '}':'{'}

    for c in s:
        if c in mp:
            # 判断当前字符是不是右括号
            if not stack or stack[-1] != mp[c]:
                return False
            stack.pop()
        else:
            # 当前字符是左括号，入栈
            stack.append(c)

    return not stack


def largestRectangleArea(heights):
    # 单调栈解法：维护一个单调递增的栈，遇到更小的高度时，弹出栈顶元素，计算以该元素为高的矩形面积
    stack = []
    heights = [0] + heights + [0]
    res = 0

    for i in range(len(heights)):
        while stack and heights[stack[-1]] > heights[i]:
            # stack[-1] 是当前矩形的左边界，i 是右边界，h 是高度，w 是宽度
            # 循环条件是找右边界，循环是找左边界
            h = heights[stack.pop()]
            w = i - stack[-1] - 1
            res = max(res, h * w)
        stack.append(i)

    return res


class MinStack:
    """设计一个支持 push、pop、top 操作，并能在常数时间内检索到最小元素的栈。"""
    def __init__(self):
        self.st = []
        self.min_st = []

    def push(self, x):
        self.st.append(x)
        if not self.min_st or x <= self.min_st[-1]:
            self.min_st.append(x)

    def pop(self):
        if self.st.pop() == self.min_st[-1]:
            self.min_st.pop()

    def getMin(self):
        return self.min_st[-1]
    

def calculate(s):
    """实现一个基本的计算器来计算一个简单的字符串表达式 s 的值。
    表达式字符串 s 可能包含空格 ' '，数字 0-9，和算符 +、-、*、/ 。整数除法仅保留整数部分。"""
    stack = []
    num = 0
    sign = '+'

    for c in s + '+':
        if c.isdigit():
            num = num * 10 + int(c)
        elif c in '+-*/':
            if sign == '+': stack.append(num)
            if sign == '-': stack.append(-num)
            if sign == '*': stack.append(stack.pop() * num)
            if sign == '/': stack.append(int(stack.pop() / num))
            num = 0
            sign = c

    return sum(stack)

def removeDuplicateLetters(s):
    """给你一个字符串 s ，请你去除字符串中重复的字母，
    使得每个字母只出现一次。需保证返回结果的字典序最小（要求不能打乱其他字符的相对位置）。"""
    stack = []
    seen = set()
    last = {c:i for i,c in enumerate(s)}

    for i, c in enumerate(s):
        if c in seen:
            continue

        while stack and c < stack[-1] and last[stack[-1]] > i:
            seen.remove(stack.pop())

        stack.append(c)
        seen.add(c)

    return ''.join(stack)