from flask import Flask, request, jsonify, render_template
import clingoSchedule
import psycopg2
from psycopg2 import sql


app = Flask(__name__)
zero_val_array = '{0,0,0,0,0,0,0,0,0,0,0,0,0,0}'

skill_to_edit = ''

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


def add_default_emp_skill_level(skill,emp):     
    execute_SQL(sql.SQL("INSERT INTO {} VALUES(%s,%s,%s)").format(sql.Identifier('skills')),execute_args = [skill,emp,0])
    return None

@app.route('/addEmployee',methods = ["POST"])
def add_employee():
    emp_info = list(request.get_json().values())

    avail_info = emp_info[11:]
    avail_info = [int(i) for i in avail_info]
    execute_SQL(sql.SQL("INSERT INTO {}(id, first_name, last_name, role, wage) VALUES (%s, %s, %s, %s, %s)").format(sql.Identifier('employees')),execute_args = emp_info[0:5])
    id = emp_info[0]
    
    execute_SQL(sql.SQL("INSERT INTO {} VALUES(%s, %s)").format(sql.Identifier('availability')),execute_args = [id,avail_info]) 
    execute_SQL(sql.SQL("INSERT INTO {} VALUES(%s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier('extremes')),execute_args = [id,*emp_info[5:11]])
    skill_names = execute_SQL(sql.SQL("SELECT skill FROM {}").format(sql.Identifier('required_skills_for_shift')))
    
    #Could possibly be achieved with a temporary single row single column table for id, LEFT JOIN(SELECT skill FROM required_skills_for_shift,id_table)
    for name in skill_names:
        execute_SQL(sql.SQL("INSERT INTO {} VALUES(%s,%s,%s)").format(sql.Identifier('skills')),execute_args = [name,id,0])
    
    return jsonify('Employee added successfully')

@app.route('/editExistingEmployee', methods = ["GET"])
def edit_existing_emp_home():
    return render_template('editEmployee.html')

@app.route('/loadEmployeeInfo',methods=["GET"])
def load_employee_info():
    employee = request.args.get('employee')
    
    query_response = execute_SQL(sql.SQL("SELECT * FROM {} JOIN {} USING (id) JOIN {} USING (id) WHERE id = %s").format(sql.Identifier('employees'),sql.Identifier('extremes'),sql.Identifier('availability')),execute_args = [employee])
    
    return jsonify(query_response)

@app.route('/loadEmployeeListData',methods = ["GET"])
def load_employee_names():
    
    query_response = execute_SQL(sql.SQL("SELECT first_name, last_name, id, role FROM {}").format(sql.Identifier('employees')))
    return_array = [{"firstName":emp[0], "lastName":emp[1], "id":emp[2], "role":emp[3]} for emp in query_response]

    return jsonify(return_array)


@app.route('/selectEmpToEdit', methods = ["GET"])
def select_emp_to_edit():
    employee_id = request.args.get('employee')
    return render_template('editSelectedEmployee.html',employee = str(employee_id))

@app.route('/updateEmployee',methods = ["POST"])
def update_employee():
    
     
    request_data = list(request.get_json().values())
    
    emp_id = request_data[0]
    employee_table_data = request_data[1:5]
    extremes_table_data = request_data[5:11]
    avail_info = request_data[11:]
    avail_info = [int(i) for i in avail_info]
    
    execute_SQL(sql.SQL("UPDATE {} SET(first_name, last_name, role, wage) = (%s, %s, %s, %s) WHERE id = %s").format(sql.Identifier('employees')),
                   [*employee_table_data,emp_id])
    execute_SQL(sql.SQL("UPDATE {} SET(min_shift,max_shift,min_weekly,max_weekly,min_days,max_days) = (%s, %s, %s, %s, %s, %s) WHERE id = %s").format(sql.Identifier('extremes')),execute_args = [*extremes_table_data,emp_id])
    execute_SQL(sql.SQL("UPDATE {} SET shift_pref = %s WHERE id = %s").format(sql.Identifier('availability')),execute_args = [avail_info,emp_id])

    return jsonify("Updated Employee Information Saved Successfully.")

@app.route('/deleteEmployee',methods = ["POST"])
def delete_employee():     
    emp_id = request.get_json()
    execute_SQL(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier('employees')),execute_args = [emp_id])
    execute_SQL(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier('extremes')),execute_args = [emp_id])
    execute_SQL(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier('availability')),execute_args = [emp_id])
    execute_SQL(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier('skills')),execute_args = [emp_id])

    return jsonify("Employee Deleted.")

@app.route('/deleteSkill',methods=["POST"])
def delete_skill():
    skill_name = request.get_json()
    execute_SQL(sql.SQL("DELETE FROM {} WHERE skill = %s").format(sql.Identifier('required_skills_for_shift')),execute_args = [skill_name])
    execute_SQL(sql.SQL("DELETE FROM {} WHERE skill = %s").format(sql.Identifier('skills')),execute_args = [skill_name])

    return jsonify("Skill Deleted.")

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

@app.route('/getSchedule',methods= ["GET"])
def get_schedule():
    with open('Schedule/scheduleFile.txt','r') as file0:
        solution = file0.read()
        solution = solution.replace(':',',')
        solution = solution.split(';')
        

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
    
    info = execute_SQL(sql.SQL("SELECT * FROM employees WHERE id = %s"),execute_args = [emp_id])[0]
    
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

    
     
    update_Bool = execute_SQL(sql.SQL("SELECT * FROM {}").format(sql.Identifier('business_info')))
    if update_Bool:
        execute_SQL(sql.SQL("UPDATE {} SET (business_name,min_employees,min_managers,exempt_role,max_total_hours,max_hours_importance,hours_of_op) = (%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier('business_info')),execute_args = [business_name,*business_info_ints[:5],hours_of_op])
    else:
        execute_SQL(sql.SQL("INSERT INTO {} VALUES(%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier('business_info')),execute_args = [business_name,hours_of_op,*business_info_ints[:5]])
    
    
    return jsonify("Added Successfully")

@app.route('/loadBusinessInfo',methods = ["GET"])
def load_business_info():
    business_info = execute_SQL(sql.SQL("SELECT * FROM {}").format(sql.Identifier('business_info')))
    return jsonify(business_info)

@app.route('/loadSkillLevels',methods = ["GET"])
def load_skill_levels():
    employee = request.args.get('employee')
    query_response = execute_SQL(sql.SQL("SELECT skill,skill_level FROM {} WHERE id = %s").format(sql.Identifier('skills')),execute_args = [employee])
    return jsonify(query_response)

@app.route('/updateSkillLevel',methods = ["POST"])
def update_skill_level():
    request_data = request.get_json()
    skill = request_data['skill']
    skill_level = request_data['skill_level']
    id = request_data['id']

    execute_SQL(sql.SQL("UPDATE {} SET skill_level = %s WHERE id = %s AND skill = %s").format(sql.Identifier('skills')),execute_args = [skill_level,id,skill])
    return jsonify("Skill level updated successfully.")

@app.route('/loadSkillInfo',methods = ["GET"])
def load_skill_info():
    return load_selected_item_details(request.args.get('skill'),"required_skills_for_shift",'skill')

@app.route('/loadShiftInfo', methods = ["GET"])
def load_shift_info():
    return load_selected_item_details(request.args.get('shift'),"shifts","shiftname")

def load_selected_item_details(selected_item,table,name_column):
    item_info = execute_SQL(sql.SQL("SELECT * FROM {} WHERE {} = %s").format(sql.Identifier(table),sql.Identifier(name_column)),execute_args = [selected_item])
    return jsonify(item_info)



@app.route('/editSelectedSkillPage', methods = ["GET"])
def edit_selected_skill_home():
    return render_template('editSelectedSkill.html')

@app.route('/editSkills', methods = ["GET"])
def edit_skills_home():
    return render_template('editSkills.html')

@app.route('/loadRequiredSkills', methods = ["GET"])
def load_required_skills():
    return load_drop_down_info(["skill","importance","role"],"required_skills_for_shift")

@app.route('/loadShifts', methods = ["GET"])
def load_shifts():
    return load_drop_down_info(["shiftname","importance","maxhours"],"shifts")

def load_drop_down_info(columns_to_select,table):
    query_response = execute_SQL(sql.SQL("SELECT {},{},{} FROM {}").format(sql.Identifier(columns_to_select[0]),sql.Identifier(columns_to_select[1]),sql.Identifier(columns_to_select[2]),sql.Identifier(table)))        

    return_array = [{"name":x[0], "importance":x[1], columns_to_select[2]:x[2]} for x in query_response]
    return jsonify(return_array)

@app.route('/updateSkill',methods = ["POST"])
def update_skill():
    return use_info(request.get_json(),which_function="update",table="required_skills_for_shift")

@app.route('/addSkill', methods = ["POST"])
def add_skill():
    status, skill = use_info(request.get_json(),which_function="insert",table="required_skills_for_shift")
    if status == "Skill Added Successfully":
        emp_ids = execute_SQL(sql.SQL("SELECT id FROM {}").format(sql.Identifier('employees')))
        for id in emp_ids:
            add_default_emp_skill_level(skill,id)
    return jsonify("Operation successful")

def use_info(info,which_function = None,table = None):
    if table == "required_skills_for_shift":
        time_vals = list(info.values())[3:]
        time_vals = [int(i) for i in time_vals]
        
        name = info['skillName']
        info3 = info['role']
        importance = info['importance']
        role_or_max_hrs = 'role'
        name_column = "skill"
        return_statement = jsonify("Skill Operation Successful"),name
    elif table == "shifts":
        time_vals = list(info.values())[3:]
        time_vals = [int(i) for i in time_vals]
        
        name = info['shiftName']
        info3 = info['maxHours']
        importance = info['importance']
        role_or_max_hrs = "maxhours"
        name_column = "shiftname"
        return_statement = jsonify("Shift Operation Successful")
    else:
        return jsonify("Operation failed")

    try:
        if which_function == "insert":
            execute_SQL(sql.SQL("INSERT INTO {} VALUES(%s,%s,%s,%s)").format(sql.Identifier(table)),execute_args = [name, time_vals, importance, info3])
        elif which_function == "update":
            execute_SQL(sql.SQL("UPDATE {} SET (schedule_blocks,importance,{}) = (%s,%s,%s) WHERE {} = %s").format(sql.Identifier(table),sql.Identifier(role_or_max_hrs),sql.Identifier(name_column)),execute_args = [time_vals,importance,info3,name])
            return jsonify("Update Successful")
    except:
        return jsonify("Operation failed")

    return return_statement

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

