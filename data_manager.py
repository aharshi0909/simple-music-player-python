import os
import json
from datetime import datetime
from typing import List, Dict

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.history_file = os.path.join(self.data_dir, "history.json")
        os.makedirs(self.data_dir, exist_ok=True)
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w") as f:
                json.dump({}, f)

    def _load(self, path: str) -> dict:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save(self, path: str, data: dict):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_to_listening_history(self, user_id: str, track: Dict):
        history = self._load(self.history_file)
        if user_id not in history:
            history[user_id] = []
        track = track.copy()
        track["played_at"] = datetime.now().isoformat()
        history[user_id].insert(0, track)
        history[user_id] = history[user_id][:100]
        self._save(self.history_file, history)

    def get_user_listening_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        history = self._load(self.history_file)
        return history.get(user_id, [])[:limit]
