import os
import datetime
from pathlib import Path
import shutil
from .get_lab_data import GetLabData

class ReadSummary:
    def __init__(self, group_info, day, reference_folder=".", zemi_folder="."):
        self.group_info = group_info
        self.day = day
        self.reference_folder = reference_folder
        self.zemi_folder = zemi_folder
        self.template = self.get_template()
        self.LabData = GetLabData(group_info,day,reference_folder)
        self.out_folder = self.LabData.out_folder
        self.pdf_folder = self.LabData.pdf_folder


    # 議事録のテンプレートを取得
    def get_template(self):
        template_path = os.path.join(self.reference_folder,"year_month_day.txt")
        template_summary = []
        with open(template_path, 'r', encoding='utf-8') as f:
            file_text = f.read().split('\n')
            base_sets = [[0,1],[1,2], [7,len(file_text)]]
            for i in range(len(base_sets)):
                for j in range(base_sets[i][0],base_sets[i][1]):
                    template_summary.append('{}\n'.format(file_text[j]))
                if i == len(base_sets)-1:
                    continue
                for j in range(base_sets[i][1],base_sets[i+1][0]):
                    template_summary.append('{}'.format(file_text[j]))
        return template_summary

    # 編集者の名前を消した議事録のファイル名の生成
    def today_summary_file(self, day=None):
        if day == None:
            day = self.day
        return '{}_{:0>2}_{:0>2}_{}.txt'.format(str(day.year),str(day.month),str(day.day),self.group_info[1])


    # 議事録に作成者の名前があるファイルの生成
    def add_editor_name(self, person_name, day=None):
        if day == None:
            day = self.day
        return '{}_{:0>2}_{:0>2}_{}_{}.txt'.format(str(day.year),str(day.month),str(day.day),person_name,self.group_info[1])
    
    def get_summary_file_name(self, person_name, day=None):
        if day == None:
            day = self.day
        file_names = [self.today_summary_file(day), self.add_editor_name(person_name,day)]
        folder_names = [self.out_folder, self.pdf_folder]
        day_folder = self.LabData.today_summary_folder(day)
        for folder_name in folder_names:
            current_folder = os.path.join(folder_name, day_folder)
            for file_name in file_names:
                res = os.path.join(current_folder, file_name)
                if os.path.exists(res) == True:
                    return res
        summary_folder = os.path.join(folder_names[0],day_folder)
        if os.path.exists(summary_folder) != True:
            os.makedirs(summary_folder)
        return os.path.join(summary_folder,file_names[0])

    def get_recorder_absence(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.read().split("\n")
            recorder_index = 4 # 議事録作成者
            absence_index = 6 # 欠席者
            recorder = lines[recorder_index].split(":")[1].replace(" ", "")
            absence_text = lines[absence_index].split(":")[1].replace(" ","")
            absence = []
            for name in absence_text.split(","):
                if name == "" or name == 'None' or name == None:
                    continue
                absence.append(name)                
            return recorder,absence


    # 作成した議事録から全体への連絡事項を取得する
    def get_announcements(self, file_name, names):
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

    # outからpdfに議事録のファイルを移動する
    def move_pre_summary(self, out_folder, pdf_folder, file_name):
        summary_folder = self.LabData.today_summary_folder()
        from_path = os.path.join(out_folder,file_name)
        to_path = os.path.join(pdf_folder,summary_folder,file_name)
        if os.path.exists(to_path):
            return True
        elif os.path.exists(from_path) != True:
            return True
        print('{} => {}'.format(from_path,to_path))
        shutil.move(from_path,to_path)

    # tabの数を数える
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

    # 記述のある議事録から情報を取得する
    def get_summary_contents(self, file_name, member_data):
        current_summary = open(file_name,'r',encoding='utf-8').read().split('\n')
        current_index = current_summary.index(next(iter(member_data)))
        current_name  = ""
        current_title = member_data[next(iter(member_data))].popitem()[0]
        member_data[next(iter(member_data))][current_title] = []

        for content in current_summary[current_index:]:
            cnt = self.count_tab(content)
            if cnt == 0 and content in member_data:
                current_name = content
            elif cnt == 1 and content[1:] in member_data[current_name]:
                current_title = content[1:]
            elif content[cnt:] != "":
                member_data[current_name][current_title].append(content[cnt:])
        return member_data    