from setuptools import setup, find_packages

# Read the contents of the requirements.txt file
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f.readlines() if not line.startswith("-f")]

setup(
    name="ai-talks",
    version="0.9.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,  # Use the parsed requirements here
    entry_points={
        "console_scripts": [
            "ai-talks=ai_talks.chat:run_agi",
        ],
    },
    author="Dmitry Kosarevsky",
    author_email="if.kosarevsky@gmail.com",
    description="A ChatGPT API wrapper, providing a user-friendly Streamlit web interface",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dKosarevsky/AI-Talks",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="ai agi streamlit streamlit-component chat bot gpt llm",
    python_requires=">=3.10",
)
