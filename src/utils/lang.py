from dataclasses import dataclass
from typing import List


# Parent data class
@dataclass
class Locale:
    ai_role_options: List[str]
    ai_role_prefix: str
    title: str
    language: str
    lang_code: str
    donates: str
    donates1: str
    donates2: str
    chat_placeholder: str
    chat_run_btn: str
    chat_clear_btn: str
    chat_save_btn: str
    select_placeholder1: str
    select_placeholder2: str
    select_placeholder3: str
    radio_placeholder: str
    radio_text1: str
    radio_text2: str
    stt_placeholder: str
    footer_title: str
    footer_option1: str
    footer_option2: str
    footer_chat: str
    footer_channel: str


# Child data class for English
@dataclass
class EnLocale(Locale):
    ai_role_prefix: str = "You are a girl"
    title: str = "AI Talks"
    language: str = "English"
    lang_code: str = "en"
    donates: str = "Donates"
    donates1: str = "Russia"
    donates2: str = "World"
    chat_placeholder: str = "Start Your Conversation With AI:"
    chat_run_btn: str = "Run"
    chat_clear_btn: str = "Clear"
    chat_save_btn: str = "Save"
    select_placeholder1: str = "Select Model"
    select_placeholder2: str = "Select Role"
    select_placeholder3: str = "Create Role"
    radio_placeholder: str = "Role Interaction"
    radio_text1: str = "Select"
    radio_text2: str = "Create"
    stt_placeholder: str = "To Hear The Voice Of AI Press Play"
    footer_title: str = "Support & Feedback"
    footer_option1: str = "Info"
    footer_option2: str = "Donates"
    footer_chat: str = "AI Talks Chat"
    footer_channel: str = "AI Talks Channel"


# Child data class for Russian
@dataclass
class RuLocale(Locale):
    ai_role_prefix: str = "Вы девушка"
    title: str = "Разговорчики с ИИ"
    language: str = "Russian"
    lang_code: str = "ru"
    donates: str = "Поддержать Проект"
    donates1: str = "Россия"
    donates2: str = "Остальной Мир"
    chat_placeholder: str = "Начните Вашу Беседу с ИИ:"
    chat_run_btn: str = "Запустить"
    chat_clear_btn: str = "Очистить"
    chat_save_btn: str = "Сохранить"
    select_placeholder1: str = "Выберите Модель"
    select_placeholder2: str = "Выберите Роль"
    select_placeholder3: str = "Создайте Роль"
    radio_placeholder: str = "Взаимодествие с Ролью"
    radio_text1: str = "Выбрать"
    radio_text2: str = "Создать"
    stt_placeholder: str = "Чтобы Услышать ИИ Нажми Кнопку Проигрывателя"
    footer_title: str = "Поддержка и Обратная Связь"
    footer_option1: str = "Информация"
    footer_option2: str = "Задонатить"
    footer_chat: str = "Чат Разговорчики с ИИ"
    footer_channel: str = "Канал Разговорчики с ИИ"


AI_ROLE_OPTIONS_EN = [
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

AI_ROLE_OPTIONS_RU = [
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

en = EnLocale(ai_role_options=AI_ROLE_OPTIONS_EN)
ru = RuLocale(ai_role_options=AI_ROLE_OPTIONS_RU)
