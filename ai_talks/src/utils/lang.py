from dataclasses import dataclass
from typing import List  # NOQA: UP035

from .constants import AI_ROLE_OPTIONS_EN, AI_ROLE_OPTIONS_RU, AI_TALKS_URL, README_URL


@dataclass
class Locale:
    ai_role_options: List[str]
    ai_role_prefix: str
    ai_role_postfix: str
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
    speak_btn: str
    input_kind: str
    input_kind_1: str
    input_kind_2: str
    select_placeholder1: str
    select_placeholder2: str
    select_placeholder3: str
    radio_placeholder: str
    radio_text1: str
    radio_text2: str
    stt_placeholder: str
    footer_title: str
    footer_option0: str
    footer_option1: str
    footer_option2: str
    footer_chat: str
    footer_channel: str
    responsibility_denial: str
    donates_info: str
    tokens_count: str
    message_cost: str
    total_cost: str
    empty_api_handler: str


# --- LOCALE SETTINGS ---
en = Locale(
    ai_role_options=AI_ROLE_OPTIONS_EN,
    ai_role_prefix="You are a female",
    ai_role_postfix="Answer as concisely as possible.",
    title="AI Talks",
    language="English",
    lang_code="en",
    donates="Donates",
    donates1="Russia",
    donates2="World",
    chat_placeholder="Start Your Conversation With AI:",
    chat_run_btn="Ask",
    chat_clear_btn="Clear",
    chat_save_btn="Save",
    speak_btn="Push to Speak",
    input_kind="Input Kind",
    input_kind_1="Text",
    input_kind_2="Voice [test mode]",
    select_placeholder1="Select Model",
    select_placeholder2="Select Role",
    select_placeholder3="Create Role",
    radio_placeholder="Role Interaction",
    radio_text1="Select",
    radio_text2="Create",
    stt_placeholder="To Hear The Voice Of AI Press Play",
    footer_title="Support & Feedback",
    footer_option0="Chat",
    footer_option1="Info",
    footer_option2="Donate",
    footer_chat="AI Talks Chat",
    footer_channel="AI Talks Channel",
    responsibility_denial="""
        `AI Talks` uses the `Open AI` API to interact with `ChatGPT`, an AI that generates information.
        Please note that neural network responses may not be reliable, inaccurate or irrelevant.
        We are not responsible for any consequences associated with the use or reliance on the information provided.
        Use the received data at your discretion.
    """,
    donates_info="""
        `AI Talks` collects donations solely for the purpose of paying for the `Open AI` API.
        This allows you to provide access to communication with AI for all users.
        Support us for joint development and interaction with the intelligence of the future!
    """,
    tokens_count="Tokens count: ",
    message_cost="Message cost: ",
    total_cost="Total cost of conversation: ",
    empty_api_handler=f"""
        API key not found. Create `.streamlit/secrets.toml` with your API key.
        See [README.md]({README_URL}) for instructions or use the original [AI Talks]({AI_TALKS_URL}).
    """,
)

ru = Locale(
    ai_role_options=AI_ROLE_OPTIONS_RU,
    ai_role_prefix="Вы девушка",
    ai_role_postfix="Отвечай максимально лаконично.",
    title="Разговорчики с ИИ",
    language="Russian",
    lang_code="ru",
    donates="Поддержать Проект",
    donates1="Россия",
    donates2="Остальной Мир",
    chat_placeholder="Начните Вашу Беседу с ИИ:",
    chat_run_btn="Спросить",
    chat_clear_btn="Очистить",
    chat_save_btn="Сохранить",
    speak_btn="Нажмите и Говорите",
    input_kind="Вид ввода",
    input_kind_1="Текст",
    input_kind_2="Голос [тестовый режим]",
    select_placeholder1="Выберите Модель",
    select_placeholder2="Выберите Роль",
    select_placeholder3="Создайте Роль",
    radio_placeholder="Взаимодествие с Ролью",
    radio_text1="Выбрать",
    radio_text2="Создать",
    stt_placeholder="Чтобы Услышать ИИ Нажми Кнопку Проигрывателя",
    footer_title="Поддержка и Обратная Связь",
    footer_option0="Чат",
    footer_option1="Инфо",
    footer_option2="Донаты",
    footer_chat="Чат Разговорчики с ИИ",
    footer_channel="Канал Разговорчики с ИИ",
    responsibility_denial="""
        `Разговорчики с ИИ` использует API `Open AI` для взаимодействия с `ChatGPT`, ИИ, генерирующим информацию.
        Пожалуйста, учтите, что ответы нейронной сети могут быть недостоверными, неточными или нерелевантными.
        Мы не несём ответственности за любые последствия,
        связанные с использованием или доверием к информации сгенерированныой нейронной сетью.
        Используйте полученные данные генераций на своё усмотрение.
    """,
    donates_info="""
        `AI Talks` собирает донаты исключительно с целью оплаты API `Open AI`.
        Это позволяет обеспечить доступ к общению с ИИ для всех желающих пользователей.
        Поддержите нас для совместного развития и взаимодействия с интеллектом будущего!
    """,
    tokens_count="Количество токенов: ",
    message_cost="Cтоимость сообщения: ",
    total_cost="Общая стоимость разговора: ",
    empty_api_handler=f"""
        Ключ API не найден. Создайте `.streamlit/secrets.toml` с вашим ключом API.
        Инструкции см. в [README.md]({README_URL}) или используйте оригинальный [AI Talks]({AI_TALKS_URL}).
    """,
)
