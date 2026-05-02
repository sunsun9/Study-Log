from __future__ import annotations

from pathlib import Path

"""
一个安全的文件局部替换器：
通过"精确匹配 + 唯一性校验"避免误改，
替换后返回变更行号，
适合在代码生成、Agent 自动修改文件等场景中使用。
"""

def edit_file(path: str, old_text: str, new_text: str, cwd: str | None = None) -> dict:
    if cwd:
        file_path = Path(cwd) / path
    else:
        file_path = Path(path)

    # 获取文件路径
    file_path = file_path.resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    # 读取文件内容
    content = file_path.read_text(encoding="utf-8")
    if old_text not in content:
        raise ValueError(f"Could not find the exact text in {path}. The old text must match exactly.")
    
    # 找到要替换的旧内容数量，防止误改多处
    occurrences = content.count(old_text)
    if occurrences > 1:
        raise ValueError(f"Found {occurrences} occurrences of the text in {path}. The text must be unique.")
    
    # 替换旧内容，仅替换一次
    new_content = content.replace(old_text, new_text, 1)

    if content == new_content:
        raise ValueError(f"No changes made to {path}")
    
    file_path.write_text(new_content, encoding="utf-8")

    old_lines = content.split("\n")
    new_lines = new_content.split("\n")

    first_change_line = None
    for i, (old, new) in enumerate(zip(old_lines, new_lines)):
        if old != new:
            first_change_line = i + 1
            break

    return {
        "message": f"Successfully replaced text in {path}",
        "first_change_line": first_change_line,
    }

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        try:
            result = edit_file(sys.argv[1], sys.argv[2], sys.argv[3])
            print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        print("Usage: python edit.py <file_path> <old_text> <new_text>", file=sys.stderr)