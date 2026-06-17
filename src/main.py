import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extract import extract_all
from src.transform import transform_all
from src.load import load_all

def run_etl():
    print("Запуск ETL-пайплайна")
    raw = extract_all()
    cleaned = transform_all(raw)
    load_all(cleaned)
    print("ETL завершён")

if __name__ == "__main__":
    run_etl()