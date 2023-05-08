from dataclasses import dataclass
from typing import List  # NOQA: UP035

from .constants import ADMIN_TG, AI_ROLE_OPTIONS_EN, AI_ROLE_OPTIONS_RU, AI_TALKS_URL, README_URL


@dataclass
class Locale:
    ai_role_options: List[str]
    ai_role_prefix: str
    title: str
    language: str
    lang_code: str
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
    tokens_count: str
    message_cost: str
    total_cost: str
    sum_tokens: str
    available_tokens: str
    activate: str
    greetings: str
    username: str
    password: str
    login: str
    logining: str
    register: str
    registration: str
    logout: str
    empty_api_handler: str
    balance_handler: str


# --- LOCALE SETTINGS ---
en = Locale(
    ai_role_options=AI_ROLE_OPTIONS_EN,
    ai_role_prefix="You are a female",
    title="AI Talks",
    language="English",
    lang_code="en",
    chat_placeholder="Start Your Conversation With AI:",
    chat_run_btn="Ask",
    chat_clear_btn="Clear",
    chat_save_btn="Save",
    select_placeholder1="Select Model",
    select_placeholder2="Select Role",
    select_placeholder3="Create Role",
    radio_placeholder="Role Interaction",
    radio_text1="Select",
    radio_text2="Create",
    tokens_count="Tokens count: ",
    message_cost="Message cost: ",
    total_cost="Total cost of conversation: ",
    sum_tokens="Tokens sum: ",
    available_tokens="Available Tokens: ",
    activate=f"Account Activating is required. Contact [Admin]({ADMIN_TG}).",
    greetings="Hey, ",
    username="Username:",
    password="Password:",  # noqa: S106
    login="Login",
    logining="login ...",
    register="Register",
    registration="registration ...",
    logout="Logout",
    empty_api_handler=f"""
        API key not found. Create `.streamlit/secrets.toml` with your API key.
        See [README.md]({README_URL}) for instructions or use the original [AI Talks]({AI_TALKS_URL}).
    """,
    balance_handler="Balance: ",
)

ru = Locale(
    ai_role_options=AI_ROLE_OPTIONS_RU,
    ai_role_prefix="Вы девушка",
    title="Разговорчики с ИИ",
    language="Russian",
    lang_code="ru",
    chat_placeholder="Начните Вашу Беседу с ИИ:",
    chat_run_btn="Спросить",
    chat_clear_btn="Очистить",
    chat_save_btn="Сохранить",
    select_placeholder1="Выберите Модель",
    select_placeholder2="Выберите Роль",
    select_placeholder3="Создайте Роль",
    radio_placeholder="Взаимодействие с Ролью",
    radio_text1="Выбрать",
    radio_text2="Создать",
    tokens_count="Количество токенов: ",
    message_cost="Стоимость сообщения: ",
    total_cost="Общая стоимость разговора: ",
    sum_tokens="Сумма токенов: ",
    available_tokens="Доступные Токены: ",
    activate=f"Необходима активация. Свяжитесь с [Администратором]({ADMIN_TG}).",
    greetings="Привет, ",
    username="Имя Пользователя:",
    password="Пароль:",  # noqa: S106
    login="Войти",
    logining="входим ...",
    register="Зарегистрироваться",
    registration="регистрация ...",
    logout="Выйти",
    empty_api_handler=f"""
        Ключ API не найден. Создайте `.streamlit/secrets.toml` с вашим ключом API.
        Инструкции см. в [README.md]({README_URL}) или используйте оригинальный [AI Talks]({AI_TALKS_URL}).
    """,
    balance_handler="Баланс: ",
)
