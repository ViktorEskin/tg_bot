import os
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json

# Загружаем переменные окружения
load_dotenv()

API_KEY = os.getenv("API_KEY")  # Используем переменную окружения
CHANNEL_ID = os.getenv("CHANNEL_ID")

youtube = build("youtube", "v3", developerKey=API_KEY)

def get_videos(query):
    """
    Выполняет поиск видео на YouTube по заданному запросу.
    Возвращает список словарей с id и title видео.
    """
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=CHANNEL_ID,
            maxResults=10,
            order="date",
            q=query  # Добавляем параметр запроса
        )
        response = request.execute()
    except Exception as e:
        print(f"Ошибка запроса к API: {e}")
        return []

    videos = []
    for item in response.get("items", []):
        video_id = item["id"].get("videoId")
        if not video_id:
            continue
        videos.append({
            "id": video_id,
            "title": item["snippet"]["title"],
        })

    return videos

def remove_hashtags(title):
    """
    Удаляет хештеги из заголовка видео.
    """
    return re.sub(r"#\S+", "", title).strip()

def generate_youtube_links(videos):
    """
    Преобразует список видео в формат ссылок для отправки пользователю.
    Удаляет хештеги из заголовков.
    """
    if not videos:
        return "Видео не найдены."

    links = [f"🔗 {remove_hashtags(video['title'])} - https://www.youtube.com/watch?v={video['id']}" for video in videos]
    return "\n".join(links)

def convert_markdown_to_telegram(text):
    """
    Преобразует ссылки из Markdown-формата в формат, понятный Telegram.
    """
    markdown_link_pattern = r"\[([^\]]+)\]\((https?://[^\)]+)\)"
    
    def replace_match(match):
        title = match.group(1)
        url = match.group(2)
        return f"🔗 {title} - {url}"
    
    converted_text = re.sub(markdown_link_pattern, replace_match, text)
    return converted_text

# Пример использования
if __name__ == "__main__":
    # query = "психология"
    videos = get_videos(query)
    formatted_links = generate_youtube_links(videos)
    print(convert_markdown_to_telegram(formatted_links))
