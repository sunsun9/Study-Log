from __future__ import annotations

import os
import sys
import threading

from pathlib import Path
from typing import Any, Tuple
from dotenv import load_dotenv 

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from flask import Flask, request, jsonify

from core.llm import call_llm
from core.node import Node, Flow
from tools import get_tools, ToolExecutor
from feishu_client import send_message

app = Flask(__name__)

SYSTEM_PROMPT = (
    "你是一个会调用工具的助手。"
    "当问题涉及最新消息、模型版本、产品发布时间或事实核验时，优先调用 search 工具，再基于搜索结果回答。"
    "若问题是本地文件/代码相关，优先使用 read/grep/find/ls 等本地工具"
)

sessions: dict[str, list] = {}

processed_event_ids: set[str] = set()

class ChatNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        state = payload
        assistant_message = call_llm(
            messages=state["messages"],
            tools=state["tools"],
            system_prompt=SYSTEM_PROMPT,
        )
        state["messages"].append(assistant_message)

        if assistant_message.get("tool_calls"):
            return "tool_call", state
        return "output", state
    

class ToolCallNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        state = payload
        last_msg = state["messages"][-1]
        tool_calls = state["executor"].parse_tool_calls(last_msg)
        results = state["executor"].execute_all(tool_calls)

        for tc, result in zip(tool_calls, results):
            print(f" [Tool] {tc.name}({tc.arguments})")
            state["messages"].append(result.to_message())
        return "chat", state
    
class OutputNode(Node):
    def exec(self, payload: Any) -> Tuple[str, Any]:
        state = payload
        content = state["messages"][-1].get("content", "")
        state["final_reply"] = content
        return "default", state

def run_agent(chat_id: str, user_text: str) -> str:
    if chat_id not in sessions:
        sessions[chat_id] = []

    messages = sessions[chat_id]
    messages.append({"role": "user", "content": user_text})

    state = {
        "messages": messages,
        "tools": [t.to_llm_format() for t in get_tools()],
        "executor": ToolExecutor(),
        "final_reply": "",
    }

    chat = ChatNode()
    tool_call = ToolCallNode()
    output = OutputNode()

    chat - "tool_call" >> tool_call
    tool_call - "chat" >> chat
    chat - "output" >> output

    _, final_state = Flow(chat).run(state)
    reply = final_state["final_reply"]
    return reply

@app.route("/feishu/webhook", methods=["POST"])
def feishu_webhook():
    body = request.json or {}

    # 1. 飞书首次配置时的 URL 验证
    if body.get("type") == "url_verification":
        return jsonify({"challenge": body.get("challenge")})

    # 2. 获取事件信息
    header = body.get("header", {})
    event_id = header.get("event_id", "")
    event_type = header.get("event_type", "")

    # 防重放：同一 event_id 只处理一次
    if event_id in processed_event_ids:
        return jsonify({"code": 0})
    processed_event_ids.add(event_id)

    # 3. 只处理收到消息的事件
    if event_type != "im.message.receive_v1":
        return jsonify({"code": 0})

    event = body.get("event", {})
    message = event.get("message", {})
    msg_type = message.get("message_type", "")
    chat_id = message.get("chat_id", "")

    # 只处理文本消息
    if msg_type != "text" or not chat_id:
        return jsonify({"code": 0})

    import json
    content = json.loads(message.get("content", "{}"))
    user_text = content.get("text", "").strip()

    if not user_text:
        return jsonify({"code": 0})

    print(f"[飞书] 收到消息 chat_id={chat_id}: {user_text}")

    # 4. 先立刻返回 200，再异步处理（飞书要求 3 秒内响应）
    def handle():
        try:
            reply = run_agent(chat_id, user_text)
            send_message(chat_id, reply)
            print(f"[飞书] 已回复: {reply[:80]}...")
        except Exception as e:
            send_message(chat_id, f"出错了：{e}")
            print(f"[Error] {e}")

    threading.Thread(target=handle, daemon=True).start()
    return jsonify({"code": 0})

if __name__ == "__main__":
    load_dotenv()
    required = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "FEISHU_APP_ID", "FEISHU_APP_SECRET"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"⚠️  缺少环境变量: {', '.join(missing)}")
        sys.exit(1)

    print("🤖 飞书 Bot 启动，监听 http://0.0.0.0:3000/feishu/webhook")
    app.run(host="0.0.0.0", port=3000, debug=False)
