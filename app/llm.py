from openai import OpenAI

from .config import settings


def get_llm_client() -> OpenAI:
    return OpenAI(
        api_key=settings.openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            **({"HTTP-Referer": settings.openrouter_site_url} if settings.openrouter_site_url else {}),
            **({"X-Title": settings.openrouter_app_name} if settings.openrouter_app_name else {}),
        },
    )
