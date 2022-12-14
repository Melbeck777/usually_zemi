import os
import datetime
import shutil
from pathlib import Path
import pandas as pd

class make_index:
    def __init__(self, reference_folder, zemi_folder):
        self.reference_folder = reference_folder
        self.schedule_file    = os.path.join(self.reference_folder,'schedule.txt') # zemi schedule
        self.zemi_folder      = zemi_folder
        self.template_folder  = os.path.join(self.zemi_folder, 'template')

    def get_schedule(self, group_info):
        schedule = []
        term = 0
        today = datetime.datetime.today()
        if today.month < 3:
            term = 1
        path = os.path.join(self.reference_folder,'{}_schedule.csv'.format(today.year-term))
        data = pd.read_csv(path)
        columns = data.columns
        for index,now_date in enumerate(data[columns[0]]):
            now = "{} {}".format(now_date, data[group_info[1]][index])
            today = datetime.datetime.strptime(now,'%Y/%m/%d %H:%M')
            schedule.append(today)
        return schedule

    def create_translate_folder(self,date):
        to_name = os.path.join(self.zemi_folder,'{}_{}'.format(date.month, date.day))
        if os.path.exists(to_name) == False:
            shutil.copytree(self.template_folder, to_name)
        return to_name

    def get_editor_name(self,path):
        return os.path.basename(path).split('_')[0]

    def translate_pptx(self, date):
        date_folder = self.create_translate_folder(date,self.zemi_folder)
        for ppt in Path(date_folder).glob('*.pptx'):
            editor_name = self.get_editor_name(ppt)
            to_name = os.path.join(date_folder, '{}_{:0>4}{:0>2}{:0>2}.pptx'.format(editor_name,date.year,date.month,date.day))
            if os.path.exists(to_name) == False:
                shutil.move(ppt,to_name)
                print('{} => {}'.format(ppt,to_name))
        return to_name.replace('pptx','pdf')
    