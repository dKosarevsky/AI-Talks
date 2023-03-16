# Voice ChatGPT via streamlit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://voice-chat-gpt.streamlit.app)

## Настройка pre-commit хуков[^1]

С помощью pre-commit хуков можно проверять внесённые изменения на соответствие настройкам линтера и автоматически
применять форматирование кода.
Для использования pre-commit хуков необходимо:

- Установить в используемое для разработки окружение пакет pre-commit командой
  ```py
  pip install pre-commit
  ```
- Находясь в корне репозитория, выполнить из рабочего окружения команду
  ```py
  pre-commit install
  ```

После успешной установки в консоли будет выведено сообщение:

```sh
pre-commit installed at .git/hooks/pre-commit
```

Теперь при выполнении команды `git commit` будет выполняться проверка кода изменённых файлов на соответствие стандартам
с помощью библиотек, описанных в конфигурационном файле [.pre-commit-config.yaml](.pre-commit-config.yaml).

Настройки линтеров описаны в файле [pyproject.toml](pyproject.toml)

Также можно запустить проверку всех файлов с помощью команды:

```bash
pre-commit run -a
```

Либо запустить проверку для отдельного файла командой:

```bash
pre-commit run --files dags/pik_digital/pik_dags/tms_api/__init__.py
```

Важно обратить внимание на то, что в первый раз после установки хуков процесс проверки может длиться довольно долго:
pre-commit будет устанавливать необходимые среды для проверки коммитов.

[^1]: [A framework for managing and maintaining multi-language pre-commit hooks.](https://pre-commit.com/)
