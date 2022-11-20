import os
import datetime
from pathlib import Path
from PyPDF2 import PdfFileReader
import shutil
import pandas as pd
import re

week_days = ['月','火','水','木','金','土','日']

# 個人の状況に合わせて変更する箇所
out_folder = 'out'
reference_folder = '.'
pdf_folder = 'pdf'
template = [str(x) for x in Path(reference_folder).glob('*month_day*.txt')]

my_group_info = ['lab_name','group_name']

# 今日の日付から前後6日間を今週の資料と見なして出力
today = datetime.datetime.today()
pre_week_day  = today-datetime.timedelta(days=6)
next_week_day = today+datetime.timedelta(days=6)
sep_date = datetime.datetime(2022,10,19,0,0)

# 出力用フォルダーの作成
if os.path.exists(out_folder) != True:
    os.mkdir(out_folder)

# 箇条書のリストの取得
with open(os.path.join(reference_folder,'bullet_marks.txt'), 'r', encoding='utf-8') as f:
    bullet_points_marks = f.read().split('\n')

# 無視する単語の取得
with open(os.path.join(reference_folder,'ignore.txt'), 'r', encoding='utf-8') as f:
    ignores = f.read().split('\n')

# 議事録のテンプレートを取得
def get_template():
    template_path = 'year_month_day.txt'
    template_summary = []
    with open(template_path, 'r', encoding='utf-8') as f:
        file_text = f.read().split('\n')
        base_sets = [[0,1],[1,2], [6,len(file_text)]]
        for i in range(len(base_sets)):
            for j in range(base_sets[i][0],base_sets[i][1]):
                template_summary.append('{}\n'.format(file_text[j]))
            if i == len(base_sets)-1:
                continue
            for j in range(base_sets[i][1],base_sets[i+1][0]):
                template_summary.append('{}'.format(file_text[j]))
    return template_summary

# 編集者の名前を消した議事録のファイル名の生成
def today_summary_file(day,group_name):
    return '{}_{:0>2}_{:0>2}_{}.txt'.format(str(day.year),str(day.month),str(day.day),group_name)

'''
pdf/20221010
のように班員の資料が保存されたフォルダがあるのでそれを作るための準備
'''
def today_summary_folder(day):
    return '{:0>4}{:0>2}{:0>2}'.format(str(day.year),str(day.month),str(day.day))

# 議事録に作成者の名前があるファイルの生成
def add_editor_name(day,group_name, person_name):
    return '{}_{:0>2}_{:0>2}_{}_{}.txt'.format(str(day.year),str(day.month),str(day.day),person_name,group_name)

# outからpdfに議事録のファイルを移動する
def move_pre_summary(group_folder, file_name, day):
    summary_folder = today_summary_folder(day)
    from_path = os.path.join(group_folder,file_name)
    to_path = os.path.join('pdf',summary_folder,file_name)
    if os.path.exists(to_path):
        return True
    elif os.path.exists(from_path) != True:
        return True
    print('{} => {}'.format(from_path,to_path))
    shutil.move(from_path,to_path)

# 研究室のメンバーを分類
# 研究室 > 班 > 学年
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

# member.xlsxから研究室名と班名の対応リストを取得する
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

# 議事録を編集する順番を取得する
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

# ある班のゼミに参加する人を取得する
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
    return participants

# ある班のゼミを行うスケジュールの情報を取得する
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

# 書き出す項目を決めた後のデータの取得
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
            person_data[target_name] = get_current_page(now_text, bullet_points_marks)
    return person_data

# ページの情報の取得
def get_current_page(lines, bullet_points_marks):
    res = []
    pre_bullet = False
    for it in lines:
        it = remove_ignore(it)
        bullet_flag = is_numeric_bullet(it)
        if bullet_flag:
            res.append(it)
            pre_bullet = bullet_flag
            continue
        for bullet in bullet_points_marks:
            if bullet not in it:
                continue
            bullet_flag = True
            input_data = it[it.index(bullet)+1:]
            if input_data in res:
                continue
            res.append(input_data)
        if bullet_flag:
            pre_bullet = bullet_flag
            continue
        if pre_bullet and bullet_flag == False:
            res[-1] += it
            if res.count(res[-1]) > 1:
                res.pop()
            continue 
        if it in res:
            continue
    return res

# 数字の箇条書であるか判定
def is_numeric_bullet(current_str):
    return re.compile(r"\d+\. ").match(current_str) != None

# ルールを決める前のスライドからの情報の取得
def get_old_contents_value(file_name):
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
                for ignore in  ignores:
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
    return current_contents

# 無視する言葉の除去
def remove_ignore(str):
    it = str
    for ignore in ignores:
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

# 記載する項目の取得
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

# 基本情報の記述
def write_basic_info(template,group_info,day,edit_name,all_lab_member,announcements):
    template[0] = template[0].replace('group_name', group_info[1])
    template[1] = template[1].replace('year',str(day.year)).replace('month',str(day.month)).replace('day',str(day.day))
    template[2] += "{}曜日\n".format(week_days[day.weekday()])
    template[3] += "{}:{:0>2}\n".format(day.hour,day.minute)
    template[4] += "{}\n".format(edit_name)
    template[5] += "{}\n".format(get_participant(group_info,day,all_lab_member))
    print(template)
    target_word = "班全体に対する連絡事項\n"
    start = template.index(target_word)+1
    for index in range(len(announcements)):
        if index + start >= len(template):
            template.append("{}\n".format(announcements[index]))
        else:
            template[index+start] = "{}\n".format(announcements[index])
    template.append("\n")
    return template

# 作成した議事録から全体への連絡事項を取得する
def get_announcements(file_name,names):
    target_word = "班全体に対する連絡事項"
    summary_data = open(file_name, 'r', encoding='utf-8').read().split("\n")
    start = summary_data.index(target_word)+1
    res = []
    flag = True
    while(start < len(summary_data) and flag == True):
        if summary_data[start] == "" or summary_data[start] in names:
            flag = False
        else:
            res.append(summary_data[start])
        start += 1
    return res

def count_tab(str):
    cnt = 0
    if len(str) == 0:
        return cnt
    flag = True
    while(flag and cnt < len(str)):
        if str[cnt] == '\t':
            cnt += 1
        else:
            flag = False
    return cnt

# 記述のある議事録から情報を取得する
def get_summary_contents(file_name, member_data):
    current_summary = open(file_name,'r',encoding='utf-8').read().split('\n')
    current_index = current_summary.index(next(iter(member_data)))
    current_name  = ""
    current_title = member_data[next(iter(member_data))].popitem()[0]
    member_data[next(iter(member_data))][current_title] = []

    for content in current_summary[current_index:]:
        cnt = count_tab(content)
        if cnt == 0 and content in member_data:
            current_name = content
        elif cnt == 1 and content[1:] in member_data[current_name]:
            current_title = content[1:]
        else:
            member_data[current_name][current_title].append(content[cnt:])
    return member_data

# 過去に作成した議事録との比較を行う
def compare_summary(person_summary, person_data):
    for bullet_name in person_summary:
        if len(person_data[bullet_name]) == 0:
            continue
        current_data = person_summary[bullet_name]
        for content in person_data[bullet_name]:
            if content in current_data:
                continue
            person_summary[bullet_name].append(content)
    return person_summary

# 議事録に書き出す項目をルール化した後の議事録に各情報の取得
def get_member_data(pdf_folder,day,names,group_info,edit_name):
    today_folder = os.path.join(pdf_folder,"{:0>4}{:0>2}{:0>2}".format(day.year,day.month,day.day))
    summary_file_name = os.path.join(out_folder, today_summary_file(day,group_info[1]))
    edit_summary      = os.path.join(out_folder, add_editor_name(day,group_info[1],edit_name))
    member_data = {}
    bullet_names = get_bullet_name()
    for name in names:
        member_data[name] = {}
        for bullet_name in bullet_names:
            member_data[name][bullet_name] = []
    pdf_counter = 0
    current_summary = member_data.copy()
    if os.path.exists(summary_file_name) == True:
        current_summary = get_summary_contents(summary_file_name,member_data)
    elif os.path.exists(edit_summary):
        current_summary = get_summary_contents(edit_summary,member_data)
    for name in names:
        for now_file in Path(today_folder).glob('{}*.pdf'.format(name)):
            pdf_counter += 1
            member_data[name] = get_contents_value(now_file,member_data[name])
            member_data[name] = compare_summary(current_summary[name],member_data[name])
    return member_data,pdf_counter

# ルールを決める前の議事録に書く情報の取得
def get_old_member_data(day,names,group_info,edit_name):
    today_folder = os.path.join(pdf_folder,"{:0>4}{:0>2}{:0>2}".format(today.year,today.month,today.day))
    member_data = {}
    summary_file_name = os.path.join(out_folder,today_summary_file(day,group_info[1]))
    edit_summary      = os.path.join(out_folder,add_editor_name(day,group_info[1],edit_name))
    pdf_counter = 0
    for name in names:
        member_data[name] = {'進捗報告':[''],'今後の予定':[''],'外部調査':['']}
    current_summary = member_data.copy()
    if os.path.exists(summary_file_name) == True:
        current_summary = get_summary_contents(summary_file_name, member_data)
    elif os.path.exists(edit_summary) == True:
        current_summary = get_summary_contents(edit_summary, member_data)
    for name in names:
        for now_file in Path(today_folder).glob('{}*.pdf'.format(name)):
            pdf_counter += 1
            each_data = get_old_contents_value(now_file)
            member_data[name]['進捗報告'] = each_data[0]
            member_data[name]['今後の予定'] = each_data[1]
            member_data[name]['外部調査'] = []
            member_data[name] = compare_summary(current_summary[name], member_data[name])
    return member_data,pdf_counter

# 議事録に出力する形に変換
def create_summary_text(current_summary, names, member_data):
    for name in names:
        current_summary.append("{}\n".format(name))
        for title in member_data[name]:
            current_data = member_data[name][title]
            current_summary.append("\t{}\n".format(title))
            if len(current_data) == 0:
                current_summary.append("\t\n")
            for content in current_data:
                current_summary.append("\t\t{}\n".format(content))
    return current_summary

# 議事録を作る
def create_summary(group_info):
    template_summary = get_template()
    group_folder = out_folder
    group_pdf_folder = pdf_folder
    all_lab_member = get_lab_member(today)
    schedule = get_schedule(group_info)
    edit_order = get_edit_order(group_info,all_lab_member)
    for day_index,day in enumerate(schedule):
        summary_file_name = today_summary_file(day,group_info[1])
        edit_summary = add_editor_name(day,group_info[1],edit_order[day_index%len(edit_order)])
        if next_week_day < day or pre_week_day > day:
            move_pre_summary(group_folder,summary_file_name,day)
            move_pre_summary(group_folder,edit_summary,day)
            continue
        summary_file = os.path.join(group_folder,edit_summary)
        announcements = []
        if os.path.exists(summary_file_name) == True:
            announcements = get_announcements(summary_file_name,edit_order)
        elif os.path.exists(edit_summary) == True:
            announcements = get_announcements(edit_summary,edit_order)
        elif os.path.exists(summary_file) == True:
            announcements = get_announcements(summary_file, edit_order)
        current_summary_text = write_basic_info(template_summary,group_info,day,edit_order[day_index%len(edit_order)],all_lab_member,announcements)
        if day > sep_date:
            member_data,counter = get_member_data(group_pdf_folder,day,edit_order,group_info,edit_order[day_index%len(edit_order)])
        else:
            member_data,counter = get_old_member_data(group_pdf_folder,day,edit_order,group_info,edit_order[day_index%len(edit_order)])
        if counter == 0:
            continue
        current_summary_text = create_summary_text(current_summary_text,edit_order,member_data)
        print('output file : ',summary_file)
        with open(summary_file,'w',encoding='utf-8') as f:
            f.writelines(current_summary_text)


if __name__ == '__main__':
    # 研究室，研究班
    create_summary(my_group_info)
