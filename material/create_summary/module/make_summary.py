import os
import datetime
from .get_lab_data import GetLabData
from .get_lab_data import GetLabMember
from .read_summary import ReadSummary
from .read_material import ReadMaterial

# 資料作成についてのルールを決めた日
SEP_DATE = datetime.datetime(2022,10,19)
TODAY = datetime.datetime.today()
ONE_WEEK_OFFSET = datetime.timedelta(weeks=1)

class MakeSummary:
    def __init__(self,group_info, day_index, year, reference_folder=".", sep_date=SEP_DATE): 
        self.LabMember = GetLabMember(year=year,reference_folder=reference_folder)
        self.schedule = self.LabMember.get_schedule(group_info) 
        self.day = self.schedule[day_index]
        self.sep_date = sep_date
        self.pre_week_day = TODAY-ONE_WEEK_OFFSET
        self.next_week_day = TODAY+ONE_WEEK_OFFSET
        self.LabData     = GetLabData(group_info,  self.day, reference_folder)
        self.group_info = self.LabData.group_info
        self.edit_order = self.LabData.get_edit_order()
        self.edit_name = self.edit_order[day_index%len(self.edit_order)]
        self.ReadSummary = ReadSummary(group_info,  self.day, reference_folder)
    
        self.ReadMaterial = ReadMaterial(group_info,self.day, self.edit_name, reference_folder)
        self.bullet_names = self.LabData.get_title_names()
        self.template   = self.ReadSummary.template
        self.out_folder = self.LabData.out_folder.format(self.group_info[1], self.day.year)
        self.pdf_folder = self.LabData.pdf_folder.format(self.group_info[1], self.day.year)
        self.week_days = ['月','火','水','木','金','土','日']
        self.ignores  = self.ReadMaterial.get_ignores()

    # 基本情報の記述
    def write_basic_info(self,announcements=[],recorder="", absence=[]):
        current_template = self.template
        current_template[0] = current_template[0].replace('group_name', self.group_info[1])
        current_template[1] = current_template[1].replace('year',str(self.day.year)).replace('month',str(self.day.month)).replace('day',str(self.day.day))
        current_template[2] += "{}曜日\n".format(self.week_days[self.day.weekday()])
        current_template[3] += "{}:{:0>2}\n".format(self.day.hour,self.day.minute)
        participant = self.LabData.get_participant(absence)
        if recorder == "":
            recorder = self.edit_name
        print("input absence", absence)
        current_template[4] += "{}\n".format(recorder)
        current_template[5] += "{}\n".format(participant)
        current_template[6] += "{}\n".format(self.member_arrange_to_text(absence))
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
    def compare_same_title_summary(self,person_summary, person_data):
        for bullet_name in person_summary:
            if bullet_name not in person_data:
                person_data[bullet_name] = []
                continue
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
        summary_file_name = self.ReadSummary.get_summary_file_name(self.edit_name)
        if day > self.sep_date:
            member_data,counter = self.ReadMaterial.get_presenter_data()
        else:
            member_data,counter = self.ReadMaterial.get_old_presenter_data()
        if counter == 0:
            return       
        if os.path.exists(summary_file_name) == True:
            past_summary = self.ReadSummary.get_summary_contents(summary_file_name, self.LabData.get_presenter())
            member_data = self.compare_summary(past_summary, member_data)
            announcements = self.ReadSummary.get_announcements(summary_file_name, self.edit_order)
            current_summary_text = self.write_basic_info(announcements)
        else:
            current_summary_text = self.write_basic_info()
        current_summary_text = self.create_summary_text(current_summary_text,member_data)
        # print('output file : ',summary_file_name)
        if os.path.exists(self.out_folder) == False:
            os.makedirs(self.out_folder)
        with open(summary_file_name,'w',encoding='utf-8') as f:
            f.writelines(current_summary_text)

    def create_one_day_summary_edited(self, day_index, edit_summary, announcement, absence=[], recorder=None):
        day = self.schedule[day_index]
        print(self.schedule)
        current_edit_name = self.edit_order[day_index%len(self.edit_order)]
        summary_file_name = self.ReadSummary.get_summary_file_name(current_edit_name)
        print(summary_file_name)
        if day > self.sep_date:
            member_data,counter = self.ReadMaterial.get_presenter_data()
        else:
            member_data,counter = self.ReadMaterial.get_old_presenter_data()
        if counter == 0:
            return
        member_data = self.compare_summary(edit_summary, member_data)
        current_summary_text = self.write_basic_info(announcement,recorder=recorder, absence=absence)
        current_summary_text = self.create_summary_text(current_summary_text,member_data)
        # print('output file : ',summary_file_name)
        if os.path.exists(self.out_folder) == False:
            os.makedirs(self.out_folder)
        with open(summary_file_name,'w',encoding='utf-8') as f:
            f.writelines(current_summary_text)

    def member_arrange_to_text(self,member):
        txt = ""
        already_input = []
        for name in member:
            # print("name,",name,name == None, name == "")
            if name == None or name == "" or name in already_input:
                continue
            already_input.append(name)
            txt += "{}, ".format(name)
        # print("member, txt = {},{}".format(member,txt))
        return txt[:-2]
    
    # 議事録を作る
    def create_summary(self):
        for day_index,day in enumerate(self.schedule):
            summary_file_name = self.ReadSummary.summary_file_name(day,self.group_info[1])
            self.create_one_day_summary(day_index)
    