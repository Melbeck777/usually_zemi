import datetime
from module import write_summary

def print_list(list, start=0):
    for index, element in enumerate(list):
        print("{} : {}".format(index+start,element))

today = datetime.datetime.today()
lab_member = write_summary.get_lab_member(today)
degree = list(lab_member.keys())
print_list(degree)
degree_index = int(input("Input degree index :"))
group_names = list(lab_member[degree[degree_index]].keys())
print_list(group_names[1:],1)
group_index = int(input("Input group name index :"))
group_info = [degree[degree_index], group_names[group_index]]
schedule = write_summary.get_schedule(group_info)
print_list(schedule)
day_index = int(input("Input day index : "))
print(schedule[day_index])
write_summary.create_one_day_summary(group_info, day_index)