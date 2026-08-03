import json
import os

class ConversationMemory:
    def __init__(self, max_history: int = 20):
        """
        Manages Husk's short-term conversation context and history persistence.
        :param max_history: Maximum number of recent messages to hold in active context window.
        """
        self.max_history = max_history
        self.history = []

    def add_message(self, role: str, content: str):
        """
        Appends a new message (user or assistant) to memory.
        """
        self.history.append({"role": role, "content": content})
        self._trim_history()

    def get_messages(self) -> list:
        """
        Returns active context window messages.
        """
        return self.history

    def _trim_history(self):
        """
        Keeps the history within max_history bounds to save tokens.
        """
        if len(self.history) > self.max_history:
            # Retain the most recent max_history messages
            self.history = self.history[-self.max_history:]

    def clear(self):
        """
        Clears current session memory.
        """
        self.history = []

    def save_to_file(self, filepath: str = "storage/history.json"):
        """
        Saves chat history to a JSON file in storage folder.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4)

    def load_from_file(self, filepath: str = "storage/history.json"):
        """
        Loads chat history from a JSON file if it exists.
        """
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                self.history = json.load(f)