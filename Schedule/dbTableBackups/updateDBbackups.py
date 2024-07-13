import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')
cur = conn.cursor()
def update_backup(table,filename,cursor):

    cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
    data = cursor.fetchall()
    with open('Schedule/dbTableBackups/{}'.format(filename),'w') as file:
        for line in data:
            file.write(str(line))
            file.write(str("\n"))

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
for table in cur.fetchall():
    update_backup(table[0],"{}.sql".format(table[0]),cur)
