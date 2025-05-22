from enum import Enum


AI_ROLE_OPTIONS_EN: list[str] = [
    "",
    "helpful assistant",
    "code assistant",
    "code reviewer",
    "text improver",
    "cinema expert",
    "sport expert",
    "online games expert",
    "food recipes expert",
    "English grammar expert",
    "friendly and helpful teaching assistant",
    "laconic assistant",
    "helpful, pattern-following assistant",
    "translate corporate jargon into plain English",
]

AI_ROLE_OPTIONS_RU: list[str] = [
    "",
    "ассистент, который готов помочь",
    "ассистент программиста",
    "рецензент кода программиста",
    "эксперт по улучшению текста",
    "эксперт по кинематографу",
    "эксперт в области спорта",
    "эксперт в онлайн-играх",
    "эксперт по рецептам блюд",
    "эксперт по английской грамматике",
    "эксперт по русской грамматике",
    "дружелюбный и полезный помощник преподавателя",
    "лаконичный помощник",
    "полезный помощник, следующий шаблонам",
    "переводчик корпоративного жаргона на простой русский",
]

REPO_URL: str = "https://github.com/dKosarevsky/AI-Talks"
README_URL: str = f"{REPO_URL}#readme"
AI_TALKS_URL: str = "https://ai-talks.streamlit.app/"
HEADERS: dict = {"Content-Type": "application/json; charset=utf-8"}
ADMIN_TG: str = "https://t.me/wd4000"

TEMP_KEY: str = "Temperature"
USER_TXT_KEY: str = "user_text"


class AIModels(Enum):
    # https://platform.openai.com/docs/models

    # Reasoning models
    o3_mini = "o3-mini"
    o4_mini = "o4-mini"
    o1 = "o1"
    o3 = "o3"
    o1_pro = "o1-pro"

    # Flagship chat models
    gpt4o = "gpt-4o"
    gpt4_1 = "gpt-4.1"
    chatgpt_4o = "chatgpt-4o-latest"

    # Cost-optimized models
    gpt_4_1_mini = "gpt-4.1-mini"
    gpt_4_1_nano = "gpt-4.1-nano"
    gpt_4o_mini = "gpt-4o-mini"

    # Image generation models
    dalle_3 = "dall-e-3"

    # anthropic models
    opus_4 = "claude-opus-4-0"
    opus_3 = "claude-3-opus-latest"
    sonnet_4 = "claude-sonnet-4-0"
    sonnet_3_7 = "claude-3-7-sonnet-latest"
    sonnet_3_5 = "claude-3-5-sonnet-latest"
    haiku_3_5 = "claude-3-5-haiku-latest"


class StyleDALLE(Enum):
    vivid = "vivid"
    natural = "natural"


class QualityDALLE(Enum):
    standard = "standard"
    hd = "hd"


class SizeDALLE(Enum):
    size_1024x1024 = "1024x1024"
    size_1024x1792 = "1024x1792"
    size_1792x1024 = "1792x1024"
