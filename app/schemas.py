from pydantic import BaseModel, Field, model_validator


class ChatRequest(BaseModel):
    question: str | None = Field(default=None, min_length=1)
    message: str | None = Field(default=None, min_length=1)
    prompt: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def _ensure_one_field(self):
        if not (self.question or self.message or self.prompt):
            raise ValueError("One of 'question', 'message', or 'prompt' is required")
        return self

    def text(self) -> str:
        return (self.question or self.message or self.prompt or "").strip()


class Source(BaseModel):
    id: str
    score: float | None = None
    text: str
    source: str | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
