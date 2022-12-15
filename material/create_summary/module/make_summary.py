import os
import datetime
from pathlib import Path
from PyPDF2 import PdfFileReader
import shutil
import pandas as pd
import re


class make_index:
    def __init__(self,group_info):
        self.group_info = group_info

    # 数字の箇条書であるか判定
    def is_numeric_bullet(self,current_str):
        return re.compile(r"\d+\. ").match(current_str) != None

    # 無視する言葉の除去
    def remove_ignore(self,str):
        it = str
        for ignore in ignores:
            if ignore in it:
                it = it[len(ignore)+1:]
        return it

    # 記載する項目の取得
    def get_bullet_name(self):
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
    def write_basic_info(self,template,group_info,day,edit_name,all_lab_member,announcements):
        template[0] = template[0].replace('group_name', group_info[1])
        template[1] = template[1].replace('year',str(day.year)).replace('month',str(day.month)).replace('day',str(day.day))
        template[2] += "{}曜日\n".format(week_days[day.weekday()])
        template[3] += "{}:{:0>2}\n".format(day.hour,day.minute)
        template[4] += "{}\n".format(edit_name)
        template[5] += "{}\n".format(get_participant(group_info,day,all_lab_member))
        target_word = "班全体に対する連絡事項\n"
        start = template.index(target_word)+1
        for index in range(len(announcements)):
            if index + start >= len(template):
                template.append("{}\n".format(announcements[index]))
            else:
                template[index+start] = "{}\n".format(announcements[index])
        template.append("\n")
        return template

    # 過去に作成した議事録との比較を行う
    def compare_summary(self,person_summary, person_data):
        for bullet_name in person_summary:
            if len(person_data[bullet_name]) == 0:
                continue
            current_data = person_summary[bullet_name]
            for content in person_data[bullet_name]:
                if content in current_data:
                    continue
                person_summary[bullet_name].append(content)
        return person_summary

    # 議事録に出力する形に変換
    def create_summary_text(self,current_summary, names, member_data):
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

    def create_one_day_summary(self,group_info, day_index):
        template_summary = get_template()
        group_folder = os.path.join(out_folder,group_info[0],group_info[1])
        group_pdf_folder = os.path.join(pdf_folder,group_info[0],group_info[1])
        all_lab_member = get_lab_member(today)
        day = get_schedule(group_info)[day_index]
        edit_order = get_edit_order(group_info,all_lab_member)
        summary_file_name = today_summary_file(day,group_info[1])
        edit_summary = add_editor_name(day,group_info[1],edit_order[day_index%len(edit_order)])
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
            print("run get_member_data")
            member_data,counter = get_member_data(group_pdf_folder,day,edit_order,group_info,edit_order[day_index%len(edit_order)])
        else:
            member_data,counter = get_old_member_data(group_pdf_folder,day,edit_order,group_info,edit_order[day_index%len(edit_order)])
        print("{}\n{}".format(counter,member_data))
        if counter == 0:
            return 
        current_summary_text = create_summary_text(current_summary_text,edit_order,member_data)
        print('output file : ',summary_file)
        if os.path.exists(group_folder) == False:
            os.makedirs(group_folder)
        with open(summary_file,'w',encoding='utf-8') as f:
            f.writelines(current_summary_text)


    # 議事録を作る
    def create_summary(self):
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
            create_one_day_summary(group_info,day_index)