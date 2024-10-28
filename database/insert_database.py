import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine_url = os.getenv('ENGINE_URL')

def insert_data_into_table(table_name, csv_files):
    engine = create_engine(engine_url)
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Data inserted successfully into {table_name}!")

# insert_data_into_table(table_name = 'CANDIDATE', csv_files = ['../datafetch/combined_profiles.csv'])
