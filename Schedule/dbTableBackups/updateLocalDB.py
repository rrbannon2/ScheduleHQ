import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')
cur = conn.cursor()

def load_table_data(table_file_name,table_name):
    with open(table_file_name,'r') as table_file:
        if table_name in ['employees','extremes','skills'] :
            for line in table_file.readlines():
                line = line.replace("'","").replace('(','').replace(')','').replace('\n','').split(", ")
                update_table_data(table_name, line)
        elif table_name == 'availability':
            for line in table_file.readlines():
                line = line.split('[')
                line[0] = line[0].replace("(","").replace(", ","").replace("'","")
                line[1] = line[1].replace("])","").replace("\n","").replace(" ","").split(",")
                line[1] = [int(i) for i in line[1]]
                update_table_data(table_name, line)
        elif table_name in ['business_info','required_skills_for_shift','shifts']:
            for line in table_file.readlines():
                line = line.split('[')
                line[0] = line[0].replace("(","").replace(", ","").replace("'","")
                line[1] = line[1].replace("'","")
                line[1] = line[1].split("]")
                integer_vals = line[1][1]
                integer_vals = integer_vals.replace(")","").replace("\n","").split(", ")[1:]
                line[1] = line[1][0].replace(")","").replace("\n","").replace(" ","").split(",")
                line[1] = [int(i) for i in line[1]]
                for i in integer_vals:
                    line.append(int(i))
                
                update_table_data(table_name, line)

        
        

def update_table_data(table_name,line):
    values_string = '(' + ','.join(['%s' for i in line]) + ')'
    cur.execute(sql.SQL("INSERT INTO {} VALUES" + values_string).format(sql.Identifier('{}'.format(table_name))),line)
    
def delete_existing_table(table_name):
    cur.execute(sql.SQL('DELETE FROM {}').format(sql.Identifier('{}'.format(table_name))))

def check_table_data(table_name):
    cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('{}'.format(table_name))))
    print(cur.fetchall())

def update_local_db(table,file):
    delete_existing_table(table)
    load_table_data(file,table)
    check_table_data(table)

update_local_db('employees','schedule/dbTableBackups/employees.sql')
update_local_db('availability','schedule/dbTableBackups/availability.sql')
update_local_db('extremes','schedule/dbTableBackups/extremes.sql')
update_local_db('required_skills_for_shift','schedule/dbTableBackups/required_skills_for_shift.sql')
update_local_db('business_info','schedule/dbTableBackups/business_info.sql')
update_local_db('skills','schedule/dbTableBackups/skills.sql')
update_local_db('shifts','Schedule/dbTableBackups/shifts.sql')


