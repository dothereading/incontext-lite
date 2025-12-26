import os
import sys
import yaml
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("LLM_OPENROUTER_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.getenv("MODEL", "openai/gpt-4o-mini")  # Default to a reliable, cost-effective model

def load_prompts(filepath: str = "prompts.yaml") -> dict:
    """Loads prompt templates from a YAML file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing {filepath}: {e}")
        sys.exit(1)

def call_llm(prompt: str) -> str:
    """Sends a prompt to the LLM API and returns the response text."""
    if not API_KEY:
        print("Error: LLM_OPENROUTER_KEY not found in environment variables.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raise error for 4xx/5xx status codes
        
        data = response.json()
        
        if "error" in data:
            print(f"API Error: {data['error']}")
            sys.exit(1)
            
        return data["choices"][0]["message"]["content"]
        
    except requests.exceptions.RequestException as e:
        print(f"Network or API Error: {e}")
        sys.exit(1)
    except (KeyError, IndexError) as e:
        print(f"Unexpected API response format: {e}")
        sys.exit(1)

def simplify_article(article: str, language: str, level: str, prompts: dict) -> str:
    """Generates a simplified version of the article."""
    prompt = prompts["simplify_article"].format(language=language, level=level, article=article)
    return call_llm(prompt)

def generate_questions(simplified_article: str, language: str, level: str, prompts: dict) -> str:
    """Generates comprehension questions based on the simplified article."""
    prompt = prompts["generate_questions"].format(language=language, level=level, simplified_article=simplified_article)
    return call_llm(prompt)

def main():
    # 1. Load resources
    prompts = load_prompts()
    
    try:
        with open("article.txt", "r", encoding="utf-8") as f:
            article = f.read()
    except FileNotFoundError:
        print("Error: article.txt not found. Please create it with the text you want to simplify.")
        sys.exit(1)

    # 2. Get user input
    print("--- Article Simplifier ---")
    language = input("Target Language: ").strip()
    level = input("Target Level (e.g., A2, Intermediate): ").strip()

    if not language or not level:
        print("Error: Language and Level are required.")
        sys.exit(1)

    # 3. Process article
    print("\nSimplifying article...")
    simplified = simplify_article(article, language, level, prompts)

    paragraphs = simplified.split("\n\n")
    print("\n--- PREVIEW ---\n")
    print("\n\n".join(paragraphs[:2]))
    print("\n...\n")

    print("Generating questions...")
    qa_content = generate_questions(simplified, language, level, prompts)

    # 4. Format output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "simplifications"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"simplified_{timestamp}.txt")
    
    file_content = simplified + "\n\n" + "-" * 40 + "\n\n"
    
    # Attempt to split questions and answers for formatting
    parts = qa_content.split("### ANSWERS ###")
    if len(parts) == 2:
        questions = parts[0].strip()
        answers = parts[1].strip()
        file_content += "COMPREHENSION QUESTIONS\n\n"
        file_content += questions
        file_content += "\n\n" + "\n" * 50 + "\n\n" # Add vertical spacing to hide answers
        file_content += "ANSWERS\n\n"
        file_content += answers
    else:
        file_content += qa_content

    # 5. Save to file
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(file_content)
        print(f"Success! Check {filename} for the full article, questions, and answers.")
    except IOError as e:
        print(f"Error saving file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
