import sqlite3
import pandas as pd

df = pd.read_csv("Result_1.csv")

connection = sqlite3.connect("../instance/site.db")
df.to_sql("User", connection, if_exists="replace")
connection.close()