import psycopg2
from psycopg2 import sql
conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')
cur = conn.cursor()
zero_val_array = '{0,0,0,0,0,0,0,0,0,0,0,0,0,0}'

# cur.execute("CREATE TABLE employees(id int, first_name varchar(255), last_name varchar(255), role int, wage int)")
# cur.execute(sql.SQL("CREATE TABLE availability(id int, shift_pref integer ARRAY[28] DEFAULT %s)"),[zero_val_array])
# cur.execute("CREATE TABLE skills(skill varchar(255), id int, skill_level int)")
# cur.execute("CREATE TABLE required_skills_for_shift(skill varchar(255), schedule_blocks integer ARRAY[14], importance int, role int)")
# cur.execute("CREATE TABLE extremes(id int, min_shift int DEFAULT 0, max_shift int DEFAULT 24, min_weekly int DEFAULT 0, max_weekly int DEFAULT 120, min_days int DEFAULT 0, max_days int DEFAULT 7)")
# cur.execute("ALTER TABLE employees ADD CONSTRAINT emp_id PRIMARY KEY (id)")
# cur.execute("ALTER TABLE availability ADD CONSTRAINT avail_id PRIMARY KEY (id)")
# cur.execute("ALTER TABLE extremes ADD CONSTRAINT extremes_id PRIMARY KEY (id)")
# cur.execute("ALTER TABLE skills ADD CONSTRAINT skill_lvls_primary PRIMARY KEY (skill, id)")
# cur.execute("CREATE TABLE business_info(business_name varchar(255), hours_of_op integer ARRAY[28], min_employees int, min_managers int, exempt_role int,max_total_hours int, max_hours_importance int)")
# cur.execute("CREATE TABLE shifts(shiftName varchar(255), schedule_blocks integer ARRAY[14], importance int, maxHours int)")

cur.execute("CREATE TABLE employees2(id int, first_name varchar(255), last_name varchar(255), role int, wage int)")
cur.execute(sql.SQL("CREATE TABLE availability2(id int, shift_pref integer ARRAY[28] DEFAULT %s)"),[zero_val_array])
cur.execute("CREATE TABLE skills2(skill varchar(255), id int, skill_level int)")
cur.execute("CREATE TABLE required_skills_for_shift2(skill varchar(255), schedule_blocks integer ARRAY[14], importance int, role int)")
cur.execute("CREATE TABLE extremes2(id int, min_shift int DEFAULT 0, max_shift int DEFAULT 24, min_weekly int DEFAULT 0, max_weekly int DEFAULT 120, min_days int DEFAULT 0, max_days int DEFAULT 7)")
cur.execute("ALTER TABLE employees2 ADD CONSTRAINT emp_id PRIMARY KEY (id)")
cur.execute("ALTER TABLE availability2 ADD CONSTRAINT avail_id PRIMARY KEY (id)")
cur.execute("ALTER TABLE extremes2 ADD CONSTRAINT extremes_id PRIMARY KEY (id)")
cur.execute("ALTER TABLE skills2 ADD CONSTRAINT skill_lvls_primary PRIMARY KEY (skill, id)")
cur.execute("CREATE TABLE business_info2(business_name varchar(255), hours_of_op integer ARRAY[28], min_employees int, min_managers int, exempt_role int,max_total_hours int, max_hours_importance int)")
cur.execute("CREATE TABLE shifts2(shiftName varchar(255), schedule_blocks integer ARRAY[14], importance int, maxHours int)")

def get_db_connection():
    conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')
    return conn

def execute_SQL(sql_statement,execute_args=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    if execute_args:
        cursor.execute(sql_statement,execute_args)
    else:
        cursor.execute(sql_statement)
    try:
        fetched = cursor.fetchall()
    except:
        fetched = "Failed to fetch data"

    conn.commit()
    cursor.close()
    conn.close()
    return fetched

def add_employee(emp_info):
    id = emp_info[0]
    avail_info = emp_info[11:]
    execute_SQL(sql.SQL("INSERT INTO {}(id, first_name, last_name, role, wage) VALUES (%s, %s, %s, %s, %s)").format(sql.Identifier('employees2')),execute_args = emp_info[0:5])
    execute_SQL(sql.SQL("INSERT INTO {} VALUES(%s, %s)").format(sql.Identifier('availability2')),execute_args = [id,avail_info]) 
    execute_SQL(sql.SQL("INSERT INTO {} VALUES(%s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier('extremes2')),execute_args = [id,*emp_info[5:11]])

add_employee()