import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')
cur = conn.cursor()



def load_table_data(table_file_name,table_name):
    with open(table_file_name,'r') as table_file:
        if 'employees' in table_name or 'extremes' in table_name or 'skills' in table_name :
            for line in table_file.readlines():
                line = line.replace("'","").replace('(','').replace(')','').replace('\n','').split(", ")
                update_table_data(table_name, line)
        elif 'availability' in table_name:
            for line in table_file.readlines():
                line = line.split('[')
                line[0] = line[0].replace("(","").replace(", ","").replace("'","")
                line[1] = line[1].replace("])","").replace("\n","").replace(" ","").split(",")
                line[1] = [int(i) for i in line[1]]
                update_table_data(table_name, line)
        elif 'business_info' in table_name or 'required_skills_for_shift' in table_name or 'shifts' in table_name:
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
        # elif 'schedule' in table_name:
        #     for line in table_file.readlines():
        #         line = line
        else:
            print("table name doesn't match any known tables")

        
        

def update_table_data(table_name,line):
    values_string = '(' + ','.join(['%s' for i in line]) + ')'
    cur.execute(sql.SQL("INSERT INTO {} VALUES" + values_string).format(sql.Identifier('{}'.format(table_name))),line)
    
def delete_existing_table(table_name):
    try:
        cur.execute(sql.SQL('DELETE FROM {}').format(sql.Identifier('{}'.format(table_name))))
    except:
        print("{} table does not exist, could not be deleted.")
def check_table_data(table_name):
    cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('{}'.format(table_name))))
    print(cur.fetchall())

def update_local_db(table,file):
    delete_existing_table(table)
    load_table_data(file,table)
    check_table_data(table)
    conn.commit()


update_local_db('test_employees','Schedule/dbTableBackups/test_employees.sql')
update_local_db('test_availability','Schedule/dbTableBackups/test_availability.sql')
update_local_db('test_extremes','Schedule/dbTableBackups/test_extremes.sql')
update_local_db('test_required_skills_for_shift','Schedule/dbTableBackups/test_required_skills_for_shift.sql')
update_local_db('test_business_info','Schedule/dbTableBackups/test_business_info.sql')
update_local_db('test_skills','Schedule/dbTableBackups/test_skills.sql')
update_local_db('test_shifts','Schedule/dbTableBackups/test_shifts.sql')
# update_local_db('test_schedule_29_2024','Schedule/dbTableBackups/test_schedule_29_2024.sql')


