# 1️⃣求一个数组中，两数之和等于目标值的元素

# 有序版
def two_sum(nums, target):
    lo, hi = 0, len(nums) - 1   # lo 指向最左（最小），hi 指向最右（最大）
    
    while lo < hi:               # 两指针还没相遇就继续
        s = nums[lo] + nums[hi]  # 算出当前两数之和
        if s == target:          # 刚好等于目标，找到了！
            return [lo, hi]
        elif s < target:         # 和太小了，需要更大的数 → 左指针右移
            lo += 1
        else:                    # 和太大了，需要更小的数 → 右指针左移
            hi -= 1
    return []  # 没找到

# 无序版
def two_sum2(nums, target):
    seen = {}                        # 存 {值: 下标}，注意值是key，下标是value
    for i, x in enumerate(nums):
        complement = target - x      # 需要找的另一个数
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []


# ② 前缀和 —— O(1) 数组区间求和
# 是很多算法题的底层工具
def build_prefix(nums):
    n = len(nums)
    pre = [0] * (n + 1)          # pre[i] = nums[0..i-1] 之和
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]
    return pre
# 区间 [l, r] 之和 = pre[r+1] - pre[l]


# ③ 差分数组 —— O(1) 区间加法，O(n) 还原
# nums = [2, 3, 5, 5, 8]
# diff = [2, 1, 2, 0, 3] 这就是差分数组
# 前缀和是"快速查询"，差分数组是**"快速修改"** —— 对某个区间整体加一个值，O(1) 完成，最后再 O(n) 一次性还原。
# 两者是互逆操作，经常配套出现。
def range_add(diff, l, r, val):
    # 这个是对查分数组直接+val，所以这个的效果就是将[l, r]中的每一个元素都+val
    diff[l]     += val  # 因为前一个元素没有+
    diff[r + 1] -= val           # 因为r后面的一个元素没有+，超界时需 r+1 < len(diff)
    # 而中间的每一个元素都增大了相同的大小，所以中间的差分没有变

def restore(diff):
    # 从查分数组还原到原来的数组
    res = diff[:]   # 复制差分数组
    for i in range(1, len(res)):
        res[i] += res[i - 1]
    return res

