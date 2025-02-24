import sqlite3

def initialize_db():
    conn = sqlite3.connect("videos.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
                      id TEXT PRIMARY KEY,
                      title TEXT,
                      description TEXT)''')
    conn.commit()
    conn.close()

def save_videos_to_db(videos):
    conn = sqlite3.connect("videos.db")
    cursor = conn.cursor()
    for video in videos:
        cursor.execute("INSERT OR IGNORE INTO videos VALUES (?, ?, ?)", 
                       (video['id'], video['title'], video['desc']))
    conn.commit()
    conn.close()

def search_videos(query):
    conn = sqlite3.connect("videos.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM videos WHERE title LIKE ? OR description LIKE ?", (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()
    
    conn.close()
    return results

def get_videos(query: str):
    """
    Функция для поиска видео в базе данных по запросу.
    :param query: Строка поиска.
    :return: Список найденных видео в формате словарей.
    """
    results = search_videos(query)
    videos = [{"id": row[0], "title": row[1], "description": row[2]} for row in results]
    return videos

# Инициализация базы данных при запуске
initialize_db()

# Пример вызова функции поиска
analysis_result = "example query"
youtube_results = get_videos(str(analysis_result))
