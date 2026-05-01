from __future__ import annotations

import os
import sys
from pathlib import Path
from types import Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.llm import call_llm_simple
from core.node import Node, Flow
from tools.builtins.search import search as search_ddgs

class QueryNode(Node):
    """获取查询-查询节点"""
    def exec(self, payload: Any) -> Tuple[str, Any]:
        return "search", str(payload)
    
class SearchNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        results = search_ddgs(str(payload), max_results=3)
        titles = [r.get("title") or r.get("body") or "" for r in results]
        summary_input = " | ".join([t for t in titles if t])
        return "summarize", summary_input
    
class SummarizeNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        prompt = f"基于一下要点写一句话摘要：{payload}"
        text = call_llm_simple(prompt)
        return "default", text
    
def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        print("提示： 请先设置环境变量 OPENAI_API_KEY")
        return
    
    query = QueryNode()
    search = SearchNode()
    summarize = SummarizeNode()

    query - "search" >> search
    search - "summarize" >> summarize

    flow = Flow(query)
    _, result = flow.run("asyncio python best practices")
    print("Workflow 流出：", result)

if __name__ == "__main__":
    main()