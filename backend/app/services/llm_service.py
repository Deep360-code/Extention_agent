from groq import AsyncGroq
from app.config import settings

groq_client = AsyncGroq(
    api_key=settings.GROQ_API_KEY,
)

SUPPORTED_MODELS = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"] # Valid Groq models

async def get_groq_response(prompt: str, model: str = "llama3-70b-8192") -> dict:
    """
    Calls the Groq API and returns the generated content and token usage.
    """
    # Ensure model is valid
    if model not in SUPPORTED_MODELS:
        model = "llama-3.1-8b-instant"

    chat_completion = await groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        temperature=0.7,
        max_tokens=2048,
    )

    content = chat_completion.choices[0].message.content
    tokens_used = chat_completion.usage.total_tokens if chat_completion.usage else 0

    return {
        "content": content,
        "tokens_used": tokens_used
    }
