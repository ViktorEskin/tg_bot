import logging
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize

# Настройка логирования
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

nltk.download('punkt')

def analyze_query(query):
    logging.info("Анализ запроса: %s", query)
    tokens = word_tokenize(query)
    logging.info("Результат токенизации: %s", tokens)
    return tokens

def search_videos(query):
    logging.info("Поиск видео по запросу: %s", query)
    try:
        conn = sqlite3.connect("videos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description FROM videos")
        videos = cursor.fetchall()
        conn.close()

        if not videos:
            logging.warning("В базе данных нет видео.")
            return None

        texts = [video[1] + " " + video[2] for video in videos]
        video_ids = [video[0] for video in videos]

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts)
        query_vector = vectorizer.transform([query])

        similarities = (tfidf_matrix * query_vector.T).toarray()
        best_match_index = similarities.argmax()
        best_match_score = similarities.max()

        logging.info("Лучший индекс совпадения: %d, Оценка: %f", best_match_index, best_match_score)

        return video_ids[best_match_index] if best_match_score > 0 else None
    except Exception as e:
        logging.error("Ошибка при поиске видео: %s", str(e))
        return None
