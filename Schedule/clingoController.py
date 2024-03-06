import clingoSchedule

clingoSchedule.run_clingo(3)
solution = ''
with open('Schedule/clingoSolution.txt','r') as file:
    solution += file.read()
    solution += '.'
    
# print("Testing", solution)
print('Model for week 1 completed')
print('Now running program to obtain model for week 2')
# clingoSchedule.run_clingo(1,solution,2,1)