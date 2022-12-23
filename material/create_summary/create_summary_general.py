import datetime
from module.get_lab_data import get_lab_member
from module.make_summary import make_summary

def print_list(list, start=0):
    for index, element in enumerate(list[start:]):
        print("{} : {}".format(index+start,element))

def input_range(list, start=0):
    print_list(list, start)
    index = int(input("Input index:"))
    while index < start or index >= len(list):
        print("Input range({}, {})".format(start, len(list)-1))
        print_list(list, start)
        index = int(input("Input index:"))
    return index

lab_member_obj = get_lab_member()
group_infos = lab_member_obj.lab_group_list
group_index = input_range(group_infos)
group_info = group_infos[group_index]
schedule = lab_member_obj.get_schedule(group_info)
day_index = input_range(schedule)
ms = make_summary(group_info,day_index)
ms.create_one_day_summary(day_index)