import json
import os
from datetime import datetime
from typing import Literal, Optional

LOG_FILE = ".gemini_logs/history.json"


class GeminiLogger:
    def __init__(self):
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not os.path.exists(".gemini_logs"):
            os.makedirs(".gemini_logs")
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)

    def log(
        self,
        role: Literal["user", "assistant", "system"],
        content: str,
        context_source: Optional[str] = None,
        metadata: Optional[dict] = None,
    ):

        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "context_source": context_source,  # e.g., "GEMINI_MEMORY.md", "GLOBAL_MEMORY_GUIDE.md"
            "metadata": metadata or {},
        }

        try:
            with open(LOG_FILE, "r+", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.truncate()
        except Exception as e:
            print(f"Failed to log to JSON: {e}")

    def log_code_change(self, file_path: str, description: str, diff: str = ""):
        self.log(
            role="assistant",
            content=f"Code Change: {description}",
            metadata={"type": "code_change", "file": file_path, "diff": diff},
        )


# Singleton instance
logger = GeminiLogger()

if __name__ == "__main__":
    # Test
    logger.log("user", "Test message", "manual_test")
    logger.log_code_change(
        "backend/main.py", "Added endpoint", "+ def get_items(): pass"
    )
    print(f"Logged to {LOG_FILE}")
