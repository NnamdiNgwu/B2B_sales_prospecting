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
from src.llm.llm_manager import LLMManager

class LLMService:
    def __init__(self) -> None:
        self._mgr = LLMManager()

    def generate(self, prompt: str, **params: Dict[str, Any]) -> str:
        """
        Generic text generation. Do not inject a default system prompt here.
        Let llm_manager/B2BMessagePersonalizer own personalization instructions.
        """
        try:
            # Primary: use manager’s own generate (single source of truth)
            try:
                text = self._mgr.generate(prompt=prompt, **params)  # type: ignore[attr-defined]
                return self._postprocess(text, params)
            except AttributeError:
                # Fallback: call LLM as chat; include system only if provided
                try:
                    from langchain_core.messages import HumanMessage, SystemMessage
                except Exception:
                    from langchain.schema import HumanMessage, SystemMessage  # type: ignore
                messages = []
                if isinstance(params.get("system"), str) and params["system"].strip():
                    messages.append(SystemMessage(content=params["system"]))
                messages.append(HumanMessage(content=prompt))
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
        max_chars = params.get("max_chars")
        if isinstance(max_chars, int) and max_chars > 0 and len(text) > max_chars:
            return text[:max_chars].rstrip()
        return text

def get_llm_service() -> LLMService:
    return LLMService()