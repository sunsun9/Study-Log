from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.llm import cal_llm
from core.node import Node, Flow
from tools import get_tools, ToolExecutor

SYSTEM_PROMPT = (
    "你是一个会调用工具的助手。"
    "当问题涉及最新信息、模型版本、产品发布时间或事实核验时，优先先调用 search 工具，再基于搜索结果回答。"
    "若问题时本地文件/代码相关，优先使用 read/grep/find/ls 等本地工具。"
)

class ChatNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        messages = shared["messages"]
        tools = shared["tools"]

        assistant_message = cal_llm(message=messages, tools=tools, system_prompt=SYSTEM_PROMPT)
        messages.append(assistant_message)

        if assistant_message.get("tool_calls"):
            return "tool_call", assistant_message

        return "output", assistant_message
    
class ToolCallNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        response = payload
        messages = shared["messages"]
        executor = shared["tool_executor"]

        tool_calls = executor.parse_tool_calls(response)
        results = executor.execute_all(tool_calls)

        for tc, result in zip(tool_calls, results):
            print(f" [Tool] 执行：{tc.name}({tc.arguments})")
            print(f" [Tool] 结果：{result.content[:100]}...")
            messages.append(result.to_message())

        return "chat", None
    
class OutputNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        response = payload
        content = response.get("content", "")
        print(f"\n🤖 Assistant: {content}\n")
        return "default", None


def run_chat() -> None:
    print("=" * 60)
    print("🤖 Chatbot with Tools")
    print("=" * 60)
    print("可用工具: read, write, edit, bash, grep, find, ls, search")
    print("输入 'quit' 或 'exit' 退出\n")

    share.clear()
    shared["messages"] = []
    shared["tools"] = [t.to_llm_format() for t in get_tools()]
    shared["tool_executor"] = ToolExecutor()

    chat = ChatNode()
    tool_call = ToolCallNode()
    output = OutputNode()

    chat - "tool_call" >> tool_call
    tool_call - " chat" >> chat
    chat - "output" >> output

    while True:
        user_input = input("👤 You: ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            print("\n再见！")
            break

        if not user_input:
            continue

        shared["messages"].append({"role": "user", "content": user_input})
        flow = Flow(chat)
        flow.run()

def main() -> None:
    if not os.environ.get("OPENAI_API_KEY") or not os.environ.get("OPENAI_BASE_URL"):
        print("⚠️  提示：请先设置环境变量 OPENAI_API_KEY 和 OPENAI_BASE_URL")
        return

    run_chat()

if __name__ == "__main__":
    main()