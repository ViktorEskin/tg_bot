import openai
import os
import re
from dotenv import load_dotenv
from youtube_api import get_videos, generate_youtube_links, convert_markdown_to_telegram

# Загружаем переменные окружения
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def analyze_query_with_gpt(query):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}]
    )
    return re.sub(r'\*\*(.*?)\*\*', r'\1', (response.choices[0].message.content))

def ai_recommendation(query):
    return analyze_query_with_gpt(query)

def get_video_recommendations(query):
    """
    Получает видео по запросу, форматирует ссылки и возвращает удобный для Telegram формат с MarkdownV2.
    """
    videos = get_videos(query)
    formatted_links = generate_youtube_links(videos)
    return convert_markdown_to_telegram(formatted_links)

# Пример вызова функции:
if __name__ == "__main__":
    query = "самопознание"
    print(get_video_recommendations(query))
