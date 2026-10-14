import os
from typing import Optional, Dict, Any

class LLMBridge:
    """
    Seamless interface for Gemini LLM generation with deterministic
    offline fallback when no API key is provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None

    def synthesize_narrative(self, prompt: str, fallback_text: str) -> str:
        """
        Attempts LLM completion if client is active, else returns fallback text.
        """
        if not self.client:
            return fallback_text
            
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            if response and response.text:
                return response.text.strip()
        except Exception:
            pass
            
        return fallback_text
