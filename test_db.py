import sqlite3 
 
try: 
    conn = sqlite3.connect("money_tracker.db") 
    print("SQLite подключение работает!") 
    conn.close() 
except Exception as e: 
    print(f"Ошибка: {e}") 
