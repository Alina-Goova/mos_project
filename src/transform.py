import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
    filename='logs/errors.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]
    return df

def drop_duplicates_by_key(df: pd.DataFrame, key_col: str) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=[key_col], keep='first')
    after = len(df)
    if before != after:
        logging.warning(f"Удалено {before - after} дубликатов по колонке {key_col}")
    return df

def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
    if strategy == 'drop':
        before = len(df)
        df = df.dropna()
        after = len(df)
        if before != after:
            logging.warning(f"Удалено {before - after} строк с пропусками")
    elif strategy == 'fill':
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna('unknown')
    return df

def convert_to_datetime(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        invalid = df[col].isna()
        if invalid.any():
            logging.warning(f"В колонке {col} {invalid.sum()} некорректных дат")
    return df

# Очистка customers
def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = drop_duplicates_by_key(df, 'customer_id')
    # Удаляем строки с пустым customer_id (если есть)
    df = df.dropna(subset=['customer_id'])
    # Проверяем email
    if 'email' in df.columns:
        df['email'] = df['email'].fillna('')
    df = convert_to_datetime(df, 'created_at')
    # Оставляем строки, где не удалось распарсить дату, но с NaN
    return df

# Очистка orders
def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = drop_duplicates_by_key(df, 'order_id')
    # Удаляем заказы без customer_id
    df = df.dropna(subset=['customer_id'])
    df = convert_to_datetime(df, 'order_timestamp')
    # Удаляем строки с некорректной датой (там будет NaN)
    df = df.dropna(subset=['order_timestamp'])
    df = df[(df['quantity'] > 0) & (df['unit_price'] > 0)]
    df['total_amount'] = df['quantity'] * df['unit_price']
    return df

# Очистка products
def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = drop_duplicates_by_key(df, 'product_id')
    # Заменяем 'N/A' в price на NaN
    df['price'] = df['price'].replace('N/A', pd.NA)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    # Удаляем товары с некорректной ценой
    df = df.dropna(subset=['price'])
    df = df[df['price'] > 0]
    # is_active преобразуем в булево
    if 'is_active' in df.columns:
        df['is_active'] = df['is_active'].astype(str).str.lower().map({'true': True, 'false': False})
    return df

# Очистка events
def clean_events(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = drop_duplicates_by_key(df, 'event_id')
    # Удаляем события с customer_id = 999999 (ошибка)
    df = df[df['customer_id'] != 999999]
    df = convert_to_datetime(df, 'event_timestamp')
    df = df.dropna(subset=['event_timestamp'])
    return df

# Очистка payments
def clean_payments(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_column_names(df)
    df = drop_duplicates_by_key(df, 'payment_id')
    # Удаляем платежи с error_amount
    df = df[df['amount'] != 'error_amount']
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['amount'])
    df = df[df['amount'] > 0]
    df = convert_to_datetime(df, 'payment_timestamp')
    df = df.dropna(subset=['payment_timestamp'])
    return df

def transform_all(raw_data: dict) -> dict:
    cleaned = {}
    if 'customers' in raw_data:
        cleaned['customers'] = clean_customers(raw_data['customers'])
        print(f"Очищено customers: {len(cleaned['customers'])} записей")
    if 'orders' in raw_data:
        cleaned['orders'] = clean_orders(raw_data['orders'])
        print(f"Очищено orders: {len(cleaned['orders'])} записей")
    if 'products' in raw_data:
        cleaned['products'] = clean_products(raw_data['products'])
        print(f"Очищено products: {len(cleaned['products'])} записей")
    if 'events' in raw_data:
        cleaned['events'] = clean_events(raw_data['events'])
        print(f"Очищено events: {len(cleaned['events'])} записей")
    if 'payments' in raw_data:
        cleaned['payments'] = clean_payments(raw_data['payments'])
        print(f"Очищено payments: {len(cleaned['payments'])} записей")
    return cleaned