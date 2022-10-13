import os
import datetime
import shutil
from pathlib import Path
import locale
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from io import StringIO

# locale.setlocale(locale.LC_TIME,'ja_JP.UTF-8')
schedule_path = 'schedule.txt'
out_folder = r'Summary\late'
template = [str(x) for x in Path('Summary').glob('*month_day*.txt')]
target_day = datetime.datetime(2022,7,26)
week_days = ['月','火','水','木','金','土','日']

today = datetime.datetime.today()

with open('bullet_marks.txt', 'r', encoding='utf-8') as f:
    bullet_points_marks = f.read().split('\n')

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
        
        people_data,counter = get_personal_data(group_folder,day,write_order)
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
    # return 

def get_txt_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        order = f.read().split('\n')
    return order

def get_order_data(path):
    res = {}
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
    end_index = 0
    with open(file_name,'rb') as f:
        resource_manager = PDFResourceManager()
        output = StringIO()
        LapPrams = LAParams()
        text_converter = TextConverter(resource_manager, output, laparams=LapPrams)
        page_interpreter = PDFPageInterpreter(resource_manager,text_converter)
        for index,now in enumerate(PDFPage.get_pages(f)):
            end_index = index
        for index,now in enumerate(PDFPage.get_pages(f)):
            if index == 1 or index == end_index:
                page_interpreter.process_page(now)
        output_text = output.getvalue()
        output.close()
        text_converter.close()
    now_content_index = 0
    for contents in output_text.split('\n'):
        if contents == str(end_index):
            break
        elif len(contents) == 0:
            continue
        elif contents == '1':
            now_content_index += 1
        elif contents[0] in bullet_points_marks:
            current_contents[now_content_index].append(contents[1:])
    return current_contents


if __name__ == '__main__':
    create_summary(template[0])