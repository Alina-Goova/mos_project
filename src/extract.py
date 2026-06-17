import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def extract_csv(filepath: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(filepath, **kwargs)

def extract_json(filepath: str) -> pd.DataFrame:
    return pd.read_json(filepath)

def extract_excel(filepath: str, sheet_name: str = 0) -> pd.DataFrame:
    return pd.read_excel(filepath, sheet_name=sheet_name)

def extract_xml(filepath: str) -> pd.DataFrame:
    return pd.read_xml(filepath)

def extract_all() -> dict:
    data = {}

    customers_path = DATA_DIR / "customers.csv"
    if customers_path.exists():
        data['customers'] = extract_csv(customers_path, dtype={'customer_id': int})
        print(f"Загружено customers: {len(data['customers'])} записей")

    orders_path = DATA_DIR / "orders.json"
    if orders_path.exists():
        data['orders'] = extract_json(orders_path)
        print(f"Загружено orders: {len(data['orders'])} записей")

    products_path = DATA_DIR / "products.xlsx"
    if products_path.exists():
        data['products'] = extract_excel(products_path, sheet_name='products')
        print(f"Загружено products: {len(data['products'])} записей")

    events_path = DATA_DIR / "events.xml"
    if events_path.exists():
        data['events'] = extract_xml(events_path)
        print(f"Загружено events: {len(data['events'])} записей")

    payments_path = DATA_DIR / "payments.csv"
    if payments_path.exists():
        data['payments'] = extract_csv(payments_path, sep='^', dtype={'payment_id': int})
        print(f"Загружено payments: {len(data['payments'])} записей")

    return data