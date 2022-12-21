import os
import datetime
from .get_lab_data import get_lab_data
from .get_lab_data import get_lab_member
from .read_summary import read_summary
from .read_material import read_material

# 資料作成についてのルールを決めた日
SEP_DATE = datetime.datetime(2022,10,19)
TODAY = datetime.datetime.today()
ONE_WEEK_OFFSET = datetime.timedelta(weeks=1)

class make_summary:
    def __init__(self,group_info, day_index, sep_date=SEP_DATE):
        self.group_info = group_info
        self.lab_member = get_lab_member()
        self.schedule = self.lab_member.get_schedule(group_info) 
        self.day = self.schedule[day_index]
        self.sep_date = sep_date
        self.pre_week_day = TODAY-ONE_WEEK_OFFSET
        self.next_week_day = TODAY+ONE_WEEK_OFFSET
        self.lab_data     = get_lab_data(group_info,  self.day)
        self.edit_order = self.lab_data.get_edit_order()
        self.edit_name = self.edit_order[day_index%len(self.edit_order)]
        self.read_summary = read_summary(group_info,  self.day)
    
        self.read_material = read_material(group_info,self.day, self.edit_name)
        self.bullet_names = self.lab_data.get_title_names()
        self.template   = self.read_summary.template
        self.out_folder = self.lab_data.out_folder
        self.pdf_folder = self.lab_data.pdf_folder
        self.week_days = ['月','火','水','木','金','土','日']
        self.ignores  = self.read_material.get_ignores()
    
    # 基本情報の記述
    def write_basic_info(self,announcements=[]):
        current_template = self.template
        current_template[0] = current_template[0].replace('group_name', self.group_info[1])
        current_template[1] = current_template[1].replace('year',str(self.day.year)).replace('month',str(self.day.month)).replace('day',str(self.day.day))
        current_template[2] += "{}曜日\n".format(self.week_days[self.day.weekday()])
        current_template[3] += "{}:{:0>2}\n".format(self.day.hour,self.day.minute)
        current_template[4] += "{}\n".format(self.edit_name)
        current_template[5] += "{}\n".format(self.lab_data.get_participant())
        target_word = "班全体に対する連絡事項\n"
        start = current_template.index(target_word)+1
        for index in range(len(announcements)):
            if index + start >= len(current_template):
                current_template.append("{}\n".format(announcements[index]))
            else:
                current_template[index+start] = "{}\n".format(announcements[index])
        current_template.append("\n")
        return current_template
    
# 
    
    # 過去に作成した議事録との比較を行う
    def compare_same_title_summary(self,person_summary, person_data):
        for bullet_name in person_summary:
            if len(person_data[bullet_name]) == 0:
                continue
            current_data = person_summary[bullet_name]
            for content in person_data[bullet_name]:
                if content in current_data:
                    continue
                person_summary[bullet_name].append(content)
        return person_summary

    def compare_summary(self, past_summary, current_material):
        out_summary = {}
        for name in past_summary:
            out_summary[name] = self.compare_same_title_summary(past_summary[name], current_material[name])
        return out_summary
    
    # 議事録に出力する形に変換
    def create_summary_text(self,current_summary, member_data):
        for name in self.edit_order:
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
        summary_file_name = self.read_summary.get_summary_file_name(self.edit_name)
        if day > self.sep_date:
            member_data,counter = self.read_material.get_presenter_data()
        else:
            member_data,counter = self.read_material.get_old_presenter_data()
        if counter == 0:
            return       
        if os.path.exists(summary_file_name) == True:
            past_summary = self.read_summary.get_summary_contents(summary_file_name, self.lab_data.get_presenter())
            member_data = self.compare_summary(past_summary, member_data)
            announcements = self.read_summary.get_announcements(summary_file_name, self.edit_order)
            current_summary_text = self.write_basic_info(announcements)
        else:
            current_summary_text = self.write_basic_info()
        current_summary_text = self.create_summary_text(current_summary_text,member_data)
        print('output file : ',summary_file_name)
        print(current_summary_text)
        if os.path.exists(self.out_folder) == False:
            os.makedirs(self.out_folder)
        with open(summary_file_name,'w',encoding='utf-8') as f:
            f.writelines(current_summary_text)

    # 議事録を作る
    def create_summary(self):
        for day_index,day in enumerate(self.schedule):
            summary_file_name = self.read_summary.summary_file_name(day,self.group_info[1])
            if self.next_week_day < day or self.pre_week_day > day:
                self.read_summary.move_pre_summary(self.out_folder,summary_file_name,day)
                continue
            self.create_one_day_summary(day_index)