import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

engine_url = os.getenv('ENGINE_URL')

def retrieve_data_as_dataframe(table_name):
    engine = create_engine(engine_url)

    query = f'SELECT * FROM "{table_name}";'
    df_from_db = pd.read_sql(query, con=engine)
    return df_from_db

TABLE_name = 'CANDIDATE'

candidate_df = retrieve_data_as_dataframe(TABLE_name)
print("Candidate data from the table ", candidate_df.head())
print(f" The dataframe size is : {candidate_df.shape} " )


