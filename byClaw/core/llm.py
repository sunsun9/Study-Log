from __future__ import annotations

import os
from typing import Any
from openai import OpenAI
from dotenv import load_dotenv 

def call_llm_simple(prompt: str) -> str :
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE_URL")
    )
    response = client.chat.completions.create(
        model='qwen3.6-plus',
        messages=[{"role": "user", "content": prompt}]
    )
    message = response.choices[0].message
    return message.content or ""

def cal_llm(
        message: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        system_prompt: str | None = None,
) -> dict[str, Any]:
    msgs = list(message)

    if system_prompt:
        "如果有系统提示的话，放在消息列表的最前面，作为系统消息"
        msgs = [{"role": "system", "content": system_prompt}, *msgs]

    kwargs: dict[str, Any] = {
        "model": "qwen3.6-plus",
        "messages": msgs,
    }

    if tools:
        # 或者是skills，或者是工具，反正就是一些可以调用的能力，模型可以根据需要选择调用哪些工具来完成任务
        kwargs["tools"] = tools
        # 关于工具的选择，也可以设置从消息中指定，看到一个视频说的是工具指定的越准确，完成的效果也会越好
        kwargs["tool_choice"] = "auto"

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE_URL")
    )
    response = client.chat.completions.create(**kwargs)
    message = response.choices[0].message

    result: dict[str, Any] = {
        "role": message.role,
        "content": message.content or "",
    }

    reasoning_content = getattr(message, "reasoning_content", None)
    if reasoning_content:
        result["reason_content"] = reasoning_content

    if message.tool_calls:
        result["tool_calls"] = [tool_call.model_dump() for tool_call in message.tool_calls]

    return result

if __name__ == "__main__":
    load_dotenv()
    print("Basic:", call_llm_simple("用一句话解释什么是Agent。"))