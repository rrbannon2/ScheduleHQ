from flask import Flask, request, jsonify, session, make_response
import clingoSchedule
import psycopg2
from psycopg2 import sql
import secrets
import hashlib
from userClass import User
import datetime

#TODO: Remove references to "schedule_29_2024", replace with a generated table

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
    execute_SQL("CREATE TABLE {} (id int PRIMARY KEY, first_name varchar(255), last_name varchar(255), role int, wage int)",[sql.Identifier('{}_employees'.format(user_org))])
    execute_SQL("CREATE TABLE {} (id int PRIMARY KEY, shift_pref integer ARRAY[28] DEFAULT %s)",[sql.Identifier('{}_availability'.format(user_org))],execute_args=[zero_val_array])
    execute_SQL("CREATE TABLE {} (skill varchar(255), id int, skill_level int, CONSTRAINT {} PRIMARY KEY (skill,id))",[sql.Identifier('{}_skills'.format(user_org)),sql.Identifier('{}_skillsPK'.format(user_org))])
    execute_SQL("CREATE TABLE {} (skill varchar(255), schedule_blocks integer ARRAY[14], importance int, role int)",[sql.Identifier('{}_required_skills_for_shift'.format(user_org))])
    execute_SQL("CREATE TABLE {} (id int PRIMARY KEY, min_shift int DEFAULT 0, max_shift int DEFAULT 24, min_weekly int DEFAULT 0, max_weekly int DEFAULT 120, min_days int DEFAULT 0, max_days int DEFAULT 7)",[sql.Identifier('{}_extremes'.format(user_org))])
    execute_SQL("CREATE TABLE {} (business_name varchar(255), hours_of_op integer ARRAY[28], min_employees int, min_managers int, exempt_role int,max_total_hours int, max_hours_importance int)",[sql.Identifier('{}_business_info'.format(user_org))])
    execute_SQL("CREATE TABLE {} (shiftName varchar(255), schedule_blocks integer ARRAY[14], importance int, maxHours int)",[sql.Identifier('{}_shifts'.format(user_org))])

    return jsonify("Sign up successful!")

def authenticate(email,password):
    query_response = execute_SQL("SELECT user_id, salt, salted_password, organization FROM {} WHERE email = %s",[sql.Identifier("admin_users")],execute_args=[email]) 
    if query_response:
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
    else:
        return None

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
    print(tokens_dict)

    return token

def create_cookie_response(token, response_value, response_name = 'body', cookie_lifespan = 300):
    cookie_response = make_response({response_name:response_value,"token":token})
    cookie_response.set_cookie("token",token,cookie_lifespan,samesite='Strict')
    return cookie_response

# def token_required(request_func):
#     # print(request.get_json)
#     token = request.cookies.get("token")
#     user = token_verify(token)
#     if user:
#         body = request_func()
#         new_token = generate_token(user)
#         return {"token":new_token,"body":body}
#     else:
#         return {'a':'b'},401
    
# app.config['before_request'] = token_required

@app.route('/login',methods = ["POST"])
def login():
    login_info = request.get_json()
    email = login_info["userEmail"]
    attempt_password = login_info["password"]
    user = authenticate(email,attempt_password)
    if user:
        token = generate_token(user)
        cookie_response = create_cookie_response(token,"Login Successful","response")
        return cookie_response
    else:
        return {"response": "Email or Password incorrect, please try again.","token":None}

def add_default_emp_skill_level(skill,emp, organization):     
    execute_SQL("INSERT INTO {} VALUES(%s,%s,%s)",[sql.Identifier('{}_skills'.format(organization))],execute_args = [skill,emp,0])
    return None



@app.route('/addEmployee',methods = ["POST"])
def add_employee():
    token = request.cookies.get("token")
    request_dict = request.get_json()
    user = token_verify(token)
    if user:
        emp_info = list(request_dict.values())
        organization = user.get_organization()
        avail_info = emp_info[11:]
        avail_info = [int(i) for i in avail_info]
        execute_SQL("INSERT INTO {}(id, first_name, last_name, role, wage) VALUES (%s, %s, %s, %s, %s)",[sql.Identifier('{}_employees'.format(organization))],execute_args = emp_info[0:5])
        id = emp_info[0]
        
        execute_SQL("INSERT INTO {} VALUES(%s, %s)",[sql.Identifier('{}_availability'.format(organization))],execute_args = [id,avail_info]) 
        execute_SQL("INSERT INTO {} VALUES(%s, %s, %s, %s, %s, %s, %s)",[sql.Identifier('{}_extremes'.format(organization))],execute_args = [id,*emp_info[5:11]])
        skill_names = execute_SQL("SELECT skill FROM {}",[sql.Identifier('{}_required_skills_for_shift'.format(organization))])
        
        #Could possibly be achieved with a temporary single row single column table for id, LEFT JOIN(SELECT skill FROM required_skills_for_shift,id_table)
        for name in skill_names:
            execute_SQL("INSERT INTO {} VALUES(%s,%s,%s)",[sql.Identifier('{}_skills'.format(organization))],execute_args = [name,id,0])
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,"Employee Added Successfully")
        return cookie_response
    else:
        return {'a':'b'},401

@app.route('/loadEmployeeInfo',methods=["GET"])
def load_employee_info():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        employee = request.args.get('employee')
        query_response = execute_SQL("SELECT * FROM {} JOIN {} USING (id) JOIN {} USING (id) WHERE id = %s",(sql.Identifier('{}_employees'.format(organization)),sql.Identifier('{}_extremes'.format(organization)),sql.Identifier('{}_availability'.format(organization))),execute_args = [employee])
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,query_response)
        return cookie_response
    else:
        return {'a':'b'},401

@app.route('/loadEmployeeListData',methods = ["GET"])
def load_employee_names():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        try:
            query_response = execute_SQL("SELECT first_name, last_name, id, role FROM {}",[sql.Identifier('{}_employees'.format(organization))])
        except:
            new_token = generate_token(user)
            return create_cookie_response(new_token,"No existing employees found")
        return_array = [{"firstName":emp[0], "lastName":emp[1], "id":emp[2], "role":emp[3]} for emp in query_response]
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,return_array)
        return cookie_response
    else:
        return {'a':'b'},401


@app.route('/updateEmployee',methods = ["POST"])
def update_employee():
    token = request.cookies.get("token")
    request_dict = request.get_json()
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
        execute_SQL("UPDATE {} SET(min_shift,max_shift,min_weekly,max_weekly,min_days,max_days) = (%s, %s, %s, %s, %s, %s) WHERE id = %s",[sql.Identifier('{}_extremes'.format(organization))],execute_args = [*extremes_table_data,emp_id])
        execute_SQL("UPDATE {} SET shift_pref = %s WHERE id = %s",[sql.Identifier('{}_availability'.format(organization))],execute_args = [avail_info,emp_id])
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,"Updated Employee Information Saved Successfully.")
        return cookie_response
    else:
        return {'a':'b'},401
        

@app.route('/deleteEmployee',methods = ["POST"])
def delete_employee():     
    token = request.cookies.get("token")
    emp_id = request.get_json()
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        execute_SQL("DELETE FROM {} WHERE id = %s",[sql.Identifier('{}_employees'.format(organization))],execute_args = [emp_id])
        execute_SQL("DELETE FROM {} WHERE id = %s",[sql.Identifier('{}_extremes'.format(organization))],execute_args = [emp_id])
        execute_SQL("DELETE FROM {} WHERE id = %s",[sql.Identifier('{}_availability'.format(organization))],execute_args = [emp_id])
        execute_SQL("DELETE FROM {} WHERE id = %s",[sql.Identifier('{}_skills'.format(organization))],execute_args = [emp_id])
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,"Employee Deleted Successfully")
        return cookie_response
    else:
        return {'a':'b'},401

@app.route('/deleteSkill',methods=["POST"])
def delete_skill():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        skill_name = request.get_json()
        execute_SQL("DELETE FROM {} WHERE skill = %s",[sql.Identifier('{}_required_skills_for_shift'.format(organization))],execute_args = [skill_name])
        execute_SQL("DELETE FROM {} WHERE skill = %s",[sql.Identifier('{}_skills'.format(organization))],execute_args = [skill_name])
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,"Skill Deleted Successfully")
        return cookie_response
    else:
        return {'a':'b'},401

@app.route('/deleteShift',methods = ["POST"])
def delete_shift():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        shift_name = request.get_json()
        execute_SQL("DELETE FROM {} WHERE shiftName = %s",[sql.Identifier('{}_shifts'.format(organization))],execute_args = [shift_name])
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,"Shift Deleted Successfully")
        return cookie_response
    else:
        return {'a':'b'},401

@app.route('/deleteUser',methods = ["POST"])
def delete_user():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        # organization = user.get_organization()
        user_name = request.get_json()
        execute_SQL("DELETE FROM {} WHERE email = %s",[sql.Identifier('users')],execute_args = [user_name])
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,"User Deleted Successfully")
        return cookie_response
    else:
        return {'a':'b'},401


@app.route('/writeSchedule', methods = ["POST"])
def write():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        user_org = user.get_organization()
        response = request.get_json()
        print(response["date"])
        try:
            execute_SQL("CREATE TABLE {} (id int PRIMARY KEY,first_name varchar(255), last_name varchar(255),sunday varchar(255), monday varchar(255), tuesday varchar(255), wednesday varchar(255), thursday varchar(255), friday varchar(255), saturday varchar(255),total_hours varchar(64),week_ending_date varchar(255))",[sql.Identifier("{}_{}".format(user_org,response["date"]))])
        except Exception as error:
            print(error)
            execute_SQL("DROP TABLE {}",[sql.Identifier('{}_{}'.format(user_org,response["date"]))])
            execute_SQL("CREATE TABLE {} (id int PRIMARY KEY,first_name varchar(255), last_name varchar(255),sunday varchar(255), monday varchar(255), tuesday varchar(255), wednesday varchar(255), thursday varchar(255), friday varchar(255), saturday varchar(255),total_hours varchar(64),week_ending_date varchar(255))",[sql.Identifier("{}_{}".format(user_org,response["date"]))])
            

        clingoSchedule.run_clingo(user_org,response["seconds"],response["date"])
        new_token = generate_token(user)
        response_val = "Schedule is being generated"
        cookie_response = create_cookie_response(new_token,response_val)
        return cookie_response
    else:
        return {'a':'b'},401
    

@app.route('/getSchedule',methods= ["GET"])
def get_schedule():
    token = request.cookies.get("token")
    # request_dict = request.get_json()
    # token = request_dict["token"]
    user = token_verify(token)
    if user:
        user_org = user.get_organization()
        try:
            date = request.args.get("wEndDate")
            print(date)
        except Exception as error:
            print(error)
        dates_list = []
        if not date:

            today = datetime.date.today()
            date = (today + datetime.timedelta((5-today.weekday()) % 7))

            for i in range(-2,4):
                dates_list.append((date + datetime.timedelta(7*i)).strftime("%m/%d/%Y"))
            date = date.strftime("%m/%d/%Y")
        else:
            print(date)
            if "-1" in date:
                date = date[:-2]
                date = datetime.datetime.strptime(date,'%m/%d/%Y')
                date = date - datetime.timedelta(7)
                if date.weekday() == 5:
                    for i in range(-2,4):
                        dates_list.append((date + datetime.timedelta(7*i)).strftime("%m/%d/%Y"))
                    date = date.strftime("%m/%d/%Y")
                else:
                    date = "Selected date is not a Saturday, please choose a different date"

            elif " 1" in date:
                print("Plus One Week")
                date = date[:-2]
                date = datetime.datetime.strptime(date,'%m/%d/%Y')
                date = date + datetime.timedelta(7)
                if date.weekday() == 5:
                    for i in range(-2,4):
                        dates_list.append((date + datetime.timedelta(7*i)).strftime("%m/%d/%Y"))
                    date = date.strftime("%m/%d/%Y")
                else:
                    date = "Selected date is not a Saturday, please choose a different date"
            else:
                date = datetime.datetime.strptime(date,'%m/%d/%Y')
                if date.weekday() == 5:
                    for i in range(-2,4):
                        dates_list.append((date + datetime.timedelta(7*i)).strftime("%m/%d/%Y"))
                    date = date.strftime("%m/%d/%Y")
                else:
                    date = "Selected date is not a Saturday, please choose a different date"
        try:
            solution = execute_SQL("SELECT * FROM {}",[sql.Identifier('{}_{}'.format(user_org,date))])
            if len(solution) > 0:
                response_val = {"response":solution,"fetchedDate":date,"datesInfo":dates_list}
            else:
                response_val = {"response":"False","fetchedDate":date,"datesInfo":dates_list}
        except Exception as error:
            print(error)
            response_val = {"response":"False","fetchedDate":date,"datesInfo":dates_list}
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,response_val)
        return cookie_response
    else:
        return {'a':'b'},401
        

@app.route('/updateBusinessInfo',methods = ["POST"])
def update_business_info():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        business_info = list(request.get_json().values())
        business_name = business_info[0]
        business_info_ints = [int(i) for i in business_info[1:]]
        hours_of_op = business_info_ints[5:]

        update_Bool = execute_SQL("SELECT * FROM {}",[sql.Identifier('{}_business_info'.format(organization))])
        if update_Bool:
            execute_SQL("UPDATE {} SET (business_name,min_employees,min_managers,exempt_role,max_total_hours,max_hours_importance,hours_of_op) = (%s,%s,%s,%s,%s,%s,%s)",[sql.Identifier('{}_business_info'.format(organization))],execute_args = [business_name,*business_info_ints[:5],hours_of_op])
        else:
            execute_SQL("INSERT INTO {} VALUES(%s,%s,%s,%s,%s,%s,%s)",[sql.Identifier('{}_business_info'.format(organization))],execute_args = [business_name,hours_of_op,*business_info_ints[:5]])
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,"Business Information Updated Successfully")
        return cookie_response
    else:
        return {'a':'b'},401
    

@app.route('/loadBusinessInfo',methods = ["GET"])
def load_business_info():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        business_info = execute_SQL("SELECT * FROM {}",[sql.Identifier('{}_business_info'.format(organization))])
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,business_info)
        return cookie_response
    else:
        return {'a':'b'},401


@app.route('/loadSkillLevels',methods = ["GET"])
def load_skill_levels():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        employee = request.args.get('employee')
        query_response = execute_SQL("SELECT skill,skill_level FROM {} WHERE id = %s",[sql.Identifier('{}_skills'.format(organization))],execute_args = [employee])
        new_token = generate_token(user)
        print("Query response",query_response)
        cookie_response = create_cookie_response(new_token,query_response)
        return cookie_response
    else:
        return {'a':'b'},401


@app.route('/updateSkillLevel',methods = ["POST"])
def update_skill_level():
    token = request.cookies.get("token")
    request_data = request.get_json()
    # token = request_data["token"]
    user = token_verify(token)
    if user:
        print(request_data)
        organization = user.get_organization()
        id = request_data['id']
        skills = request_data["skills"]
        for skill_key in skills.keys():
            skill = skill_key
            skill_level = skills[skill_key]
            execute_SQL("UPDATE {} SET skill_level = %s WHERE id = %s AND skill = %s",[sql.Identifier('{}_skills'.format(organization))],execute_args = [skill_level,id,skill])
        
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,"Skill levels updated successfully")
        return cookie_response
    else:
        return {'a':'b'},401

@app.route('/loadSkillInfo',methods = ["GET"])
def load_skill_info():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        return load_selected_item_details(request.args.get('skill'),"required_skills_for_shift",'skill',user)
    else:
        return {'a':'b'},401

@app.route('/loadShiftInfo', methods = ["GET"])
def load_shift_info():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        return load_selected_item_details(request.args.get('shift'),"shifts","shiftname",user)
    else:
        return {'a':'b'},401

def load_selected_item_details(selected_item,table,name_column,user):
    organization = user.get_organization()
    table = organization + '_' + table
    item_info = execute_SQL("SELECT * FROM {} WHERE {} = %s",(sql.Identifier(table),sql.Identifier(name_column)),execute_args = [selected_item])
    new_token = generate_token(user)
    cookie_response = create_cookie_response(new_token,item_info)
    return cookie_response


@app.route('/loadRequiredSkills', methods = ["GET"])
def load_required_skills():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        return_array = load_drop_down_info(["skill","importance","role"],"{}_required_skills_for_shift".format(organization))
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,return_array,response_name="returnArray")
        return cookie_response
    else:
        return {'a':'b'},401

@app.route('/loadShifts', methods = ["GET"])
def load_shifts():
    token = request.cookies.get("token")
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        return_array = load_drop_down_info(["shiftname","importance","maxhours"],"{}_shifts".format(organization))
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,return_array)
        return cookie_response
    else:
        return {'a':'b'},401

def load_drop_down_info(columns_to_select,table):
    query_response = execute_SQL("SELECT {},{},{} FROM {}",(sql.Identifier(columns_to_select[0]),sql.Identifier(columns_to_select[1]),sql.Identifier(columns_to_select[2]),sql.Identifier(table)))        

    return_array = [{"name":x[0], "importance":x[1], columns_to_select[2]:x[2]} for x in query_response]
    return return_array

@app.route('/updateSkill',methods = ["POST"])
def update_skill():
    token = request.cookies.get("token")
    request_dict = request.get_json()
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        return_statement = use_info(request_dict,which_function="update",table="{}_required_skills_for_shift".format(organization))
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,return_statement)
        return cookie_response
    else:
        return {'a':'b'},401
    
@app.route('/addSkill', methods = ["POST"])
def add_skill():
    token = request.cookies.get("token")
    request_dict = request.get_json()
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        status, skill = use_info(request_dict,which_function="insert",table="{}_required_skills_for_shift".format(organization))
        if status == "Skill Added Successfully":
            emp_ids = execute_SQL("SELECT id FROM {}",[sql.Identifier('{}_employees'.format(organization))])
            for id in emp_ids:
                add_default_emp_skill_level(skill,id,organization)
            return_statement = "Skill Added Successfully"
        else:
            return_statement = "Skill Not Added"
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,return_statement)
        return cookie_response
    else:
        return {'a':'b'},401
        

def use_info(info,which_function = None,table = None):
    if "required_skills_for_shift" in table:
        time_vals = list(info.values())[3:]
        time_vals = [int(i) for i in time_vals]
        
        name = info['skillName']
        info3 = info['role']
        importance = info['importance']
        role_or_max_hrs = 'role'
        name_column = "skill"
        return_statement = "Skill Operation Successful",name
    elif "shifts" in table:
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
    token = request.cookies.get("token")
    request_dict = request.get_json()
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        return_statement = use_info(request_dict,which_function="insert",table="{}_shifts".format(organization))
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,return_statement)
        return cookie_response
    else:
        return {'a':'b'},401
        
@app.route('/updateShift',methods = ["POST"])
def update_shift():
    token = request.cookies.get("token")
    request_dict = request.get_json()
    user = token_verify(token)
    if user:
        organization = user.get_organization()
        return_statement = use_info(request_dict,which_function="update",table="{}_shifts".format(organization))
        new_token = generate_token(user)
        cookie_response = create_cookie_response(new_token,return_statement)
        return cookie_response
    else:
        return {'a':'b'},401
    
if __name__ == '__main__':
    app.run(debug=True,port=5001) 

