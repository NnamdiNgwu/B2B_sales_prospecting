# from loguru import logger
# from src.llm.llm_manager import LLMManager

# class LLMService:
#     def __init__(self) -> None:
#         self._mgr = LLMManager()

#     def generate(self, prompt: str, **kwargs) -> str:
#         try:
#             # Prefer a direct method if present
#             if hasattr(self._mgr, "generate") and callable(getattr(self._mgr, "generate")):
#                 return self._mgr.generate(prompt=prompt, **kwargs)  # type: ignore

#             # Fallback: call the manager like a chat model with a single HumanMessage
#             try:
#                 from langchain_core.messages import HumanMessage
#             except Exception:
#                 from langchain.schema import HumanMessage  # type: ignore

#             res = self._mgr([HumanMessage(content=prompt)])  # __call__ path
#             if isinstance(res, dict) and "content" in res:
#                 return str(res.get("content", ""))
#             if hasattr(res, "content"):
#                 return str(getattr(res, "content"))
#             return str(res)
#         except Exception as e:
#             logger.error(f"LLMService.generate failed: {e}")
#             return ""

# def get_llm_service() -> LLMService:
#     return LLMService()


from typing import Any, Dict
from loguru import logger

# Prefer absolute import (src layout)
from src.llm.llm_manager import LLMManager

class LLMService:
    def __init__(self) -> None:
        # LLMManager loads provider/model from env/.env
        self._mgr = LLMManager()

    def generate(self, prompt: str, **params: Dict[str, Any]) -> str:
        """
        Generate text using the configured LLM.

        Params supported (best-effort; some providers may ignore):
          - system: str (system prompt)
          - temperature: float
          - max_tokens: int (hinted via system prompt to keep replies short)
        """
        try:
            system_msg = params.get(
                "system",
                "You are a concise assistant. Respond in one short sentence unless otherwise requested.",
            )

            # Try to use a direct generate() if the manager exposes it.
            if hasattr(self._mgr, "generate") and callable(getattr(self._mgr, "generate")):
                text = self._mgr.generate(prompt=prompt, **params)  # type: ignore[attr-defined]
                return self._postprocess(text, params)

            # Fallback: call the manager like a chat model with messages
            try:
                from langchain_core.messages import HumanMessage, SystemMessage
            except Exception:
                # Older langchain
                from langchain.schema import HumanMessage, SystemMessage  # type: ignore

            messages = [SystemMessage(content=system_msg), HumanMessage(content=prompt)]

            # LLMManager.__call__(messages) returns either a dict-like or object with .content
            res = self._mgr(messages)  # type: ignore[call-arg]
            if isinstance(res, dict) and "content" in res:
                text = str(res.get("content", ""))
            elif hasattr(res, "content"):
                text = str(getattr(res, "content"))
            else:
                text = str(res)

            return self._postprocess(text, params)
        except Exception as e:
            logger.error(f"LLMService.generate failed: {e}")
            return ""

    def _postprocess(self, text: str, params: Dict[str, Any]) -> str:
        # Soft cap length if caller asked for terseness
        max_chars = params.get("max_chars")
        if isinstance(max_chars, int) and max_chars > 0 and len(text) > max_chars:
            return text[:max_chars].rstrip()
        return text

def get_llm_service() -> LLMService:
    return LLMService()