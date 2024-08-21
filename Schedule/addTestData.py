import psycopg2
from psycopg2 import sql
conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')
cur = conn.cursor()
zero_val_array = '{0,0,0,0,0,0,0,0,0,0,0,0,0,0}'
# cur.execute("DROP TABLE employees")
# cur.execute("CREATE TABLE employees(id int, first_name varchar(255), last_name varchar(255), role int, wage int)")
# cur.execute("DROP TABLE availability")
# cur.execute(sql.SQL("CREATE TABLE availability(id int, shift_pref integer ARRAY[28] DEFAULT %s)"),[zero_val_array])
# cur.execute("SELECT * FROM employees")
# print(cur.fetchall())
# # cur.execute("insert into availability Values(30,zero_val_array)")
# # cur.execute(sql.SQL("UPDATE availability SET shift_pref[%s:%s] = %s WHERE id = %s"),['1','168',zero_val_array,'30'])
# # cur.execute("select * from availability")
# print(cur.fetchall())
# cur.execute("DROP TABLE skills")
# cur.execute("CREATE TABLE skills(skill varchar(255), id int, skill_level int)")
# cur.execute("DROP TABLE required_skills_for_shift")
# cur.execute("CREATE TABLE required_skills_for_shift(skill varchar(255), schedule_blocks integer ARRAY[14], importance int, role int)")
# cur.execute("DROP TABLE hours_extremes")
# cur.execute("DROP TABLE extremes")
# cur.execute("CREATE TABLE extremes(id int, min_shift int DEFAULT 0, max_shift int DEFAULT 24, min_weekly int DEFAULT 0, max_weekly int DEFAULT 120, min_days int DEFAULT 0, max_days int DEFAULT 7)")
# cur.execute("SELECT * FROM employees")
# print(cur.fetchall())
# cur.execute("SELECT * FROM extremes")
# print(cur.fetchall())

# cur.execute("INSERT INTO variables VALUES('skill_to_edit', 'none')")
# cur.execute("ALTER TABLE employees ADD CONSTRAINT emp_id PRIMARY KEY (id)")
# cur.execute("ALTER TABLE availability ADD CONSTRAINT avail_id PRIMARY KEY (id)")
# cur.execute("ALTER TABLE extremes ADD CONSTRAINT extremes_id PRIMARY KEY (id)")
# cur.execute("DELETE FROM skills WHERE id = 5")

# cur.execute("ALTER TABLE skills ADD CONSTRAINT skill_lvls_primary PRIMARY KEY (skill, id)")
# cur.execute("INSERT INTO skills VALUES ('Sign Audit', 1, 1)")
# cur.execute("INSERT INTO skills VALUES ('Count Drawers', 1, 0)")
# cur.execute("CREATE TABLE business_info(business_name varchar(255), hours_of_op integer ARRAY[28], min_employees int, min_managers int, exempt_role int,max_total_hours int, max_hours_importance int)")
# cur.execute("DROP TABLE shifts")
# cur.execute("CREATE TABLE shifts(shiftName varchar(255), schedule_blocks integer ARRAY[14], importance int, maxHours int)")
# cur.execute("CREATE TABLE saved_schedule()")
# cur.execute("DROP TABLE admin_users")
cur.execute("CREATE TABLE admin_users(user_id SERIAL,email varchar(255) PRIMARY KEY,salt int ,salted_password varchar(255), organization varchar(255) UNIQUE)")


# cur.execute("ALTER TABLE availability RENAME to test_availability")
# cur.execute("ALTER TABLE business_info RENAME to test_business_info")
# cur.execute("ALTER TABLE extremes RENAME to test_extremes")
# cur.execute("ALTER TABLE required_skills_for_shift RENAME to test_required_skills_for_shift")
# cur.execute("ALTER TABLE shifts RENAME to test_shifts")
# cur.execute("ALTER TABLE skills RENAME to test_skills")


# cur.execute("DROP TABLE July25Test3_schedule_29_2024")
# cur.execute(sql.SQL("CREATE TABLE {}(id int PRIMARY KEY,first_name varchar(255), last_name varchar(255),sunday varchar(255), monday varchar(255), tuesday varchar(255), wednesday varchar(255), thursday varchar(255), friday varchar(255), saturday varchar(255),total_hours varchar(64),week_ending_date varchar(255))").format(sql.Identifier("{}".format('July25Test3_schedule_29_2024'))))
# cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('{}'.format("July25Test3_schedule_29_2024"))))
# print(cur.fetchall())
# cur.execute("""SELECT CURRVAL(PG_GET_SERIAL_SEQUENCE('"test_08/24/2024"', 'id')) AS "Current Value", MAX("id") AS "Max Value" FROM "test_08/24/2024";""")
# cur.execute("""SELECT SETVAL((SELECT PG_GET_SERIAL_SEQUENCE('"test_08/24/2024"','id')), (SELECT (MAX("id") + 1) FROM "test_08/24/2024"),FALSE)""")
# print(cur.fetchall())
# cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier("")))




# table_to_drop = 'admin_users_user_id_seq'

# cur.execute("""SELECT CURRVAL(PG_GET_SERIAL_SEQUENCE('"test_08/24/2024"', 'id')) AS "Current Value", MAX("id") AS "Max Value" FROM "test_08/24/2024";""")
# cur.execute("""SELECT CURRVAL(PG_GET_SERIAL_SEQUENCE('"admin_users"', 'user_id')) AS "Current Value", MAX("user_id") AS "Max Value" FROM "admin_users";""")
# print(cur.fetchall())
# Test Commit 1
conn.commit()
cur.close()
conn.close()
