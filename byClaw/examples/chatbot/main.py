from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Tuple

# 添加工作路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.node import Node, Flow, shared
from core.llm import cal_llm

SYSTEM_PROMPT = "你是一个友好的对话助手，请回答用户的问题。"

class ChatNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        messages = shared["messages"]
        assistant_message = cal_llm(message=messages, system_prompt=SYSTEM_PROMPT)
        messages.append(assistant_message)
        return "output", assistant_message

class OutputNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        response = payload
        content = response.get("content", "")
        print(f"\n🤖 Assistant: {content}\n")
        return "default", None
    
def run_chat() -> None:
    print("=" * 60)
    print("🤖 Simple Chatbot")
    print("=" * 60)
    print("请输入 'quit' 或 'exit' 退出\n")

    shared.clear()
    shared["messages"] = []

    chat = ChatNode()
    output = OutputNode()

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
        flow.run(None)


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY") or not os.environ.get("OPENAI_BASE_URL"):
        print("⚠️  提示：请先设置环境变量 OPENAI_API_KEY 和 OPENAI_BASE_URL")
        return

    run_chat()

if __name__ == "__main__":
    main()