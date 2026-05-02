from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.llm import cal_llm
from core.node import Node, Flow
from tools import get_tools, ToolExecutor