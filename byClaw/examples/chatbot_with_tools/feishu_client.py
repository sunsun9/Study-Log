"""
飞书 API 客户端 - 负责获取 token 和发送消息
放在 examples/chatbot_with_tools/feishu_client.py
"""

from __future__ import annotations

import json
import os
import time

import requests

# token 缓存，避免每次都重新请求（有效期 2 小时）
_token_cache: dict = {"token": "", "expires_at": 0}


def get_tenant_token() -> str:
    """获取飞书 tenant_access_token，自动缓存"""
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires_at"]:
        return _token_cache["token"]

    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={
            "app_id": os.environ["FEISHU_APP_ID"],
            "app_secret": os.environ["FEISHU_APP_SECRET"],
        },
        timeout=10,
    )
    data = resp.json()
    token = data.get("tenant_access_token", "")
    expire = data.get("expire", 7200)

    _token_cache["token"] = token
    _token_cache["expires_at"] = now + expire - 60  # 提前 60 秒刷新

    return token


def send_message(chat_id: str, text: str) -> None:
    """向指定 chat_id 发送文本消息"""
    token = get_tenant_token()

    # 飞书单条消息最长 4000 字，超出截断
    if len(text) > 4000:
        text = text[:3997] + "..."

    resp = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/messages",
        params={"receive_id_type": "chat_id"},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": text}),
        },
        timeout=10,
    )

    if resp.status_code != 200 or resp.json().get("code") != 0:
        print(f"[飞书] 发送失败: {resp.text}")
