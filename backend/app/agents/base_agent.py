"""
AI Mentor - Base Agent with HuggingFace + DeepSeek + Groq + Gemini Support.

Uses FREE models: Qwen2.5-72B, DeepSeek-V3, Llama-3.3-70B via HuggingFace Inference API.
Also supports Google Gemini via GEMINI_API_KEY environment variable.
"""

import json
import re
import os
import httpx
from typing import Optional, Dict, Any
from loguru import logger
from ..core.config import get_settings

# Free HuggingFace models ranked by capability
HF_MODELS = {
    "qwen2.5-72b": "Qwen/Qwen2.5-72B-Instruct",
    "qwen2.5-coder-32b": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "llama-3.3-70b": "meta-llama/Llama-3.3-70B-Instruct",
    "deepseek-r1-32b": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "mistral-small": "mistralai/Mistral-Small-24B-Instruct-2501",
    "phi-4": "microsoft/phi-4",
}

# Default model - Qwen2.5-72B is the best free Chinese model (rivals GPT-4o)
DEFAULT_HF_MODEL = "Qwen/Qwen2.5-72B-Instruct"


def get_llm_config():
    """Get LLM configuration from settings."""
    settings = get_settings()
    return {
        "provider": settings.llm_provider,
        "hf_token": os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_API_KEY") or settings.groq_api_key,
        "deepseek_key": os.getenv("DEEPSEEK_API_KEY"),
        "gemini_key": settings.gemini_api_key or os.getenv("GEMINI_API_KEY"),
        "groq_key": settings.groq_api_key,
        "model": settings.llm_model,
        "temperature": settings.llm_temperature,
        "max_tokens": settings.llm_max_tokens,
    }


async def call_huggingface(messages: list, model: str = None, max_tokens: int = 4096) -> str:
    """
    Call HuggingFace Inference API (FREE).
    Uses OpenAI-compatible chat completions endpoint.
    """
    config = get_llm_config()
    token = config["hf_token"]
    model = model or DEFAULT_HF_MODEL

    url = f"https://api-inference.huggingface.co/models/{model}/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": min(max_tokens, 4096),
        "temperature": config.get("temperature", 0.7),
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            logger.error(f"HuggingFace API error {response.status_code}: {response.text[:500]}")
            # Try fallback model
            if model != "mistralai/Mistral-Small-24B-Instruct-2501":
                logger.info("Trying fallback model...")
                return await call_huggingface(
                    messages, "mistralai/Mistral-Small-24B-Instruct-2501", max_tokens
                )
            raise Exception(f"HuggingFace API error: {response.status_code}")


async def call_deepseek(messages: list, max_tokens: int = 4096) -> str:
    """
    Call DeepSeek API (FREE credits on signup).
    DeepSeek-V3 rivals GPT-4o in accuracy.
    """
    config = get_llm_config()
    key = config.get("deepseek_key") or config.get("hf_token")

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": config.get("temperature", 0.7),
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            logger.error(f"DeepSeek API error: {response.status_code}")
            raise Exception(f"DeepSeek API error: {response.status_code}")


async def call_gemini(messages: list, max_tokens: int = 4096) -> str:
    """
    Call Google Gemini API.
    Set GEMINI_API_KEY in your .env file.
    Get a free key at: https://aistudio.google.com/app/apikey
    """
    config = get_llm_config()
    key = config.get("gemini_key")
    if not key:
        raise Exception("GEMINI_API_KEY not set. Add it to your .env file.")

    model = "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

    # Convert messages to Gemini format
    system_text = ""
    user_text = ""
    for m in messages:
        if m["role"] == "system":
            system_text = m["content"]
        elif m["role"] == "user":
            user_text = m["content"]

    payload = {
        "systemInstruction": {"parts": [{"text": system_text}]},
        "contents": [{"parts": [{"text": user_text}]}],
        "generationConfig": {
            "temperature": config.get("temperature", 0.7),
            "maxOutputTokens": min(max_tokens, 8192),
        }
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, json=payload,
                                     headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            logger.error(f"Gemini API error {response.status_code}: {response.text[:500]}")
            raise Exception(f"Gemini API error: {response.status_code}")



def get_llm():
    """
    Get LangChain LLM for providers that support it.
    Falls back to HuggingFace for free usage.
    """
    settings = get_settings()
    provider = settings.llm_provider.lower()

    if provider == "groq" and settings.groq_api_key and settings.groq_api_key != "your_groq_api_key_here":
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )
    elif provider == "openai" and settings.openai_api_key:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )
    return None  # Will use direct HTTP calls instead


def parse_json_response(response_text: str) -> Dict[str, Any]:
    """Parse JSON from LLM response, handling markdown code blocks."""
    # Try direct parse
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Extract from markdown code blocks
    json_match = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', response_text)
    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Find JSON object or array
    for pattern in [r'(\{[\s\S]*\})', r'(\[[\s\S]*\])']:
        match = re.search(pattern, response_text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

    logger.error(f"Failed to parse JSON: {response_text[:200]}...")
    return {"error": "Failed to parse response", "raw": response_text[:500]}


async def invoke_agent(system_prompt: str, user_message: str, parse_json: bool = True) -> Any:
    """
    Invoke an AI agent. Tries HuggingFace (free) first, then falls back.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    try:
        # Try LangChain LLM first (Groq/OpenAI if configured)
        llm = get_llm()
        if llm:
            from langchain_core.messages import SystemMessage, HumanMessage
            lc_messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_message)]
            response = llm.invoke(lc_messages)
            response_text = response.content
        else:
            # Use FREE HuggingFace API
            config = get_llm_config()
            provider = config["provider"].lower()

            if provider == "gemini" and config.get("gemini_key"):
                response_text = await call_gemini(messages)
            elif provider == "deepseek" and config.get("deepseek_key"):
                response_text = await call_deepseek(messages)
            elif config.get("gemini_key"):  # Auto-use Gemini if key is set
                response_text = await call_gemini(messages)
            else:
                # Default: HuggingFace (FREE)
                response_text = await call_huggingface(messages)

        if parse_json:
            return parse_json_response(response_text)
        return response_text

    except Exception as e:
        logger.error(f"Agent invocation error: {e}")
        if parse_json:
            return {"error": str(e)}
        return f"Error: {str(e)}"
