import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')
cur = conn.cursor()
def update_backup(table,filename,cursor):

    cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table)))
    data = cursor.fetchall()
    with open('schedule/dbTableBackups/{}'.format(filename),'w') as file:
        for line in data:
            file.write(str(line))
            file.write(str("\n"))

update_backup('employees','employees.sql',cur)
update_backup('extremes','extremes.sql',cur)
update_backup('required_skills_for_shift','required_skills_for_shift.sql',cur)
update_backup('availability','availability.sql',cur)
update_backup('skills','skills.sql',cur)
update_backup('business_info','business_info.sql',cur)
update_backup('shifts','shifts.sql',cur)
