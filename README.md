# AI Talks

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-talks.streamlit.app)

## ChatGPT Assistant via Streamlit

AI Talks is a Streamlit app, that ...

## Installation

Clone the repository:

```bash
git clone https://github.com/dKosarevsky/AI-Talks.git
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Add your API keys into `.streamlit/secrets.toml`:

```toml
[api_credentials]
api_key = "sk-..."
bard_session = "..."
```

## Usage

To run the app use the following command:

```bash
bash run.sh
```

Another way:

```bash
streamlit run chat.py
```

## License

This project is released under the MIT License.
