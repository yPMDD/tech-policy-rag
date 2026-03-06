"""
rag/generator.py - Bridges to the local Ollama LLM.
"""

import ollama
from typing import Optional, Dict, Any

class Generator:
    """
    Handles communication with local Ollama instance.
    """
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        # Ensure model is pulled (this might take time on first run)
        # We don't pull automatically here to avoid stalling, 
        # but we check connection.
        pass

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends query to Ollama and returns the response.
        """
        try:
            response = ollama.generate(
                model=self.model_name,
                system=system_prompt,
                prompt=user_prompt,
                stream=False
            )
            return response['response']
        except Exception as e:
            return f"Error connecting to Ollama: {e}. Make sure Ollama is running and '{self.model_name}' is pulled."

if __name__ == "__main__":
    # Test with a simple prompt
    gen = Generator()
    res = gen.generate("You are a helpful assistant.", "how can i learn spanish in 3 days")
    print(res)
