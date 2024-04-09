import sqlite3
import requests
import json
from datetime import datetime

class Test:
    def __init__(self, x:int, y:int):
        # Проверяем, что x и y являются числами
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise ValueError("Аргументы x и y должны быть числами")

        self.x = x
        self.y = y
        self.connection = sqlite3.connect('quiz_database.db')
        self.cursor = self.connection.cursor()

        # Создаем таблицу для хранения вопросов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                category TEXT,
                question TEXT,
                answer TEXT,
                UNIQUE(category, question, answer)
            )
        ''')
        self.connection.commit()

    def get_question(self):
        # Получаем викторину с https://jservice.io/
        response = requests.get(f'https://jservice.io/api/random?count={self.x}')
        data = response.json()

        # Проверяем уникальность вопроса и записываем его в базу данных
        for item in data:
            category = item['category']['title']
            question = item['question']
            answer = item['answer']

            self.cursor.execute('INSERT OR IGNORE INTO questions VALUES (?, ?, ?)', (category, question, answer))

        self.connection.commit()

    def get_category_count(self, category):
        # Получаем количество записей в указанной категории
        self.cursor.execute('SELECT COUNT(*) FROM questions WHERE category = ?', (category,))
        count = self.cursor.fetchone()[0]
        return count

    def get_y_questions(self):
        # Получаем y записей из базы данных
        self.cursor.execute('SELECT * FROM questions LIMIT ?', (self.y,))
        rows = self.cursor.fetchall()

        # Создаем JSON с данными и сохраняем его с названием текущей даты
        current_date = datetime.now().strftime("%Y-%m-%d")
        with open(f'questions_{current_date}.json', 'w') as f:
            json.dump(rows, f)

    def close_connection(self):
        # Закрываем соединение с базой данных
        self.connection.close()

# Пример использования класса Test
test_instance = Test(10, 5)
test_instance.get_question()
print(test_instance.get_category_count('Science'))
test_instance.get_y_questions()
test_instance.close_connection()
