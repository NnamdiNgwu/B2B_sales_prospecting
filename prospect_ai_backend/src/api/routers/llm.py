from fastapi import APIRouter, Depends
from ..schemas.llm import GenerateIn, GenerateOut
from ..services.llm_service import LLMService, get_llm_service

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/generate", response_model=GenerateOut)
def generate(body: GenerateIn, svc: LLMService = Depends(get_llm_service)):
    text = svc.generate(body.prompt, **(body.params or {}))
    return GenerateOut(output=text)