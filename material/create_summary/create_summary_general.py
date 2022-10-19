import os
import datetime
from pathlib import Path
from PyPDF2 import PdfFileReader
import shutil
import pandas as pd


out_folder = 'out'
reference_folder = '.'
pdf_folder = 'pdf'
template = [str(x) for x in Path(reference_folder).glob('*month_day*.txt')]
week_days = ['月','火','水','木','金','土','日']

today = datetime.datetime.today()
pre_week_day = today-datetime.timedelta(weeks=1)

if os.path.exists(out_folder) != True:
    os.mkdir(out_folder)

with open(os.path.join(reference_folder,'bullet_marks.txt'), 'r', encoding='utf-8') as f:
    bullet_points_marks = f.read().split('\n')
with open(os.path.join(reference_folder,'ignore.txt'), 'r', encoding='utf-8') as f:
    ignores = f.read().split('\n')

# テンプレートからデータを読み出す
def get_template():
    template_path = 'year_month_day.txt'
    base_sets = [[0,1],[1,2], [6,10]]
    template_summary = []
    with open(template_path, 'r', encoding='utf-8') as f:
        file_text = f.read().split('\n')
        for i in range(len(base_sets)):
            for j in range(base_sets[i][0],base_sets[i][1]):
                template_summary.append('{}\n'.format(file_text[j]))
            if i == len(base_sets)-1:
                continue
            for j in range(base_sets[i][1],base_sets[i+1][0]):
                template_summary.append('{}'.format(file_text[j]))
    return template_summary

def today_summary_file(day,group_name):
    return '{}_{:0>2}_{:0>2}_{}.txt'.format(str(day.year),str(day.month),str(day.day),group_name)

def today_summary_folder(day):
    return '{:0>4}{:0>2}{:0>2}'.format(str(day.year),str(day.month),str(day.day))

def add_editor_name(day,group_name, person_name):
    return '{}_{:0>2}_{:0>2}_{}_{}.txt'.format(str(day.year),str(day.month),str(day.day),person_name,group_name)

def move_pre_summary(group_folder, file_name, day):
    summary_folder = today_summary_folder(day)
    from_path = os.path.join(group_folder,file_name)
    to_path = os.path.join(group_folder,summary_folder,file_name)
    if os.path.exists(to_path):
        return True
    elif os.path.exists(from_path) != True:
        return True
    shutil.move(from_path,to_path)
    print('{} => {}'.format(from_path,to_path))

def create_summary(group_info):
    template_summary = get_template()
    group_folder     = join_dir(out_folder, group_info[1])
    group_pdf_folder = join_dir(pdf_folder, group_info[1])
    all_lab_member = get_lab_member(today)
    schedule = get_schedule(group_info)
    edit_order = get_edit_order(group_info,all_lab_member)
    for day_index,day in enumerate(schedule):
        summary_file_name = today_summary_file(day,group_info[1])
        edit_summary = add_editor_name(day,group_info[1],edit_order[day_index%len(edit_order)])
        if today < day or pre_week_day > day:
            move_pre_summary(group_folder,summary_file_name,day)
            move_pre_summary(group_folder,edit_summary,day)
            continue
        summary_file = os.path.join(group_folder,edit_summary)
        
        current_summary_text = template_summary[:10].copy()
        current_summary_text[0] = current_summary_text[0].replace('group_name',group_info[1])
        current_summary_text[1] = current_summary_text[1].replace('year',str(day.year)).replace('month',str(day.month)).replace('day',str(day.day))
        current_summary_text[2] += '{}\n'.format(week_days[day.weekday()]+'曜日')
        current_summary_text[3] += '{}:{:0>2}\n'.format(day.hour,day.minute)
        current_summary_text[4] += '{}\n'.format(edit_order[day_index%len(edit_order)])
        current_summary_text[5] += '{}\n'.format(get_participant(group_info,day,all_lab_member))
        people_data,counter = get_personal_data(group_pdf_folder,day,edit_order)
        if counter == 0:
            continue
        for name in edit_order:
            current_data = people_data[name]
            current_summary_text.append('{}\n'.format(name))
            for point in current_data:
                if len(current_data[point]) == 0:
                    continue
                current_summary_text.append('\t{}\n'.format(point))
                for input_str in current_data[point]:
                    current_summary_text.append('\t\t{}\n'.format(input_str))
        print('output file : ',summary_file)
        with open(summary_file,'w',encoding='utf-8') as f:
            f.writelines(current_summary_text)

def get_lab_member(day):
    term = 0
    if day.month < 3:
        term = 1
    input_xl = './member/{}_member.xlsx'.format(str(day.year-term))
    data = pd.read_excel(input_xl)
    # 研究室，研究班，学年，氏
    target_index = [9,11,0,1]
    columns = data.columns
    lab_member = {}
    for index, lab_name in enumerate(data[columns[target_index[0]]]):
        group_name = data[columns[target_index[1]]][index]
        degree = data[columns[target_index[2]]][index]
        person_name = data[columns[target_index[3]]][index]
        if lab_name in lab_member:
            if degree == '教員':
                if degree not in lab_member[lab_name]:
                    lab_member[lab_name][degree] = [person_name]
                else:
                    lab_member[lab_name][degree].append(person_name)
            elif degree == 'B3':
                if degree not in lab_member[lab_name]:
                    lab_member[lab_name][degree] = [[person_name,group_name]]
                else:
                    lab_member[lab_name][degree].append([person_name,group_name])
            elif group_name not in lab_member[lab_name]:
                lab_member[lab_name][group_name] = {}
                lab_member[lab_name][group_name][degree] = [person_name]
            elif degree not in lab_member[lab_name][group_name]:
                lab_member[lab_name][group_name][degree] = [person_name]
            else:
                lab_member[lab_name][group_name][degree].append(person_name)
        else:
            lab_member[lab_name] = {}
            if degree == '教員':
                lab_member[lab_name][degree] = [person_name]
            elif degree == 'B3':
                lab_member[lab_name][degree] = [person_name,group_name]
            elif group_name not in lab_member[lab_name]:
                lab_member[lab_name][group_name] = {}
                lab_member[lab_name][group_name][degree] = [person_name]
            elif degree not in lab_member[lab_name][group_name]:
                lab_member[lab_name][group_name][degree] = [person_name]
    return lab_member

def get_group(lab_name,all_lab_member):
    group_list = []
    for group_name in all_lab_member[lab_name]:
        if group_name == '教員' or group_name == 'B3':
            continue
        elif group_name in group_list:
            continue
        else:
            group_list.append([lab_name,group_name])
    return group_list

def get_edit_order(group_info,all_lab_member):
    lab_member = all_lab_member[group_info[0]]
    edit_order = []
    degree_order = {'D':[3,3], 'M':[2,2], 'B':[2,4]}
    group_member = lab_member[group_info[1]]
    for it in degree_order:
        for index in range(degree_order[it][0]):
            current_degree = it+str(degree_order[it][1]-index)
            if current_degree not in group_member:
                continue
            for person in group_member[current_degree]:
                edit_order.append(person)
    return edit_order

def get_participant(group_info,day,all_lab_member):
    lab_member = all_lab_member[group_info[0]]
    participants = lab_member['教員'][0]+'教授'
    for i in range(len(lab_member['教員'])-1):
        participants += ', {}'.format(lab_member['教員'][i+1])
    degree_order = {'D':[3,3], 'M':[2,2], 'B':[2,4]}
    group_member = lab_member[group_info[1]]
    for it in degree_order:
        for index in range(degree_order[it][0]):
            current_degree = it+str(degree_order[it][1]-index)
            if current_degree not in group_member:
                continue
            for person in group_member[current_degree]:
                participants += ', {}'.format(person)

    for b3 in lab_member['B3']:
        if b3[1] == group_info[1]:
            participants += ', {}'.format(b3[0])
        elif day.month < 11:
            participants += ', {}'.format(b3[0])
    return participants

def get_schedule(group_info):
    schedule = []
    term = 0
    today = datetime.datetime.today()
    if today.month < 3:
        term = 1
    path = '{}_schedule.csv'.format(today.year-term)
    data = pd.read_csv(path)
    columns = data.columns
    for index,now_date in enumerate(data[columns[0]]):
        now = "{} {}".format(now_date, data[group_info[1]][index])
        today = datetime.datetime.strptime(now,'%Y/%m/%d %H:%M')
        schedule.append(today)
    return schedule

def get_personal_data(pdf_folder,today,names):
    today_folder = os.path.join(pdf_folder,"{:0>4}{:0>2}{:0>2}".format(today.year,today.month,today.day))
    people_data = {}
    pdf_counter = 0
    bullet_names = get_bullet_name()
    for name in names:
        people_data[name] = {}
        for bullet_name in bullet_names:
            people_data[name][bullet_name] = []
    for now_file in Path(today_folder).glob('*.pdf'):
        person_name = os.path.basename(now_file).split('_')[0]
        pdf_counter += 1
        people_data[person_name] = get_contents_value(now_file,people_data[name])
    return people_data,pdf_counter

def get_contents_value(file_name,person_data):
    with open(file_name,'rb') as f:
        reader = PdfFileReader(f)
        page_numbers = reader.getNumPages()
        for index in range(page_numbers):
            now_text = reader.getPage(index).extract_text().split('\n')
            target_name = ''
            for title in person_data:
                if title in now_text[0]:
                    target_name = title
                    if len(now_text) > 2:
                        now_text = now_text[1:-1]
                    elif len(now_text) == 2:
                        now_text = [now_text[1]]
            if target_name == '':
                continue
            for it in now_text:
                it = remove_ignore(it)
                bullet_flag = False
                for bullet in bullet_points_marks:
                    if bullet not in it:
                        continue
                    bullet_flag = True
                    person_data[target_name].append(it[it.index(bullet)+1:])
                if bullet_flag:
                    continue
                person_data[target_name].append(it)
    return person_data

def remove_ignore(str):
    it = str
    for ignore in  ignores:
        if ignore in it:
            it = it[len(ignore)+1:]
    return it

def join_dir(first,second):
    res = os.path.join(first,second)
    if os.path.exists(first) != True:
        os.mkdir(first)
    if os.path.exists(res) != True:
        os.mkdir(res)
    return res    

def get_bullet_name():
    path = 'READMe.md'
    bullets_name = []
    target = '<!-- title -!>'
    with open(path, 'r', encoding='utf-8') as f:
        now_text = f.read().split('\n')
        rule_index = now_text.index('## Rule')
        for now_data in now_text[rule_index:]:
            if target in now_data:
                res = now_data.replace(' {}'.format(target),'').split(' ')[-1]
                bullets_name.append(res)
    return bullets_name

if __name__ == '__main__':
    all_lab_member = get_lab_member(today)
    group_infos = get_group('精密',all_lab_member)
    for group_info in group_infos:
        print(group_info)
        # 研究室，研究班
        create_summary(group_info)