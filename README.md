# ETL-пайплайн для аналитики продаж (Блок 3)

Домашнее задание выполнено в рамках отбора на стажировку по направлению «Аналитика данных».  
Реализован end-to-end ETL-пайплайн: загрузка данных из разнородных источников (CSV, JSON, Excel, XML), очистка, трансформация и загрузка в DWH (Star Schema) на PostgreSQL.

## Используемые технологии

- Python 3.9+
- Pandas (обработка данных)
- SQLAlchemy + psycopg2 (подключение к PostgreSQL)
- PostgreSQL (хранилище DWH)
- pgAdmin 4 (для просмотра данных)

## Структура проекта
```bash
.
├── README.md
├── data
│   ├── customers.csv
│   ├── events.xml
│   ├── orders.json
│   ├── payments.csv
│   └── products.xlsx
├── ddl
│   └── create_tables.sql
├── logs
│   └── errors.log
├── requirements.txt
├── sql
│   └── analytics.sql
└── src
    ├── extract.py
    ├── load.py
    ├── main.py
    └── transform.py
```

## Как запустить проект

### 1. Клонировать репозиторий

```bash
git clone 
cd mos_project
```

### 2. Создать виртуальное окружение и установить зависимости

```bash
python3 -m venv venv
source venv/bin/activate      # для Linux/macOS
# или venv\Scripts\activate   для Windows
pip install -r requirements.txt
```

### 3. Настроить базу данных PostgreSQL

Убедитесь, что PostgreSQL запущен

Создайте базу данных, например test_bd:
```postgresql
CREATE DATABASE test_bd;
```

Создайте файл .env в корне проекта и укажите строку подключения:
- DATABASE_URL=postgresql://пользователь:пароль@localhost:5432/test_bd

### 4. Запустить ETL-пайплайн
```bash
python src/main.py
```

После успешного выполнения вы увидите:

- Сообщения о загрузке и очистке данных.
- Создание таблиц в DWH (схема public).
- Загрузку данных в таблицы dim_customers, dim_products, dim_date, dim_payments, fact_orders.
