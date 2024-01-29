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
    gpt4_turbo_preview = "gpt-4-turbo-preview"
    gpt4_0125_preview = "gpt-4-0125-preview"
    gpt4_1106_preview = "gpt-4-1106-preview"

    gpt4_vision_preview = "gpt-4-vision-preview"

    gpt4 = "gpt-4"
    gpt4_0613 = "gpt-4-0613"
    gpt4_32k = "gpt-4-32k"
    gpt4_32k_0613 = "gpt-4-32k-0613"

    gpt35_turbo = "gpt-3.5-turbo"
    gpt35_turbo_1106 = "gpt-3.5-turbo-1106"
    gpt35_turbo_16k = "gpt-3.5-turbo-16k"

    gpt35_turbo_instruct = "gpt-3.5-turbo-instruct"

    dalle_3 = "dall-e-3"


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
