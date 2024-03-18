import clingo.control
import clingo
import psycopg2
from psycopg2 import sql


def run_clingo(truck_day_i, clingon_code = '', weeks_to_schedule_i = 1, weeks_scheduled = 0):
    days_in_week = 7
    weeks_to_schedule = weeks_to_schedule_i
    # schedule_blocks
    # last_schedule_block = schedule_blocks -1
    store_minimum_employees = '2'
    store_minimum_supervisors = '1'
    # max_total_weekly_hours = 
    
    truck_day = truck_day_i
    overtime_allowed = False
    weekend_rotation = True
    store_manager_name = "general"
    otExemptRole = 2
    num_models = 0
    
    
    conn = psycopg2.connect(host='localhost',database='roybannon',user = 'roybannon')

    #TODO: make weeks_scheduled and weeks_to_schedule parameters instead of relying on global
    #TODO: update function to format more similar to set_required_skill_for_shift so it works with call from load_shifts
    def set_important_shift(name, start_time, end_time, wk, importance, clingo_code, maximum_shift_hours = None):
        if wk == -1:
            for week in range(weeks_scheduled,weeks_to_schedule):
                for tyme in range(start_time,end_time):
                    day = day + (week * 7)
                    clingo_code += '{}({},{},{}). '.format(name,tyme,day,week)
                    week = str(week)
                clingo_code += '1{' + '{}_time_of_day_emp_count(TOD,D,{},X)'.format(name,week)
                clingo_code += '} :- X = #count{EID : assign(TOD,D,' + week + ',EID)}, '
                clingo_code += '{}(TOD,D,{}). '.format(name,week) + '{' +'{}_hours(X,{})'.format(name,week)
                clingo_code += '} = 1 :- X = #sum{Hours,TOD,' + week + ' : '
                clingo_code += '{}_time_of_day_emp_count(TOD,Day,{},Hours)'.format(name,week) + '}. '
                clingo_code += ':~ {}_hours(X,{}), Value = 0-X, Weight = Value * {}.[Weight] '.format(name,week,importance)
                if maximum_shift_hours != None:
                    clingo_code += ':- {}_hours(X,W), X > {}. '.format(name, maximum_shift_hours)
            return clingo_code
        elif wk in range(weeks_scheduled,weeks_to_schedule):
            for i in range(7):
                day = i + (wk * 7)
                wk = str(wk)
                for tyme in range(start_time,end_time):
                    clingo_code += '{}({},{},{}). '.format(name,tyme,day,wk)
                clingo_code += '1{'
                clingo_code += '{}_time_of_day_emp_count(TOD,D,{},X)'.format(name,wk)
                clingo_code += '} :- X = #count{EID : assign(TOD,D,'+ wk + ',EID)}, '
                clingo_code += '{}(TOD,D,{}). '.format(name,wk)
                clingo_code += '{'
                clingo_code += '{}_hours(X,{})'.format(name,wk)
                clingo_code += '} = 1 :- X = #sum{Hours,TOD,' + wk + ' : '
                clingo_code += '{}_time_of_day_emp_count(TOD,Day,{},Hours)'.format(name,wk)
                clingo_code += '}. '
                clingo_code += ':~ {}_hours(X,{}), Value = 0-X, Weight = Value * {}.[Weight] '.format(name,wk,importance)
                if maximum_shift_hours != None:
                    clingo_code += ':- {}_hours(X,W), X > {}. '.format(name, maximum_shift_hours)

        return clingo_code

    #TODO: make weeks_scheduled and weeks_to_schedule parameters instead of relying on global
    def set_required_skill_for_shift(start_times, end_times, skill, skill_importance, role, clingo_code, minimum_skill_level = None, days = [i for i in range(7)]):
        for wk in range(weeks_scheduled,weeks_to_schedule):
            for i in range(7):
                day = i +(wk * 7)
                for tyme in range(start_times[i],end_times[i]):
                    clingo_code += '{' + 'max_skill_{}({},{},{},EID,Level)'.format(skill,tyme,day,wk)
                    clingo_code += ': assign({},{},{},EID),skill_level(EID,{},Level,{})'.format(tyme,day,wk,skill,role) +'} = 1' + ':- ' 
                    clingo_code += '#max {XX,EID,' + skill + ',' + str(role) + ':skill_level(EID,' + skill + ',XX,' + str(role)  + '),assign({},{},{},EID)'.format(tyme,day,wk) + '} = Level. '
                    clingo_code += '\n'
            clingo_code += ':~ max_skill_{}(_,_,_,_,Level), SkillGap=5-Level, Weight=SkillGap*{}.[Weight] '.format(skill,skill_importance)
        return clingo_code

    def set_weekend_rotation_rule(rotation_list):
        weekend_rotation_rule = ''
        for wk in range(weeks_scheduled,weeks_to_schedule):
            for emp in rotation_list:
                if rotation_list[wk % len(rotation_list)] != emp:
                    weekend_rotation_rule += 'weekend_rotation_off({},{}). '.format(emp,wk)
                # else:
                #     weekend_rotation_rule += 'weekend_rotation({})'.format(emp)
        return weekend_rotation_rule
        
    def load_employees(connection):
        cur = connection.cursor()
        cur.execute(sql.SQL("SELECT * FROM employees JOIN extremes USING (id)"))
        
        for emp in cur.fetchall():
            # print(emp)
            Employee(*emp)

    def load_req_skills(connection,weeks_scheduled, weeks_to_schedule,clingo_code):
        cur = connection.cursor()
        cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('required_skills_for_shift')))
        skill_info = cur.fetchall()
        #TODO: extract for loop except function call, make it a function to be used for load_shifts as well.
        for skill in skill_info:
            start_times = skill[1][0:7]
            end_times = skill[1][7:]
            skill_name = skill[0].lower().replace(" ", "_")
            role = skill[2]
            importance = skill[3]
            clingo_code = set_required_skill_for_shift(start_times,end_times,skill_name,importance,role,clingo_code)
        return clingo_code
    
    def load_skill_levels(connection,emp_skill_levels_dict):
        cur = connection.cursor()
        cur.execute(sql.SQL("SELECT * FROM {} ").format(sql.Identifier('skills')))
        skill_lvl_info = cur.fetchall()

        for row in skill_lvl_info:
            skill_name = row[0].lower().replace(" ","_")
            emp = row[1]
            skill_lvl = row[2]

            emp_skill_levels_dict[emp][skill_name] = skill_lvl
        
        set_skill_levels(emp_skill_levels_dict)
        
    def load_shifts(connection,clingo_code):
        cur = connection.cursor()
        cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier('shifts')))
        shift_info = cur.fetchall()
        for shift in shift_info:
            start_times = shift[-1][0:7]
            end_times = shift[-1][7:]
            shift_name = shift[0].lower().replace(" ", "_")
            importance = shift[1]
            max_hours = shift[2]
            clingo_code = set_important_shift(shift_name,start_times,end_times,importance,clingo_code,maximum_shift_hours=max_hours)
        return clingo_code

    def set_skill_levels(employee_skill_levels_dict):
        for emp in Employee.employees.values():
            emp.skills = employee_skill_levels_dict[emp.employee_id]
        
    def extract_and_format_schedule_blocks(schedule_info):
        schedule_blocks = [[],[],[],[],[],[],[]]
        for i in range(len(schedule_info)):
            schedule_blocks[i % 7].append(schedule_info[i])
    
        return schedule_blocks

    def load_business_info(connection):
        cur = connection.cursor()
        cur.execute(sql.SQL("SELECT * FROM {} ").format(sql.Identifier('business_info')))
        business_info = [i for i in cur.fetchall()[0]]
        
        business_info[1] = extract_and_format_schedule_blocks(business_info[1])
        
        return business_info
        
    def load_availability(connection):
        cur = connection.cursor()
        cur.execute(sql.SQL("SELECT * FROM {} ").format(sql.Identifier('availability')))
        emp_availabilities = [i for i in cur.fetchall()]
        for emp in emp_availabilities:
            info = [i for i in emp]
            start_times = info[1][:7]
            end_times = info[1][7:]
            Employee.employees[info[0]].set_availability(start_times,end_times,0,0)
        


    class Employee():
        employees = {}
        weekly_hours = {}
        @staticmethod
        def increment_emp_count(emp):
            Employee.employees[emp.employee_id] = emp

        def __init__(self,employee_id,first_name,last_name, role, wage, min_shift,max_shift,min_weekly,max_weekly,min_days,max_days):
            self.employee_id = employee_id
            self.shift_preferences = {w:{i:[-20 for j in range(schedule_blocks[i][0],schedule_blocks[i][1])] for i in range(days_in_week)} for w in range(weeks_scheduled,weeks_to_schedule)}
            self.role = role
            self.skills = {}
            self.wage = wage//2
            self.first_name = first_name.lower() #Should be updatable.
            self.last_name = last_name 
            self.minimum_weekly_hours = min_weekly * 2
            self.maximum_weekly_hours = max_weekly * 2
            self.minimum_shift_length = min_shift * 2
            self.maximum_shift_length = max_shift * 2
            self.max_days = max_days
            self.meal_break = False
            
            Employee.increment_emp_count(self)

        def __repr__(self):
            return self.first_name + " " + self.last_name
        
        def add_rules(self):
            clingo_add = self.add_employee()
            clingo_add += self.set_minimum_weekly_hours(self.minimum_weekly_hours)
            clingo_add += self.set_maximum_weekly_hours(self.maximum_weekly_hours)
            clingo_add += self.set_minimum_shift_length(self.minimum_shift_length)
            clingo_add += self.set_maximum_shift_length(self.maximum_shift_length)
            clingo_add += self.set_max_days()
            if self.meal_break:
                clingo_add += self.add_meal_break()
            for skill in self.skills.keys():
                clingo_add += self.set_clingo_skill_levels(skill,self.skills[skill])

            return clingo_add
        
        def set_availability(self, start_times, end_times, week, available, days = [0,1,2,3,4,5,6]):
            self.set_shift_preferences(days,start_times,end_times,[available for day in days],weeks = [week])
        
           
        def set_shift_preferences(self, days, start_times, end_times, preference_lvls, weeks = [wk for wk in range(weeks_scheduled,weeks_to_schedule)]):
           
            for week in weeks:
                for i in range(len(days)):
                    start_time = max(start_times[i] - schedule_blocks[i][0],0)
                    end_time = min(((end_times[i] - schedule_blocks[i][0]) * 2), schedule_blocks[i][1]- schedule_blocks[i][0])
                    for j in range(start_time,end_time):
                        self.shift_preferences[week][days[i]][j] = preference_lvls[i]
            print(self.first_name, self.shift_preferences)
            

        def add_employee(self):
            clingo_addition = 'employee({},{},{}).'.format(self.first_name, self.role,self.wage)
            return clingo_addition
        
        #TODO: minimum weekly hours rules should depend on whether emp is available for enough hours that week.
        def set_minimum_weekly_hours(self, new_min_hours, weeks = [wk for wk in range(weeks_scheduled,weeks_to_schedule)]):
            self.minimum_weekly_hours = new_min_hours
            clingo_addition = ''
            for week in weeks:
                clingo_addition += ':- hours_count({},{},X), X < {}.'.format(self.first_name, week, new_min_hours)
            return clingo_addition

        def set_maximum_weekly_hours(self, new_max_hours, weeks = [wk for wk in range(weeks_scheduled,weeks_to_schedule)]):
            self.maximum_weekly_hours = new_max_hours
            clingo_addition = ''
            for week in weeks:
                clingo_addition = ':- hours_count({},{},X), X > {}. '.format(self.first_name, week, new_max_hours)
            return clingo_addition

        def set_minimum_shift_length(self, new_min_shift_length):
            self.minimum_shift_length = new_min_shift_length
            clingo_addition = ':- hours_count({},D,W,X),X < {}, assign(_,D,W,{}). '.format(self.first_name,new_min_shift_length,self.first_name)
            return clingo_addition
        
        def set_maximum_shift_length(self, new_max_shift_length):
            self.maximum_shift_length = new_max_shift_length
            clingo_addition = ':- hours_count({},D,W,X),X > {}. '.format(self.first_name,new_max_shift_length)
            return clingo_addition
        
        def set_max_days(self):
            clingo_addition = ':- days_count({},W,X), X > {}. '.format(self.first_name, self.max_days)
            return clingo_addition
        
        def set_skill_level(self,skill,skill_lvl):
            self.skills[skill] = skill_lvl

        def set_clingo_skill_levels(self,skill,skill_lvl):
            clingo_addition = 'skill_level({},{},{},{}). '.format(self.first_name,skill,skill_lvl,self.role)
            return clingo_addition
        
        def add_meal_break(self):
            clingo_addition = '{meal_break(TOD,D,W,'
            clingo_addition += '{}) : time(TOD,D,W)'.format(self.first_name)
            clingo_addition += '} = 1'
            clingo_addition += ' :- hours_count({},D,W,X), X > 6. '.format(self.first_name)
            clingo_addition += 'assign(TOD,D,W,{}) :- meal_break(TOD+1,D,W,{}). '.format(self.first_name, self.first_name)
            clingo_addition += 'assign(TOD,D,W,{}) :- meal_break(TOD-1,D,W,{}). '.format(self.first_name, self.first_name)
            return clingo_addition

    
    clingo_code = clingon_code
    business_info = load_business_info(conn)
    business_name, schedule_blocks, store_minimum_employees, store_minimum_supervisors,otExemptRole, max_total_weekly_hours, total_weekly_hours_weight = business_info
    
    max_total_weekly_hours *= 2
    # max_total_weekly_hours = 438
    for i in range(len(schedule_blocks)):
        schedule_blocks[i][1] = ((schedule_blocks[i][1] - schedule_blocks[i][0]) * 2) + schedule_blocks[i][0]
    # print(schedule_blocks)

    load_employees(conn)
    employee_skill_levels_dict = {emp:{} for emp in Employee.employees.keys()}
    load_availability(conn)
    clingo_code = load_req_skills(conn,weeks_scheduled,weeks_to_schedule,clingo_code)
    load_skill_levels(conn, employee_skill_levels_dict)
    
    Employee.employees[1].meal_break = True
   
    # str_last_schedule_block = str(last_schedule_block)
    for i in range(weeks_scheduled,weeks_to_schedule):
        str_i = str(i)
        # str_next_week = str(i + 1)
        

        #TODO: Refactor the below code into a function.
        
        clingo_code += '1{hours_count(EID,' + str_i + ',X)} :- X = #count{TOD,D : week' + str_i + '(assign(TOD,D,'+ str_i + ',EID)), not meal_break(TOD,D,' + str_i + ',EID)}, employee(EID,_,_).  '
        # clingo_code += '1{total_weekly_hrs('+ str_i + ',X)} :- X = #count{TOD,D,' + str_i + ',EID : assign(TOD,D,' + str_i + ',EID), not meal_break(TOD,D,' + str_i + ',EID)}.'
        clingo_code += '1{total_weekly_hrs('+ str_i + ',X)} :- X = #count{TOD,D,EID : week' + str_i + '(assign(TOD,D,' + str_i + ',EID)), not meal_break(TOD,D,' + str_i + ',EID)}.'
        clingo_code += '1{days_count(EID,'+ str_i + ',X)} :- X = #count{D : assign(TOD,D,'+ str_i + ',EID)}, employee(EID,_,_).  '
        clingo_code += ':~ total_weekly_hrs('+ str_i + ',Y),Y > {}, Value = Y - {}, Weight = Value * {}.[Weight] '.format(max_total_weekly_hours,
                                                                        max_total_weekly_hours,total_weekly_hours_weight)
        # clingo_code += ':- total_weekly_hrs('+ str_i + ',Y), Y > {}.'.format(425)
        

# TODO: replace assign/4 with assign/3 and week{}/1.
    for week in range(weeks_scheduled,weeks_to_schedule):
        start_day = 0+(7*week)
        end_day = 6 + (7*week)
        clingo_code += 'week{}(assign(TOD,D,{},EID)) :- assign(TOD,D,{},EID), D = {}..{}.'.format(week,week,week,start_day,end_day)
        

    for emp in Employee.employees.values():
        clingo_code += emp.add_rules()


    #TODO: Normalize values so that weights are on same scale.
    #TODO: Minimize wages paid.
    #TODO: Feature for rotating weekend shifts.
    #TODO: Make sure meal breaks are at appropriate time of shift. - somewhat done - avoids early breaks and late breaks.
    #TODO: Alter how skills work so that user can choose whether to use the skill gap for the best employee on the shift or the aggregate skill gap for all emps on the shift.
        #Currently just uses the best, previously used only the aggregate.

    for i in range(days_in_week):
        for j in range(schedule_blocks[i][0],schedule_blocks[i][1]):
            for L in range(weeks_scheduled,weeks_to_schedule):
                
                clingo_code += 'time({},{},{}). '.format(j,i+(L*7),L)
                emp_vals = list(Employee.employees.values())
                for k in range(len(emp_vals)):
                    if emp_vals[k].shift_preferences[L][i][j-schedule_blocks[i][0]] != 0:
                        pref_block = 'shift_preference({},{},{},{},{}).   '.format(j,i+(L*7),L,emp_vals[k].first_name, emp_vals[k].shift_preferences[L][i][j-schedule_blocks[i][0]])
                        clingo_code += pref_block


    employee_count_assignment = str(store_minimum_employees) + '{assign(TOD,D,W,EID): employee(EID,_,_)} :- time(TOD,D,W), not TOD = 0.  '
    clingo_code += employee_count_assignment


    supervisor_count_assignment = str(store_minimum_supervisors) + '{assign(TOD,D,W,EID): employee(EID,1,_)} :- time(TOD,D,W).   '
    clingo_code += supervisor_count_assignment


    daily_hours_count_clingo = '1{hours_count(EID,D,W,X)} :- X = #count{TOD : assign(TOD,D,W,EID),not meal_break(TOD,D,W,EID)}, employee(EID,_,_), time(_,D,W).   '
    clingo_code += daily_hours_count_clingo


    no_breaking_up_shifts = ':- assign(TOD,D,W,EID), not assign(TOD2,D,W,EID), assign(TOD3,D,W,EID), time(TOD,D,W),time(TOD2,D,W),'
    no_breaking_up_shifts += 'time(TOD3,D,W),TOD3 > TOD2, TOD2 > TOD. '
    clingo_code += no_breaking_up_shifts


    clingo_code = set_important_shift('truck',19,schedule_blocks[truck_day][1],truck_day,0,7,clingo_code)
    # clingo_code = set_important_shift('truck',11,last_schedule_block,truck_day,1,7,clingo_code)
    # clingo_code = set_important_shift('truck',11,last_schedule_block,truck_day,2,7,clingo_code)

    # clingo_code = set_required_skill_for_shift(20,last_schedule_block,'count_drawers',5,1,clingo_code)
    # clingo_code = set_required_skill_for_shift(0,14,'dsd',3,1,clingo_code,days=[1,2,3,4,5])
    # clingo_code = set_required_skill_for_shift(14,last_schedule_block,'sign_audit',4,1,clingo_code,days = [0])

    meal_breaks_not_allowed_close_to_shift_start = ':- meal_break(TOD2,D,W,EID), not assign(TOD,D,W,EID), TOD2 = TOD + 3.'
    meal_breaks_not_allowed_close_to_shift_end = ':- meal_break(TOD,D,W,EID), not assign(TOD2,D,W,EID), TOD2 = TOD + 3.'
    clingo_code += meal_breaks_not_allowed_close_to_shift_start
    clingo_code += meal_breaks_not_allowed_close_to_shift_end

    if overtime_allowed == False:
        clingo_code += ':- hours_count(EID,W,X), X>80, not EID = {}.'.format("general")
    else:
        clingo_code += ':~ hours_count(EID,W,X), X>80, not role = {}, Y = X - 80, Weight = Y * 3.[Weight]'
         
    clingo_code+="""
    {assign(0,D,W,EID) : employee(EID,1,_)} = 1 :- time(0,D,W).

    %Below rule does not prevent being scheduled Wk 0 Day 0 off, Wk 0 Day 6 off, Wk1 Day5 off, Wk 1 Day 6 off.
    :~ assign(_,D,W,EID), not assign(_,D2,W,EID), assign(_,D3,W,EID),days_count(EID,W,X), X = 5, employee(EID,_,_), D2 = D + 1, D3 = D2 + 1, Weight = 70.[Weight]
    :- assign(35,Day,W,EID), assign(8,Day2,W,EID), Day2 = Day + 1.

    :~ assign(TOD,Day,W,EID), shift_preference(TOD,Day,W,EID,X), Weight = 0 - X.[Weight]
    :- assign(TOD,Day,W,EID), shift_preference(TOD,Day,W,EID,-20).
    
    :- days_count(EID,W,6), days_count(EID,W2,6), W2 = W + 1.
    #show meal_break/4.
    #show assign/4.
    #show total_weekly_hrs/2.
    #show truck_hours/2.
    #show days_count/3.
    #show hours_count/3.



    """
    # print(clingo_code)
    solution = None

    days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    def on_model(model):
        emp_names = []
        for emp in Employee.employees.values():
            emp_names.append(emp.first_name)
        schedule_dict = {wk:{name:{} for name in emp_names} for wk in range(weeks_to_schedule)}
        for wk in range(weeks_to_schedule):
            for emp in Employee.employees.values():
                for i in range(7):
                    schedule_dict[wk][emp.first_name][i] = []
        

        solution = str(model)
        solution2 = solution.replace(' ','. ')
        with open('Schedule/clingoSolution.txt','w') as file:
            file.write(solution2)
        
        solution = solution.replace('(',',')
        solution = solution.replace(')','')
        solution = solution.split(' ')
        
        for block in solution:
            if 'assign' in block:
                block = block.split(',')
                try:
                    schedule_dict[int(block[3])][block[-1]][int(block[2])%7].append(int(block[1]))
                except:
                    continue
            elif 'hours' in block or 'total_weekly_hrs' in block:
                print(block)
                continue
            else:
                continue
            
            
        with open('Schedule/scheduleFile.txt','w') as file2:
            schedule = []

            for wk in schedule_dict.keys():
                for emp in schedule_dict[wk].keys():
                    for day in schedule_dict[wk][emp].keys():
                        formatted_emp = emp.capitalize()

                        if schedule_dict[wk][emp][day]:
                            schedule_block = '{}:{}-{},'.format(formatted_emp,((min(schedule_dict[wk][emp][day])-8)/2)+8,((max(schedule_dict[wk][emp][day])-8)/2)+8.5)
                            schedule.append(schedule_block)
                        else:
                            schedule_block = formatted_emp + ':' + 'Off,'
                            schedule.append(schedule_block)
            
            file2.writelines(schedule)
        return solution
            

    def ground_and_solve():
        max_step = 1

        control = clingo.Control()
        control.configuration.solve.models = num_models #Control how many unique models are generated.
        # print(clingo_code)
        try:
            control.add("base", [], clingo_code)
        except:
            RuntimeError(clingo_code)
        parts = []
        parts.append(("base", []))
        control.ground(parts)
        
        ret, step = None, 1
        while step <= max_step:
            
            # solution = control.solve(on_model=on_model)
            with control.solve(on_model=on_model,async_=True) as ret:
                if not ret.wait(180):
                    print('cancelling')
                    ret.cancel()
            
                
                
                
                
            step += 1
        
        
    ground_and_solve()
    # return clingo_code
    