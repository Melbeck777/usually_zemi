import os
import datetime
from pathlib import Path
from PyPDF2 import PdfFileReader
import re
from .get_lab_data import get_lab_data

class read_material:
    def __init__(self, group_info, day, edit_name, reference_folder="."):
        self.group_info = group_info
        self.day        = day
        self.edit_name  = edit_name
        self.reference_folder = reference_folder
        self.lab_data   = get_lab_data(group_info,day,reference_folder)
        self.presenter  = self.lab_data.get_presenter()
        self.ignores    = self.get_ignores()
        self.pdf_folder = self.lab_data.pdf_folder
        self.out_folder = self.lab_data.out_folder
        self.bullet_marks = self.get_bullet_marks()
    
    def get_ignores(self):
        ignore_file = os.path.join(self.reference_folder, "ignore.txt")
        with open(ignore_file, "r", encoding="utf-8") as f:
            res = f.read().split("\n")
        return res

    def get_bullet_marks(self):
        bullet_marks_file = "../bullet_marks.txt"
        with open(bullet_marks_file, "r", encoding="utf-8") as f:
            res = f.read().split("\n")
        return res

        # 数字の箇条書であるか判定
    def is_numeric_bullet(self,current_str):
        return re.compile(r"\d+\. ").match(current_str) != None

    # 無視する言葉の除去
    def remove_ignore(self,str):
        it = str
        for ignore in self.ignores:
            if ignore in it:
                it = it[len(ignore)+1:]
        return it

    def remove_title_and_page_num(self, lines):
        if (len(lines) > 2):
            return lines[1:-1]
        elif len(lines) == 2:
            return lines[1]
        return lines
    
    # 箇条書があるかどうかの判定
    def judge_bullet_flag(self,it):
        for bullet in self.bullet_marks:
            if bullet not in it:
                continue
            return True, it[it.index(bullet)+1:]
        return False, it
    
    # ページの情報の取得
    def get_current_page(self, lines):
        res = []
        pre_bullet = False
        for it in lines:
            it = self.remove_ignore(it)
            bullet_flag = self.is_numeric_bullet(it)
            if bullet_flag:
                res.append(it)
                pre_bullet = bullet_flag
                continue
            bullet_flag, input_data = self.judge_bullet_flag(it)
            if input_data in res:
                continue
            if bullet_flag:
                res.append(input_data)
                pre_bullet = bullet_flag
                continue
            if pre_bullet and bullet_flag == False:
                res[-1] += it
                if res.count(res[-1]) > 1:
                    res.pop()
                continue
            if len(input_data) > 3:
                res.append(input_data)
        return res


    # 書き出す項目を決めた後のデータの取得
    def get_contents_value(self, file_name,person_data):
        with open(file_name,'rb') as f:
            reader = PdfFileReader(f, strict=False)
            page_numbers = reader.getNumPages()
            for index in range(page_numbers):
                now_text = reader.getPage(index).extract_text().split('\n')
                target_name = ''
                for title in person_data:
                    if title in now_text[0]:
                        target_name = title
                        now_text = self.remove_title_and_page_num(now_text)
                if target_name == '':
                    continue
                person_data[target_name] = self.get_current_page(now_text)
        return person_data

    # ルールを決める前のスライドからの情報の取得
    def get_old_contents_value(self, file_name):
        print(file_name)
        current_contents = [[] for i in range(2)]
        with open(file_name,'rb') as f:
            reader = PdfFileReader(f, strict=False)
            page_numbers = reader.getNumPages()
            indexes = [1,page_numbers-1]
            for index,i in enumerate(indexes):
                now_text = reader.getPage(i).extract_text().split('\n') 
                now_text = self.remove_title_and_page_num(now_text)
                current_contents[index] = self.get_current_page(now_text)
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
    def get_presenter_data(self):
        presenter_data = self.presenter
        pdf_counter = 0
        today_folder = os.path.join(self.pdf_folder, self.lab_data.today_summary_folder())
        for name in presenter_data:
            for now_file in Path(today_folder).glob("*{}*.pdf".format(name)):
                pdf_counter += 1
                presenter_data[name] = self.get_contents_value(now_file,presenter_data[name])
        return presenter_data,pdf_counter

    # ルールを決める前の議事録に書く情報の取得
    def get_old_presenter_data(self):
        presenter_data = {}
        pdf_counter = 0
        today_folder = os.path.join(self.pdf_folder, self.lab_data.today_summary_folder())
        for name in self.presenter:
            presenter_data[name] = {'進捗報告':[''],'今後の予定':[''],'外部調査':['']}
        for name in presenter_data:
            print(name)
            for now_file in Path(today_folder).glob("*{}*.pdf".format(name)):
                pdf_counter += 1
                each_data = self.get_old_contents_value(now_file)
                print("each_data, ",each_data)
                presenter_data[name]['進捗報告'] = each_data[0]
                presenter_data[name]['今後の予定'] = each_data[1]
                presenter_data[name]['外部調査'] = []
        return presenter_data,pdf_counter