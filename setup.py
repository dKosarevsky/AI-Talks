from setuptools import setup, find_packages

# Read the contents of the requirements.txt file
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f.readlines() if not line.startswith("-f")]

setup(
    name="ai-talks",
    version="0.8.8.2",
    exclude_package_data={"": ["secrets.toml"]},
    packages=find_packages(exclude=["secrets.toml", ]),
    install_requires=requirements,  # Use the parsed requirements here
    entry_points={
        "console_scripts": [
            "ai-talks=pkg.run_agi:main",
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
