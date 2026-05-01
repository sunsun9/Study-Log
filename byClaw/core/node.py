from __future__ import annotations
from typing import Any, Dict, Optional, Tuple, Iterable
import time
shared = {}

"""
实现一个轻量化的工作流引擎
Flow: 管理整条流水线
Node: 是流水线上的每个处理单元
结点之间通过action连接
"""

class Node:
    def __init__(self, max_retries: int = 1, wait: float = 0) -> Node:
        # 指明下一步可以走向哪个节点
        # 这里的"Node"表示的是Node类，之所以有""，是因为在这个时候其实还没有创建类，但是又要使用，因此需要带上""
        self.successors: Dict[str, "Node"] = {}
        self._action: str = "default"                   # 当前准备注册的跳转动作名
        self.max_retries, self.wait = max_retries, wait

    def exec(self, payload: Any) -> Tuple[str, Any]:
        """子类必须重写该方法
        返回值是一个元组["接下来该走哪条路(action)", "传递的数据"]
        """
        raise NotImplementedError
    
    def _exec(self, payload: Any) -> Tuple[str, Any]:
        """带重试的执行包装器,是 exec 的安全包装，用户只需关心 exec"""
        for cur_retry in range(self.max_retries):
            try:
                return self.exec(payload)
            except Exception as e:
                if cur_retry == self.max_retries - 1:
                    raise e             # 最后一次重试仍失败，抛出异常
                if self.wait > 0:       # 等待后再试
                    time.sleep(self.wait)
        raise RuntimeError("Unexpected error in Node._exec")
    
    def __rshift__(self, other: "Node") -> "Node":
        """用当前 _action 将 b 注册为 a 的后继"""
        self.successors[self._action] = other
        self._action = "default"
        return other
    
    def __sub__(self, action: str) -> "Node":
        """把 _action 设置为 "success" """
        if not isinstance(action, str):
            raise TypeError("Action must be a string")
        self._action = action or "default"
        return self
    
class Flow:
    def __init__(self, start: Optional[Node] = None) -> None:
        self.start = start
    
    def run(self, payload: Any = None) -> Tuple[Optional[str], Any]:
        curr, last_action = self.start, "default"
        while curr:
            last_action, payload = curr._exec(payload)
            curr = curr.successors.get(last_action)
        return last_action, payload
