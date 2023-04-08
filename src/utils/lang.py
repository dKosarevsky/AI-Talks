from dataclasses import dataclass
from typing import List


# Parent data class
@dataclass
class Locale:
    ai_role_options: List[str]


# Child data class for English
@dataclass
class EnLocale(Locale):
    ai_role_prefix: str = "You are a female"
    ai_role_postfix: str = "Answer as concisely as possible with a little humor expression."
    title: str = "AI Talks"
    language: str = "English"
    lang_code: str = "en"
    donates: str = "Donates"
    donates1: str = "Russia"
    donates2: str = "World"
    chat_placeholder: str = "Start Your Conversation With AI:"
    chat_run_btn: str = "Ask"
    chat_clear_btn: str = "Clear"
    chat_save_btn: str = "Save"
    speak_btn: str = "Push to Speak"
    input_kind: str = "Input Kind"
    input_kind_1: str = "Text"
    input_kind_2: str = "Voice [test mode]"
    select_placeholder1: str = "Select Model"
    select_placeholder2: str = "Select Role"
    select_placeholder3: str = "Create Role"
    radio_placeholder: str = "Role Interaction"
    radio_text1: str = "Select"
    radio_text2: str = "Create"
    stt_placeholder: str = "To Hear The Voice Of AI Press Play"
    footer_title: str = "Support & Feedback"
    footer_option0: str = "Chat"
    footer_option1: str = "Info"
    footer_option2: str = "Donates"
    footer_chat: str = "AI Talks Chat"
    footer_channel: str = "AI Talks Channel"
    responsibility_denial: str = """
    `AI Talks` uses the `Open AI` API to interact with `ChatGPT`, an AI that generates information.
    Please note that neural network responses may not be reliable, inaccurate or irrelevant.
    We are not responsible for any consequences associated with the use or reliance on the information provided.
    Use the received data at your discretion.
    """
    donates_info: str = """
    `AI Talks` collects donations solely for the purpose of paying for the `Open AI` API.
    This allows you to provide access to communication with AI for all users.
    Support us for joint development and interaction with the intelligence of the future!
    """


# Child data class for Russian
@dataclass
class RuLocale(Locale):
    ai_role_prefix: str = "Вы девушка"
    ai_role_postfix: str = "Отвечай максимально лаконично, с легким налётом юмора."
    title: str = "Разговорчики с ИИ"
    language: str = "Russian"
    lang_code: str = "ru"
    donates: str = "Поддержать Проект"
    donates1: str = "Россия"
    donates2: str = "Остальной Мир"
    chat_placeholder: str = "Начните Вашу Беседу с ИИ:"
    chat_run_btn: str = "Спросить"
    chat_clear_btn: str = "Очистить"
    chat_save_btn: str = "Сохранить"
    speak_btn: str = "Нажмите и Говорите"
    input_kind: str = "Вид ввода"
    input_kind_1: str = "Текст"
    input_kind_2: str = "Голос [тестовый режим]"
    select_placeholder1: str = "Выберите Модель"
    select_placeholder2: str = "Выберите Роль"
    select_placeholder3: str = "Создайте Роль"
    radio_placeholder: str = "Взаимодествие с Ролью"
    radio_text1: str = "Выбрать"
    radio_text2: str = "Создать"
    stt_placeholder: str = "Чтобы Услышать ИИ Нажми Кнопку Проигрывателя"
    footer_title: str = "Поддержка и Обратная Связь"
    footer_option0: str = "Чат"
    footer_option1: str = "Информация"
    footer_option2: str = "Задонатить"
    footer_chat: str = "Чат Разговорчики с ИИ"
    footer_channel: str = "Канал Разговорчики с ИИ"
    responsibility_denial: str = """
    `Разговорчики с ИИ` использует API `Open AI` для взаимодействия с `ChatGPT`, ИИ, генерирующим информацию.
    Пожалуйста, учтите, что ответы нейронной сети могут быть недостоверными, неточными или нерелевантными.
    Мы не несём ответственности за любые последствия,
    связанные с использованием или доверием к информации сгенерированныой нейронной сетью.
    Используйте полученные данные генераций на своё усмотрение.
    """
    donates_info: str = """
    `AI Talks` собирает донаты исключительно с целью оплаты API `Open AI`.
    Это позволяет обеспечить доступ к общению с ИИ для всех желающих пользователей.
    Поддержите нас для совместного развития и взаимодействия с интеллектом будущего!
    """


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
