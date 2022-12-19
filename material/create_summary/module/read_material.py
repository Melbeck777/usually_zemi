import os
import datetime
from pathlib import Path
from PyPDF2 import PdfFileReader
import pandas as pd

class read_material:
    def __init__(self, ):



    # 書き出す項目を決めた後のデータの取得
    def get_contents_value(self, file_name,person_data):
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
    def get_current_page(self, lines, bullet_points_marks):
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


    # ルールを決める前のスライドからの情報の取得
    def get_old_contents_value(self, file_name):
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

    def count_tab(self, str):
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


    # 議事録に書き出す項目をルール化した後の議事録に各情報の取得
    def get_member_data(self, pdf_folder,day,names,group_info,edit_name):
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
    def get_old_member_data(self, day,names,group_info,edit_name):
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