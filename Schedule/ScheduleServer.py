from flask import Flask, request, jsonify, render_template, session
import clingoSchedule
import psycopg2
from psycopg2 import sql
import flask_login as fl_lgin
import secrets
import hashlib
from userClass import User
from flask_jwt import JWT, jwt_required, current_identity


app = Flask(__name__)
zero_val_array = '{0,0,0,0,0,0,0,0,0,0,0,0,0,0}'

app.config['SECRET_KEY'] = secrets.token_hex()

# app.config['SECRET_KEY'] = 'super-secret'
tokens_dict = {}

def get_db_connection():
    conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')
    return conn

def execute_SQL(sql_statement,identifiers = False,execute_args=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    if identifiers:
        for i in identifiers:
            if type(i) != sql.Identifier:
                print("SQL request contains invalid values in identifiers")
                return "SQL request contains invalid values in identifiers"
        sql_statement = sql.SQL(sql_statement).format(*identifiers)
    else:
        sql_statement = sql.SQL(sql_statement)

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

def load_user(user_id):
    print(User.users)
    return User.users[user_id]

@app.route('/addUser',methods = ["POST"])
def add_user():
    user_info = request.get_json()
    user_email = user_info["userEmail"]
    user_password = user_info["password"]
    user_org = user_info["orgName"]
    salt = secrets.randbelow(1000000)
    salted_pass = user_password + str(salt)
    salted_pass = salted_pass.encode('utf-8')
    hashed_pass = str(hashlib.sha512(salted_pass).hexdigest()) #TODO: THIS IS TEMPORARY, NOT HOW PASSWORDS WILL BE HASHED AND STORED. FIX.
    try:
        execute_SQL("INSERT INTO {} (email,salt,salted_password,organization) VALUES(%s,%s,%s,%s)",[sql.Identifier('admin_users')],execute_args = [user_email,salt,hashed_pass,user_org])
    except:
        print("Already an account")
        return jsonify("There is already an account with that email address or organization name.")
    print(execute_SQL("SELECT * FROM {}",[sql.Identifier('admin_users')]))
    # execute_SQL("CREATE TABLE {} (id int, first_name varchar(255), last_name varchar(255), role int, wage int)",[sql.Identifier('{}_employees'.format(user_org))])
    # execute_SQL("CREATE TABLE {} (id int, shift_pref integer ARRAY[28] DEFAULT %s)",[sql.Identifier('{}_availability'.format(user_org))],execute_args=[zero_val_array])
    # execute_SQL("CREATE TABLE {}_
    # execute_SQL("CREATE TABLE {}_
    # execute_SQL("CREATE TABLE {}_
    # execute_SQL("CREATE TABLE {}_
    # execute_SQL("CREATE TABLE {}_
    # execute_SQL("CREATE TABLE {}_
    # execute_SQL("CREATE TABLE {}_
    # execute_SQL("CREATE TABLE {}_
    # execute_SQL("CREATE TABLE {}_
    return jsonify("Sign up successful!")

def authenticate(email,password):
    query_response = execute_SQL("SELECT user_id, salt, salted_password, organization FROM {} WHERE email = %s",[sql.Identifier("admin_users")],execute_args=[email]) 
    user_id, salt, user_password,organization = query_response[0][:4]
    user_id = str(user_id)
    organization = str(organization)
    print(query_response)
    salted_attempt_password = password + str(salt)
    if str(hashlib.sha512(salted_attempt_password.encode('utf-8')).hexdigest()) == user_password:
        User({"user_id" : user_id,"email" : email,"organization":organization})
        return load_user(user_id)
    else:
        return None

def identity(payload):
    user_id = payload['identity']
    return load_user(user_id)

def token_verify(token_val):
    users_dict = User.users
    print(tokens_dict)
    token_val = str(token_val)
    if token_val in tokens_dict:
        user_id = tokens_dict[token_val]
        tokens_dict.pop(token_val,None)
        # print(users_dict[user_id].tokens)
        if token_val in users_dict[user_id].tokens:
            users_dict[user_id].tokens.pop()
            return users_dict[user_id]
    return False

def generate_token(user):
    token = secrets.token_hex()
    user.tokens.insert(0,token)
    tokens_dict.pop(user.tokens[-1],None)
    tokens_dict[token] = user.user_id
    # print(tokens_dict)

    return token


def token_required(request_func):
    # print(request.get_json)
    token = request.args.get("token")
    user = token_verify(token)
    if user:
        body = request_func()
        new_token = generate_token(user)
        return {"token":new_token,"body":body}
    else:
        return {'a':'b'},401
    
# app.config['before_request'] = token_required

@app.route('/login',methods = ["POST"])
def login():
    login_info = request.get_json()
    email = login_info["userEmail"]
    attempt_password = login_info["password"]
    user = authenticate(email,attempt_password)
    if user:
        token = generate_token(user)
        return {"response":"Login Successful","token":token}
    else:
        return {"response": "Email or Password incorrect, please try again.","token":None}

def add_default_emp_skill_level(skill,emp):     
    execute_SQL("INSERT INTO {} VALUES(%s,%s,%s)",[sql.Identifier('skills')],execute_args = [skill,emp,0])
    return None



@app.route('/addEmployee',methods = ["POST"])
def add_employee():
    token = request.args.get("token")
    request_dict = request.get_json()
    # token = request_dict.pop("token",None)
    user = token_verify(token)
    if user:
        emp_info = list(request_dict.values())
        organization = user.get_organization()
        avail_info = emp_info[11:]
        avail_info = [int(i) for i in avail_info]
        execute_SQL("INSERT INTO {}(id, first_name, last_name, role, wage) VALUES (%s, %s, %s, %s, %s)",[sql.Identifier('{}_employees'.format(organization))],execute_args = emp_info[0:5])
        id = emp_info[0]
        
        execute_SQL("INSERT INTO {} VALUES(%s, %s)",[sql.Identifier('availability')],execute_args = [id,avail_info]) 
        execute_SQL("INSERT INTO {} VALUES(%s, %s, %s, %s, %s, %s, %s)",[sql.Identifier('extremes')],execute_args = [id,*emp_info[5:11]])
        skill_names = execute_SQL("SELECT skill FROM {}",[sql.Identifier('required_skills_for_shift')])
        
        #Could possibly be achieved with a temporary single row single column table for id, LEFT JOIN(SELECT skill FROM required_skills_for_shift,id_table)
        for name in skill_names:
            execute_SQL("INSERT INTO {} VALUES(%s,%s,%s)",[sql.Identifier('skills')],execute_args = [name,id,0])
        new_token = generate_token(user)
        return {'body':"Employee Added Successfully",'token':new_token}
    else:
        return {'a':'b'},401

@app.route('/loadEmployeeInfo',methods=["GET"])
# @fl_lgin.login_required
def load_employee_info():
    token = request.args.get("token")
    # request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        employee = request.args.get('employee')
        query_response = execute_SQL("SELECT * FROM {} JOIN {} USING (id) JOIN {} USING (id) WHERE id = %s",(sql.Identifier('{}_employees'.format(organization)),sql.Identifier('extremes'),sql.Identifier('availability')),execute_args = [employee])
        new_token = generate_token(user)
        return {'body':query_response,'token':new_token}
    else:
        return {'a':'b'},401

@app.route('/loadEmployeeListData',methods = ["GET"])
# @fl_lgin.login_required
def load_employee_names():
    token = request.args.get("token")
    # request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        try:
            query_response = execute_SQL("SELECT first_name, last_name, id, role FROM {}",[sql.Identifier('{}_employees'.format(organization))])
        except:
            new_token = generate_token(user)
            return {'body':["No existing employees found"],'token':new_token}
        print(query_response)
        return_array = [{"firstName":emp[0], "lastName":emp[1], "id":emp[2], "role":emp[3]} for emp in query_response]
        new_token = generate_token(user)
        return {'body':return_array,'token':new_token}
    else:
        return {'a':'b'},401


@app.route('/updateEmployee',methods = ["POST"])
# @fl_lgin.fresh_login_required
def update_employee():
    token = request.args.get("token")
    request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        request_data = list(request_dict.values())
        
        emp_id = request_data[0]
        employee_table_data = request_data[1:5]
        extremes_table_data = request_data[5:11]
        avail_info = request_data[11:]
        avail_info = [int(i) for i in avail_info]
        
        execute_SQL("UPDATE {} SET(first_name, last_name, role, wage) = (%s, %s, %s, %s) WHERE id = %s",[sql.Identifier('{}_employees'.format(organization))],
                    [*employee_table_data,emp_id])
        execute_SQL("UPDATE {} SET(min_shift,max_shift,min_weekly,max_weekly,min_days,max_days) = (%s, %s, %s, %s, %s, %s) WHERE id = %s",[sql.Identifier('extremes')],execute_args = [*extremes_table_data,emp_id])
        execute_SQL("UPDATE {} SET shift_pref = %s WHERE id = %s",[sql.Identifier('availability')],execute_args = [avail_info,emp_id])
        new_token = generate_token(user)
        return {'body':"Updated Employee Information Saved Successfully.",'token':new_token}
    else:
        return {'a':'b'},401
        

@app.route('/deleteEmployee',methods = ["POST"])
# @fl_lgin.fresh_login_required
def delete_employee():     
    token = request.args.get("token")
    emp_id = request.get_json()
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        execute_SQL("DELETE FROM {} WHERE id = %s",[sql.Identifier('{}_employees'.format(organization))],execute_args = [emp_id])
        execute_SQL("DELETE FROM {} WHERE id = %s",[sql.Identifier('extremes')],execute_args = [emp_id])
        execute_SQL("DELETE FROM {} WHERE id = %s",[sql.Identifier('availability')],execute_args = [emp_id])
        execute_SQL("DELETE FROM {} WHERE id = %s",[sql.Identifier('skills')],execute_args = [emp_id])
        new_token = generate_token(user)
        return {'body':"Employee Deleted Successfully",'token':new_token}
    else:
        return {'a':'b'},401

@app.route('/deleteSkill',methods=["POST"])
# @fl_lgin.fresh_login_required
def delete_skill():
    skill_name = request.get_json()
    execute_SQL("DELETE FROM {} WHERE skill = %s",[sql.Identifier('required_skills_for_shift')],execute_args = [skill_name])
    execute_SQL("DELETE FROM {} WHERE skill = %s",[sql.Identifier('skills')],execute_args = [skill_name])

    return jsonify("Skill Deleted.")

@app.route('/deleteShift',methods = ["POST"])
# @fl_lgin.fresh_login_required
def delete_shift():
    shift_name = request.get_json()
    execute_SQL("DELETE FROM {} WHERE shiftName = %s",[sql.Identifier('shifts')],execute_args = [shift_name])

    return jsonify("Shift Deleted.")

@app.route('/deleteUser',methods = ["POST"])
# @fl_lgin.fresh_login_required
def delete_user():
    user_name = request.get_json()
    execute_SQL("DELETE FROM {} WHERE email = %s",[sql.Identifier('users')],execute_args = [user_name])

    return jsonify("User Deleted.")

# @app.route('/', methods=['GET'])
# def home():
#     return render_template('index.html')

@app.route('/writeSchedule', methods = ["POST"])
# @fl_lgin.login_required
def write():
    # token = request.args.get("token")
    # user = token_verify(token)
    # if user:
    #     response = request.get_json()
    #     clingoSchedule.run_clingo(response["seconds"],response["date"])
    #     with open('Schedule/scheduleFile.txt', 'r') as file0:
    #         solution = file0.read()
    #         solution = solution.replace('(',',')
    #         solution = solution.split(';')
        # new_token = generate_token(user)
    #     if len(solution) > 0:    
    #         return {'body':"Schedule Written Successfully",'token':new_token}
    #     else:
    #         return {'body':"No schedule generated. Please ensure it is possible to meet the requirements of the business or increase the time limit. Contact Support if issue persists.","token":new_token}
    # else:
    #     return {'a':'b'},401
    response = request.get_json()
    clingoSchedule.run_clingo(response["seconds"],response["date"])
    with open('Schedule/scheduleFile.txt', 'r') as file0:
        solution = file0.read()
        solution = solution.replace('(',',')
        solution = solution.split(';')
    if len(solution) > 0:
        return {'body':"Schedule Written Successfully"}
    else:
        return {'body':"No schedule generated. Please ensure it is possible to meet the requirements of the business or increase the time limit. Contact Support if issue persists."}


@app.route('/getSchedule',methods= ["GET"])
def get_schedule():
    token = request.args.get("token")
    # request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        with open('Schedule/scheduleFile.txt','r') as file0:
            solution = file0.read()
            solution = solution.replace('(',',')
            solution = solution.split(';')
        new_token = generate_token(user)
        return {'body':solution,'token':new_token}
    else:
        return {'a':'b'},401
        

@app.route('/updateBusinessInfo',methods = ["POST"])
# @fl_lgin.fresh_login_required
def update_business_info():
    business_info = list(request.get_json().values())
    business_name = business_info[0]
    business_info_ints = [int(i) for i in business_info[1:]]
    hours_of_op = business_info_ints[5:]

    
     
    update_Bool = execute_SQL("SELECT * FROM {}",[sql.Identifier('business_info')])
    if update_Bool:
        execute_SQL("UPDATE {} SET (business_name,min_employees,min_managers,exempt_role,max_total_hours,max_hours_importance,hours_of_op) = (%s,%s,%s,%s,%s,%s,%s)",[sql.Identifier('business_info')],execute_args = [business_name,*business_info_ints[:5],hours_of_op])
    else:
        execute_SQL("INSERT INTO {} VALUES(%s,%s,%s,%s,%s,%s,%s)",[sql.Identifier('business_info')],execute_args = [business_name,hours_of_op,*business_info_ints[:5]])
    
    
    return jsonify("Added Successfully")

@app.route('/loadBusinessInfo',methods = ["GET"])
# @fl_lgin.login_required
def load_business_info():
    business_info = execute_SQL("SELECT * FROM {}",[sql.Identifier('business_info')])
    return jsonify(business_info)

@app.route('/loadSkillLevels',methods = ["GET"])
# @fl_lgin.login_required
def load_skill_levels():
    employee = request.args.get('employee')
    query_response = execute_SQL("SELECT skill,skill_level FROM {} WHERE id = %s",[sql.Identifier('skills')],execute_args = [employee])
    return jsonify(query_response)

@app.route('/updateSkillLevel',methods = ["POST"])
def update_skill_level():
    token = request.args.get("token")
    request_data = request.get_json()
    # token = request_data["token"]
    user = token_verify(token)
    if user:
        skill = request_data['skill']
        skill_level = request_data['skill_level']
        id = request_data['id']

        execute_SQL("UPDATE {} SET skill_level = %s WHERE id = %s AND skill = %s",[sql.Identifier('skills')],execute_args = [skill_level,id,skill])
        new_token = generate_token(user)
        return {'body':"Skill level updated successfully",'token':new_token}
    else:
        return {'a':'b'},401

@app.route('/loadSkillInfo',methods = ["GET"])
def load_skill_info():
    return load_selected_item_details(request.args.get('skill'),"required_skills_for_shift",'skill')

@app.route('/loadShiftInfo', methods = ["GET"])
def load_shift_info():
    return load_selected_item_details(request.args.get('shift'),"shifts","shiftname")

def load_selected_item_details(selected_item,table,name_column):
    item_info = execute_SQL("SELECT * FROM {} WHERE {} = %s",(sql.Identifier(table),sql.Identifier(name_column)),execute_args = [selected_item])
    return jsonify(item_info)


@app.route('/loadRequiredSkills', methods = ["GET"])
def load_required_skills():
    token = request.args.get("token")
    # request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    
    if user:
        return_array = load_drop_down_info(["skill","importance","role"],"required_skills_for_shift")
        new_token = generate_token(user)
        return {"token":new_token,"returnArray":return_array}
    else:
        return {'a':'b'},401

@app.route('/loadShifts', methods = ["GET"])
def load_shifts():
    token = request.args.get("token")
    # request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        return_array = load_drop_down_info(["shiftname","importance","maxhours"],"shifts")
        new_token = generate_token(user)
        return {"token":new_token,"returnArray":return_array}
    else:
        return {'a':'b'},401

def load_drop_down_info(columns_to_select,table):
    query_response = execute_SQL("SELECT {},{},{} FROM {}",(sql.Identifier(columns_to_select[0]),sql.Identifier(columns_to_select[1]),sql.Identifier(columns_to_select[2]),sql.Identifier(table)))        

    return_array = [{"name":x[0], "importance":x[1], columns_to_select[2]:x[2]} for x in query_response]
    return return_array

@app.route('/updateSkill',methods = ["POST"])
def update_skill():
    token = request.args.get("token")
    request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        return_statement = use_info(request_dict,which_function="update",table="required_skills_for_shift")
        new_token = generate_token(user)
        return {'body':return_statement,'token':new_token}
    else:
        return {'a':'b'},401
    
@app.route('/addSkill', methods = ["POST"])
def add_skill():
    token = request.args.get("token")
    request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        status, skill = use_info(request_dict,which_function="insert",table="required_skills_for_shift")
        if status == "Skill Added Successfully":
            emp_ids = execute_SQL("SELECT id FROM {}",[sql.Identifier('{}_employees'.format(organization))])
            for id in emp_ids:
                add_default_emp_skill_level(skill,id)
            return_statement = "Skill Added Successfully"
        else:
            return_statement = "Skill Not Added"
        new_token = generate_token(user)
        return {'body':return_statement,'token':new_token}
    else:
        return {'a':'b'},401
        

def use_info(info,which_function = None,table = None):
    if table == "required_skills_for_shift":
        time_vals = list(info.values())[3:]
        time_vals = [int(i) for i in time_vals]
        
        name = info['skillName']
        info3 = info['role']
        importance = info['importance']
        role_or_max_hrs = 'role'
        name_column = "skill"
        return_statement = "Skill Operation Successful",name
    elif table == "shifts":
        time_vals = list(info.values())[3:]
        time_vals = [int(i) for i in time_vals]
        
        name = info['shiftName']
        info3 = info['maxHours']
        importance = info['importance']
        role_or_max_hrs = "maxhours"
        name_column = "shiftname"
        return_statement = "Shift Operation Successful"
    else:
        return "Operation failed"

    try:
        if which_function == "insert":
            execute_SQL("INSERT INTO {} VALUES(%s,%s,%s,%s)",[sql.Identifier(table)],execute_args = [name, time_vals, importance, info3])
        elif which_function == "update":
            execute_SQL("UPDATE {} SET (schedule_blocks,importance,{}) = (%s,%s,%s) WHERE {} = %s",(sql.Identifier(table),sql.Identifier(role_or_max_hrs),sql.Identifier(name_column)),execute_args = [time_vals,importance,info3,name])
            return "Update Successful"
    except:
        return "Operation failed"

    return return_statement

@app.route('/addShift',methods = ["POST"])
def add_shift():
    token = request.args.get("token")
    request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        return_statement = use_info(request_dict,which_function="insert",table="shifts")
        new_token = generate_token(user)
        return {'body':return_statement,'token':new_token}
    else:
        return {'a':'b'},401
        
@app.route('/updateShift',methods = ["POST"])
def update_shift():
    token = request.args.get("token")
    request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        return_statement = use_info(request_dict,which_function="update",table="shifts")
        new_token = generate_token(user)
        return {'body':return_statement,'token':new_token}
    else:
        return {'a':'b'},401
    
if __name__ == '__main__':
    app.run(debug=True) 

