import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/test_db')

def get_engine():
    return create_engine(DATABASE_URL)

def create_schema():
    engine = get_engine()
    with open('ddl/create_tables.sql', 'r') as f:
        sql = f.read()
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print("Схема DWH создана")

def load_dimension(df: pd.DataFrame, table_name: str, engine):
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Загружено {len(df)} записей в {table_name}")

def load_fact(df: pd.DataFrame, table_name: str, engine):
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Загружено {len(df)} записей в {table_name}")

# Добавляет в dim_products товары, которых нет, но они есть в заказах
def add_missing_products(engine, fact_orders):
    with engine.connect() as conn:
        order_products = fact_orders['product_id'].unique()
        existing = pd.read_sql("SELECT product_id FROM dim_products", engine)
        existing_ids = set(existing['product_id'])
        missing = set(order_products) - existing_ids
        
        if missing:
            print(f"Найдено {len(missing)} недостающих товаров. Добавляем.")
            missing_df = pd.DataFrame({
                'product_id': list(missing),
                'product_name': ['Unknown Product'] * len(missing),
                'category': ['Unknown'] * len(missing),
                'price': [0.0] * len(missing),
                'currency': ['USD'] * len(missing),
                'is_active': [False] * len(missing)
            })
            missing_df.to_sql('dim_products', engine, if_exists='append', index=False)
            print(f"Добавлено {len(missing)} товаров в dim_products")

# Добавляет в dim_customers клиентов, которых нет, но они есть в заказах
def add_missing_customers(engine, fact_orders):
    with engine.connect() as conn:
        order_customers = fact_orders['customer_id'].unique()
        existing = pd.read_sql("SELECT customer_id FROM dim_customers", engine)
        existing_ids = set(existing['customer_id'])
        missing = set(order_customers) - existing_ids
        
        if missing:
            print(f"Найдено {len(missing)} недостающих клиентов. Добавляем.")
            missing_df = pd.DataFrame({
                'customer_id': list(missing),
                'full_name': ['Unknown Customer'] * len(missing),
                'email': [''] * len(missing),
                'phone': [''] * len(missing),
                'city': ['Unknown'] * len(missing),
                'created_at': [pd.NaT] * len(missing)
            })
            missing_df.to_sql('dim_customers', engine, if_exists='append', index=False)
            print(f"Добавлено {len(missing)} клиентов в dim_customers")

def load_all(cleaned_data: dict):
    engine = get_engine()
    create_schema()

    if 'customers' in cleaned_data:
        load_dimension(cleaned_data['customers'], 'dim_customers', engine)
    if 'products' in cleaned_data:
        load_dimension(cleaned_data['products'], 'dim_products', engine)

    if 'orders' in cleaned_data:
        dates = pd.to_datetime(cleaned_data['orders']['order_timestamp']).dt.date.unique()
        dim_date = pd.DataFrame({
            'date_id': dates,
            'year': [d.year for d in dates],
            'quarter': [d.month for d in dates],
            'month': [d.month for d in dates],
            'month_name': [d.strftime('%B') for d in dates],
            'day': [d.day for d in dates],
            'day_of_week': [d.weekday() + 1 for d in dates],
            'is_weekend': [d.weekday() >= 5 for d in dates]
        })
        load_dimension(dim_date, 'dim_date', engine)

    if 'orders' in cleaned_data:
        fact_orders = cleaned_data['orders'][['order_id', 'customer_id', 'product_id', 'order_timestamp', 'quantity', 'unit_price', 'currency', 'total_amount', 'status']].copy()
        fact_orders = fact_orders.rename(columns={'order_timestamp': 'order_date'})
        
        # Добавляем недостающие сущности
        add_missing_products(engine, fact_orders)
        add_missing_customers(engine, fact_orders)
        
        load_fact(fact_orders, 'fact_orders', engine)

    if 'payments' in cleaned_data:
        payments = cleaned_data['payments'][['payment_id', 'order_id', 'amount', 'currency', 'payment_method', 'payment_timestamp']].copy()
        payments = payments.rename(columns={'payment_timestamp': 'payment_date'})
        load_dimension(payments, 'dim_payments', engine)