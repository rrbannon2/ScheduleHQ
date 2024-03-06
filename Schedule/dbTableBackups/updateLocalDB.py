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
        elif table_name == 'business_info' or table_name == 'required_skills_for_shift':
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

delete_existing_table('employees')
load_table_data('schedule/dbTableBackups/employees.sql','employees')
check_table_data('employees')

delete_existing_table('availability')
load_table_data('schedule/dbTableBackups/availability.sql','availability')
check_table_data('availability')

delete_existing_table('extremes')
load_table_data('schedule/dbTableBackups/extremes.sql','extremes')
check_table_data('extremes')

delete_existing_table('required_skills_for_shift')
load_table_data('schedule/dbTableBackups/required_skills_for_shift.sql','required_skills_for_shift')
check_table_data('required_skills_for_shift')

delete_existing_table('business_info')
load_table_data('schedule/dbTableBackups/business_info.sql','business_info')
check_table_data('business_info')

delete_existing_table('skills')
load_table_data('schedule/dbTableBackups/skills.sql','skills')
check_table_data('skills')
