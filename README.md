# teaGPT
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://teagpt-ml.streamlit.app)

![](ai_talks/assets/img/ai_face.png)

A ChatGPT API wrapper, providing a user-friendly Streamlit web interface.

Enhance your ChatGPT experience with our user-friendly API wrapper, featuring a seamless Streamlit web interface. Effortlessly interact with ChatGPT, while enjoying an intuitive and responsive design. Discover simplified access to advanced AI technology in just a few clicks.

<details>
   <summary>Demo</summary>

![](ai_talks/assets/demo/ai-talks.gif)

<details>
   <summary>Tokens counting</summary>

![](ai_talks/assets/demo/ai-talks-tokens.gif)

</details>

</details>

## Setup

1. Clone repo:

```bash
git clone https://github.com/b08x/teaGPT.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add API key to `.streamlit/secrets.toml`

```toml
[api_credentials]
api_key = "sk-..."
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

Once the script is started, you can go to the URL [http://localhost:8501](http://localhost:8501) to start using the bot.

## License


## Donation
