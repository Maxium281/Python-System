import sqlite3

db='database/interview.db'
conn=sqlite3.connect(db)
cur=conn.cursor()
print('questions schema:')
for row in cur.execute("PRAGMA table_info('questions')"):
    print(row)
print('\nanswers schema:')
for row in cur.execute("PRAGMA table_info('answers')"):
    print(row)
conn.close()
