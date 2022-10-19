import os
import datetime
from pathlib import Path
from PyPDF2 import PdfFileReader

schedule_path = 'schedule.txt'
out_folder = r'Summary\late'
template = [str(x) for x in Path('Summary').glob('*month_day*.txt')]
target_day = datetime.datetime(2022,7,26)
week_days = ['月','火','水','木','金','土','日']

today = datetime.datetime.today()
pre_week_day = today-datetime.timedelta(weeks=1)


with open('bullet_marks.txt', 'r', encoding='utf-8') as f:
    bullet_points_marks = f.read().split('\n')
with open('ignore.txt', 'r', encoding='utf-8') as f:
    ignores = f.read().split('\n')

def create_summary(path):
    base_sets = [[0,2], [5,10]]
    template_summary = []
    with open(path, 'r', encoding='utf-8') as f:
        file_text = f.read().split('\n')
        for i in range(2):
            for j in range(base_sets[i][0],base_sets[i][1]):
                template_summary.append('{}\n'.format(file_text[j]))
            if i == 1:
                continue
            for j in range(base_sets[i][1],base_sets[i+1][0]):
                template_summary.append('{}'.format(file_text[j]))
    base_path  = os.path.basename(path)
    group_name = os.path.splitext(base_path)[0].split('_')[3]
    group_folder = os.path.join('Summary',group_name)
    edit_order_path = os.path.join(group_folder,'edit_order.txt')
    edit_order, write_order = get_order_data(edit_order_path)
    schedule_path = os.path.join(group_folder,'schedule.txt')
    schedule = get_schedule(schedule_path)
    for day_index,day in enumerate(schedule):
        if today < day:
            continue
        edited_summary = os.path.join(group_folder,'{}_{:0>2}_{:0>2}_{}.txt'.format(day.year,day.month,day.day,group_name))
        if os.path.exists(edited_summary):
            continue
        summary_file = os.path.join(group_folder,'{}_{:0>2}_{:0>2}_{}_{}.txt'.format(day.year,day.month,day.day
                                        ,edit_order[day_index%len(edit_order)],group_name))
        current_summary_text = template_summary[:10].copy()
        current_summary_text[1] = current_summary_text[1].replace('month',str(day.month)).replace('day',str(day.day))
        current_summary_text[2] += ' {}\n'.format(week_days[day.weekday()]+'曜日')
        current_summary_text[3] += ' {}:{:0>2}\n'.format(day.hour,day.minute)
        current_summary_text[4] += '{}\n'.format(edit_order[day_index%len(edit_order)])
        
        # people_data,counter = get_personal_data(group_folder,day,write_order)
        people_data,counter = get_personal_data(group_folder,target_day,write_order)
        if counter == 0:
            continue
        for name in write_order:
            current_data = people_data[name]
            current_summary_text.append('{}\n'.format(name))
            for point in current_data:
                current_summary_text.append('\t{}\n'.format(point))
                for input_str in current_data[point]:
                    current_summary_text.append('\t\t{}\n'.format(input_str))
        with open(summary_file,'w',encoding='utf-8') as f:
            f.writelines(current_summary_text)

def get_order_data(path):
    edit_order = []
    with open(path,'r',encoding='utf-8') as f:
        read = f.read().split('\n')
        write_order = ['' for x in range(len(read))]
        for now in read:
            it = now.split(',')
            edit_order.append(it[0])
            write_order[int(it[1])] = it[0]
    return edit_order,write_order

def get_schedule(path):
    schedule = []
    with open(path,'r',encoding='utf-8') as f:
        for now in f.read().split('\n'):
            today = datetime.datetime.strptime(now,'%Y/%m/%d %H:%M')
            schedule.append(today)
    return schedule

def get_personal_data(group_folder,today,names):
    today_folder = os.path.join(group_folder,"{:0>4}{:0>2}{:0>2}".format(today.year,today.month,today.day))
    people_data = {}
    pdf_counter = 0
    for name in names:
        people_data[name] = {'進捗報告':[''],'今後の予定':[''],'外部調査':['']}
    for now_file in Path(today_folder).glob('*.pdf'):
        pdf_counter += 1
        personal_data = {}
        each_data = get_contents_value(now_file)
        personal_data['進捗報告'] = each_data[0]
        personal_data['今後の予定'] = each_data[1]
        personal_data['外部調査'] = ['']
        for name in names:
            if name in str(now_file):
                people_data[name] = personal_data
    return people_data,pdf_counter

def get_contents_value(file_name):
    current_contents = [[] for i in range(2)]
    with open(file_name,'rb') as f:
        reader = PdfFileReader(f)
        page_numbers = reader.getNumPages()
        indexes = [1,page_numbers-1]
        for index,i in enumerate(indexes):
            now_text = reader.getPage(i).extract_text().split('\n') 
            if len(now_text) > 2:
                now_text = now_text[1:-1]
            elif len(now_text) == 2:
                now_text = [now_text[1]]
            for it in now_text:
                for ignore in ignores:
                    if ignore in it:
                        it = it[len(ignore)+1:]
                bullet_flag = False
                for bullet in bullet_points_marks:
                    if bullet not in it:
                        continue
                    bullet_flag = True
                    current_contents[index].append(it[it.index(bullet)+1:])
                if bullet_flag:
                    continue
                current_contents[index].append(it)
        print(current_contents)
    return current_contents


if __name__ == '__main__':
    create_summary(template[0])