# inContext Lite: Simplify an Article for Language Learning

This tool simplifies articles into a target language and level, and generates comprehension questions to test understanding. It uses an LLM (via OpenRouter) to process the text. This is meant to be a quick, customizable version of the inContext Notebook. For the full experience, check out [incontextlearning.com](https://incontextlearning.com). 

## Features

- **Simplify Articles**: Rewrites complex text into your desired language and proficiency level (e.g., Spanish A2).
- **Generate Questions**: Creates comprehension questions based on the simplified text.
- **Customizable Prompts**: Uses a YAML file for easy prompt engineering.
- **Output Management**: Saves results to timestamped text files with a preview in the terminal.

## Prerequisites

- Python 3.8+
- An OpenRouter API key (or compatible OpenAI-style API)

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install requests python-dotenv pyyaml
    ```

2.  **Configure Environment**:
    Create a `.env` file in the project root and add your API key:
    ```env
    LLM_OPENROUTER_KEY=your_api_key_here
    MODEL=openai/gpt-5-mini 
    ```

3.  **Prepare Input**:
    Create a file named `article.txt` in the same directory and paste the text you want to simplify into it.

## Usage

Run the script from the terminal:

```bash
python3 main.py [article_path] [--language LANGUAGE] [--level LEVEL]
```

### Examples

**Interactive Mode (prompts for input):**
```bash
python3 main.py
```

**With Arguments:**
```bash
python3 main.py my_article.txt --language Spanish --level B2
```

**Mix and Match:**
```bash
python3 main.py --language French
# Will use default article.txt and prompt for level
```

The script will generate a new file in the `simplifications/` folder named `simplified_YYYYMMDD_HHMMSS.txt` containing:
- The simplified article.
- Comprehension questions.
- Answers (hidden at the bottom of the file).

## Customization

You can modify the `prompts.yaml` file to change how the AI simplifies text or generates questions.

```yaml
simplify_article: |
  Goal: Rewrite the article below in {language}...
  ...
```
