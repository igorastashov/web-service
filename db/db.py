import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = ('postgresql://astashovivl:uCAG29k5zuu6NXYtOg123tUar4YjX4Af@dpg-cm256n6n7f5s73es9d0g-a'
                           '.frankfurt-postgres.render.com/db_postgres_n2ov')

dogs_data = {
    'name': ['Bob', 'Marli', 'Snoopy', 'Rex', 'Pongo', 'Tillman', 'Uga'],
    'pk': list(range(7)),
    'kind': ['terrier', 'bulldog', 'dalmatian', 'dalmatian', 'dalmatian', 'bulldog', 'bulldog']
}

timestamps_data = {
    'id': [0, 1],
    'timestamp': [12, 10]
}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

# populate database with existing data
for data_name, data in zip(
        ['dogs', 'timestamps'],
        [dogs_data, timestamps_data]
):
    df = pd.DataFrame.from_dict(data)
    df.to_sql(data_name, engine, index=False, if_exists='replace')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
