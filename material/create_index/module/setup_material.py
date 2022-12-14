import os
import datetime
import shutil
from pathlib import Path
import pandas as pd

TODAY = datetime.datetime.today()
class setup_material:
    def __init__(self, reference_folder, zemi_folder):
        # 参照するファイルが入ってるディレクトリの親ファイル
        self.reference_folder = reference_folder
        self.zemi_folder      = zemi_folder
        self.template_folder  = os.path.join(self.reference_folder, "template")
        self.schedule_folder  = os.path.join(self.reference_folder, "schedule")
        self.index_folder     = os.path.join(self.reference_folder, "index")

    def get_term(self):
        if TODAY.month < 4:
            return 1
        return 0
    
    def get_title_names(self):
        readme  = os.path.join(self.reference_folder, "README.md")
        title_names = {}
        target_word = "<!-- title -!>"
        with open(readme, 'r', encoding='utf-8') as f:
            read = f.read().split("\n")
            rule_index = read.index("## Rule")
            for line in read[rule_index:]:
                if target_word in line:
                    key = line.replace(" {}".format(target_word),"").split(" ")[-1]
                    title_names[key] = {}
        return title_names
    
    def get_marks(self, file):
        if os.path.exists(file) == False:
            print("{} is not found".format(file))
            return ""
        with open(file, 'r', encoding='utf-8') as f:
            return f.read().split("\n")
    
    # group_info = [lab_name, group_name]
    def get_schedule(self, group_info):
        schedule = []
        term = self.get_term()
        path = os.path.join(self.schedule_folder,'{}_schedule.csv'.format(TODAY.year-term))
        data = pd.read_csv(path)
        columns = data.columns
        for index,now_date in enumerate(data[columns[0]]):
            now = "{} {}".format(now_date, data[group_info[1]][index])
            current_date = datetime.datetime.strptime(now,'%Y/%m/%d %H:%M')
            schedule.append(current_date)
        return schedule
    
    # file_path = {full name}_{date}.pptx
    def get_editor_name(self,path):
        return os.path.basename(path).split('_')[0]

    def today_name(self, date):
        return "{}{:0>2}{:0>2}".format(date.year,date.month,date.day)

    def make_today_folder(self,date):
        to_name = os.path.join(self.zemi_folder,self.today_name(date))
        # template フォルダのコピー
        if os.path.exists(to_name) == False:
            shutil.copytree(self.template_folder, to_name)
        return to_name
    
    def make_today_pptx(self, date):
        date_folder = self.make_today_folder(date)
        for ppt in Path(date_folder).glob('*.pptx'):
            editor_name = self.get_editor_name(ppt)
            to_name = os.path.join(date_folder, '{}_{}.pptx'.format(editor_name,self.today_name(date)))
            if os.path.exists(to_name) == False:
                # template の変更
                shutil.move(ppt,to_name)
                print('{} => {}'.format(ppt,to_name))
        return to_name.replace('pptx','pdf')
    
    