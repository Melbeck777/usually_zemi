import os
import datetime
from pathlib import Path
from PyPDF2 import PdfFileReader
import shutil
import pandas as pd
import re
import read_summary

class make_index:
    def __init__(self,group_info, day):
        self.group_info = group_info
        self.day = day
        self.read_summary = read_summary(self.group_info, self.day)
        self.bullet_names = self.get_bullet_name()
        self.template = self.read_summary.template
        self.out_folder = self.read_summary.out_folder
        self.pdf_folder = self.read_summary.pdf_folder
        self.week_days = ['月','火','水','木','金','土','日']
        self.schedule = self.read_summary.get_schedule()
        self.ignores = self.read_summary.get_ignores()
    
    # 数字の箇条書であるか判定
    def is_numeric_bullet(self,current_str):
        return re.compile(r"\d+\. ").match(current_str) != None

    # 無視する言葉の除去
    def remove_ignore(self,str):
        it = str
        for ignore in self.lab_names:
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
    def write_basic_info(self,edit_name,announcements):
        current_template = self.template
        current_template[0] = current_template[0].replace('group_name', self.group_info[1])
        current_template[1] = current_template[1].replace('year',str(self.day.year)).replace('month',str(self.day.month)).replace('day',str(self.day.day))
        current_template[2] += "{}曜日\n".format(self.week_days[self.day.weekday()])
        current_template[3] += "{}:{:0>2}\n".format(self.day.hour,self.day.minute)
        current_template[4] += "{}\n".format(edit_name)
        current_template[5] += "{}\n".format(self.read_summary.get_participant())
        target_word = "班全体に対する連絡事項\n"
        start = current_template.index(target_word)+1
        for index in range(len(announcements)):
            if index + start >= len(current_template):
                current_template.append("{}\n".format(announcements[index]))
            else:
                current_template[index+start] = "{}\n".format(announcements[index])
        current_template.append("\n")
        return current_template

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

    def create_one_day_summary(self, day_index):
        day = self.schedule[day_index]
        edit_order = self.read_summary.get_edit_order()
        summary_file_name = self.read_summary.get_summary_file_name(edit_order[day_index%len(edit_order)])
        
        announcements = self.read_summary.get_announcements(summary_file_name, edit_order)
        current_summary_text = self.write_basic_info(edit_order[day_index%len(edit_order)],self.read_summary.all_lab_member,announcements)
        if day > sep_date:
            member_data,counter = self.get_member_data(self.pdf_folder,edit_order,edit_order[day_index%len(edit_order)])
        else:
            member_data,counter = self.get_old_member_data(self.pdf_folder,edit_order,edit_order[day_index%len(edit_order)])
        print("{}\n{}".format(counter,member_data))
        if counter == 0:
            return 
        current_summary_text = self.create_summary_text(current_summary_text,edit_order,member_data)
        print('output file : ',summary_file_name)
        if os.path.exists(self.out_folder) == False:
            os.makedirs(self.out_folder)
        with open(summary_file_name,'w',encoding='utf-8') as f:
            f.writelines(current_summary_text)


    # 議事録を作る
    def create_summary(self):
        edit_order = self.read_summary.get_edit_order()
        for day_index,day in enumerate(self.schedule):
            summary_file_name = self.read_summary.summary_file_name(day,self.group_info[1])
            if next_week_day < day or pre_week_day > day:
                move_pre_summary(self.out_folder,summary_file_name,day)
                continue
            create_one_day_summary(day_index)