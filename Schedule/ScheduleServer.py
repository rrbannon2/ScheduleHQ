from flask import Flask, request, jsonify, render_template
import clingoSchedule
import psycopg2
from psycopg2 import sql
import csv

app = Flask(__name__)
zero_val_array = '{0,0,0,0,0,0,0,0,0,0,0,0,0,0}'

skill_to_edit = ''

def get_db_connection():
    conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')
    return conn

@app.route('/add_employee',methods = ["POST"])
def add_employee():
    emp_info = list(request.get_json().values())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    avail_info = emp_info[11:]
    avail_info = [int(i) for i in avail_info]
    cursor.execute(sql.SQL("INSERT INTO {}(id, first_name, last_name, role, wage) VALUES (%s, %s, %s, %s, %s)").format(sql.Identifier('employees')),emp_info[0:5])
    id = emp_info[0]
    
    cursor.execute(sql.SQL("INSERT INTO {} VALUES(%s, %s)").format(sql.Identifier('availability')),[id,avail_info]) 
    cursor.execute(sql.SQL("INSERT INTO {} VALUES(%s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier('extremes')),[id,*emp_info[5:11]])
    cursor.execute(sql.SQL("SELECT skill FROM {}").format(sql.Identifier('required_skills_for_shift')))
    skill_names = cursor.fetchall()
    #Could possibly be achieved with a temporary single row single column table for id, LEFT JOIN(SELECT skill FROM required_skills_for_shift,id_table)
    for name in skill_names:
        cursor.execute(sql.SQL("INSERT INTO {} VALUES(%s,%s,%s)").format(sql.Identifier('skills')),[name,id,0])
    
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify('Employee added successfully')

@app.route('/editExistingEmployee', methods = ["GET"])
def edit_existing_emp_home():
    return render_template('editEmployee.html')

@app.route('/loadEmployeeInfo',methods=["GET"])
def load_employee_info():
    employee = request.args.get('employee')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT * FROM {} JOIN {} USING (id) JOIN {} USING (id) WHERE id = %s").format(sql.Identifier('employees'),
                                                        sql.Identifier('extremes'),sql.Identifier('availability')),[employee])
    query_response = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(query_response)

@app.route('/loadEmployeeNames',methods = ["GET"])
def load_employee_names():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(sql.SQL("SELECT first_name, last_name, id FROM {}").format(sql.Identifier('employees')))
    return jsonify(cursor.fetchall())

@app.route('/selectEmpToEdit', methods = ["GET"])
def select_emp_to_edit():
    employee_id = request.args.get('employee')
    return render_template('editSelectedEmployee.html',employee = str(employee_id))

@app.route('/updateEmployee',methods = ["POST"])
def update_employee():
    conn = get_db_connection()
    cursor = conn.cursor()
    request_data = list(request.get_json().values())
    
    emp_id = request_data[0]
    employee_table_data = request_data[1:5]
    extremes_table_data = request_data[5:11]
    avail_info = request_data[11:]
    avail_info = [int(i) for i in avail_info]
    
    cursor.execute(sql.SQL("UPDATE {} SET(first_name, last_name, role, wage) = (%s, %s, %s, %s) WHERE id = %s").format(sql.Identifier('employees')),
                   [*employee_table_data,emp_id])
    cursor.execute(sql.SQL("UPDATE {} SET(min_shift,max_shift,min_weekly,max_weekly,min_days,max_days) = (%s, %s, %s, %s, %s, %s) WHERE id = %s").format(sql.Identifier('extremes')),[*extremes_table_data,emp_id])
    cursor.execute(sql.SQL("UPDATE {} SET shift_pref = %s WHERE id = %s").format(sql.Identifier('availability')),[avail_info,emp_id])

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify("Updated Employee Information Saved Successfully.")

@app.route('/deleteEmployee',methods = ["POST"])
def delete_employee():
    conn = get_db_connection()
    cursor = conn.cursor()
    emp_id = request.get_json()
    cursor.execute(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier('employees')),[emp_id])
    cursor.execute(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier('extremes')),[emp_id])
    cursor.execute(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier('availability')),[emp_id])
    cursor.execute(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier('skills')),[emp_id])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify("Employee Deleted.")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/writeSchedule', methods = ["GET"])
def write():
    clingoSchedule.run_clingo(3)
    with open('Schedule/scheduleFile.txt', 'r') as file0:
        solution = file0.read()
        solution = solution.split(',')

    return jsonify(solution)

@app.route('/addEmployeePage',methods = ["GET"])
def add_emp_home():
    return render_template('addEmployee.html')
    
@app.route('/addSkillsPage', methods = ["GET"])
def add_skills_home():
    return render_template('addSkills.html')

@app.route('/businessInfoPage',methods = ["GET"])
def business_info_home():
    return render_template('businessInfo.html')

@app.route('/addShiftPage', methods = ["GET"])
def add_shift_home():
    return render_template('addShift.html')

@app.route('/editShiftPage', methods = ["GET"])
def edit_shift_home():
    return render_template('editShift.html')

@app.route('/employeeSkillsPage', methods = ["GET"])
def edit_employee_skills():
    emp_id = request.args.get('employee')
    # first_name = request.args.get('firstName')
    # last_name = request.args.get('lastName')
    # role = request.args.get('role')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT * FROM employees WHERE id = %s"),[emp_id])
    info = cursor.fetchall()[0]

    first_name = info[1]
    last_name = info[2]
    role = info[3]
    return render_template('employeeSkills.html',employee = emp_id, firstName = first_name, lastName = last_name, role0 = role)

@app.route('/selectSkillToEdit', methods = ["GET"])
def select_skill_to_edit():
    skill_name = request.args.get('skill')
    
    return render_template('editSelectedSkill.html',skill = str(skill_name))

@app.route('/generateSchedulePage',methods=["GET"])
def generate_schedule_home():
    return render_template('generateSchedule.html')

@app.route('/updateBusinessInfo',methods = ["POST"])
def update_business_info():
    business_info = list(request.get_json().values())
    business_name = business_info[0]
    business_info_ints = [int(i) for i in business_info[1:]]
    hours_of_op = business_info_ints[5:]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('business_info')))
    if cursor.fetchall():
        cursor.execute(sql.SQL("UPDATE {} SET (business_name,min_employees,min_managers,exempt_role,max_total_hours,max_hours_importance,hours_of_op) = (%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier('business_info')),[business_name,*business_info_ints[:5],hours_of_op])
    else:
        cursor.execute(sql.SQL("INSERT INTO {} VALUES(%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier('business_info')),[business_name,hours_of_op,*business_info_ints[:5]])
    cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('business_info')))
    conn.commit()
    return jsonify("Added Successfully")

@app.route('/loadBusinessInfo',methods = ["GET"])
def load_business_info():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('business_info')))
    business_info = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify(business_info)

@app.route('/loadSkillLevels',methods = ["GET"])
def load_skill_levels():
    employee = request.args.get('employee')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT skill,skill_level FROM {} WHERE id = %s").format(sql.Identifier('skills')),[employee])
    query_response = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(query_response)

@app.route('/updateSkillLevel',methods = ["POST"])
def update_skill_level():
    request_data = request.get_json()
    skill = request_data['skill']
    skill_level = request_data['skill_level']
    id = request_data['id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql.SQL("UPDATE {} SET skill_level = %s WHERE id = %s AND skill = %s").format(sql.Identifier('skills')),[skill_level,id,skill])
    conn.commit()
    return jsonify("Skill level updated successfully.")

@app.route('/loadSkillInfo',methods = ["GET"])
def load_skill_info():
    return load_selected_item_details(request.args.get('skill'),"required_skills_for_shift",'skill')

@app.route('/loadShiftInfo', methods = ["GET"])
def load_shift_info():
    return load_selected_item_details(request.args.get('shift'),"shifts","shiftname")

def load_selected_item_details(selected_item,table,name_column):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT * FROM {} WHERE {} = %s").format(sql.Identifier(table),sql.Identifier(name_column)),[selected_item])
    item_info = cursor.fetchall()
    return jsonify(item_info)



@app.route('/editSelectedSkillPage', methods = ["GET"])
def edit_selected_skill_home():
    return render_template('editSelectedSkill.html')

@app.route('/editSkills', methods = ["GET"])
def edit_skills_home():
    return render_template('editSkills.html')

@app.route('/loadSkills', methods = ["GET"])
def load_skills():
    return load_drop_down_info("skill","required_skills_for_shift")

@app.route('/loadShifts', methods = ["GET"])
def load_shifts():
    return load_drop_down_info("shiftname","shifts")

def load_drop_down_info(column_to_select,table):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(sql.SQL("SELECT {} FROM {}").format(sql.Identifier(column_to_select),sql.Identifier(table)))
    drop_down_data = cursor.fetchall()
        
    cursor.close()
    conn.close()
    return jsonify(drop_down_data)

@app.route('/updateSkill',methods = ["POST"])
def update_skill():
    return use_info(request.get_json(),which_function="update",table="required_skills_for_shift")

@app.route('/addSkill', methods = ["POST"])
def add_skill():
    return use_info(request.get_json(),which_function="insert",table="required_skills_for_shift")

def use_info(info,which_function = None,table = None):
    if table == "required_skills_for_shift":
        conn = get_db_connection()
        cursor = conn.cursor()

        time_vals = list(info.values())[3:]
        time_vals = [int(i) for i in time_vals]
        
        name = info['skillName']
        info3 = info['role']
        importance = info['importance']
        role_or_max_hrs = 'role'
        name_column = "skill"
    elif table == "shifts":
        conn = get_db_connection()
        cursor = conn.cursor()

        time_vals = list(info.values())[3:]
        time_vals = [int(i) for i in time_vals]
        
        name = info['shiftName']
        info3 = info['maxHours']
        importance = info['importance']
        role_or_max_hrs = "maxhours"
        name_column = "shiftname"
    else:
        return jsonify("Operation failed")

    if which_function == "insert":
        cursor.execute(sql.SQL("INSERT INTO {} VALUES(%s,%s,%s,%s)").format(sql.Identifier(table)),[name, time_vals, importance, info3])
    elif which_function == "update":
        cursor.execute(sql.SQL("UPDATE {} SET (schedule_blocks,importance,{}) = (%s,%s,%s) WHERE {} = %s").format(sql.Identifier(table),sql.Identifier(role_or_max_hrs),sql.Identifier(name_column)),[time_vals,importance,info3,name])

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify("Operation successful")

@app.route('/addShift',methods = ["POST"])
def add_shift():
    return use_info(request.get_json(),which_function="insert",table="shifts")

@app.route('/updateShift',methods = ["POST"])
def update_shift():
    return use_info(request.get_json(),which_function="update",table="shifts")

@app.route('/selectShiftToEdit',methods = ["GET"])
def select_shift_to_edit():
    shift_name = request.args.get('shift')
    return render_template('editSelectedShift.html',shift = str(shift_name))

if __name__ == '__main__':
    app.run(debug=True) 

