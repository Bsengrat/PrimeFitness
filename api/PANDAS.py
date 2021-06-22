import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db', echo=False)

df = pd.read_excel('Base_Food.xlsx')
data = pd.DataFrame(df, columns = ['Display_Name', 'Portion_Amount', 'Calories'])
print(data)


#df.to_sql('food', con=engine)
engine.exceute("SELECT * FROM food").fetchall()

