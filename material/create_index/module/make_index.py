import os
import datetime
import shutil
from pathlib import Path
import pandas as pd
from .setup_material import setup_material
from .read_material import read_material
from .read_index import read_index

TODAY = datetime.datetime.today()
class make_index:
    def __init__(self, reference_folder, zemi_folder):
        self.reference_folder = reference_folder
        self.zemi_folder = zemi_folder
        self.setup_material = setup_material(reference_folder, zemi_folder)
        self.read_material = read_material(reference_folder, zemi_folder)
        self.read_index = read_index(reference_folder, zemi_folder)
        self.current_index_data = self.read_index.get_each_day_contents()

    def get_today_material(self,folder):
        for name in Path(folder).glob("*.pdf"):
            return name

    def compare_title(self, index_data, material_data):
        res = index_data
        for line in material_data:
            if line not in res:
                res.append(line)
        return res

    def compare_current_date(self, date):
        current_date_line  = self.setup_material.today_name(date)
        date_pdf_folder = self.setup_material.make_today_folder(date)
        file_name = self.get_today_material(date_pdf_folder)
        material_data = self.read_material.get_contents_value(file_name)
        print(current_date_line)
        if current_date_line not in self.current_index_data:
            return material_data
        print(self.current_index_data[current_date_line])
        index_data = self.current_index_data[current_date_line]
        for title in material_data:
            if title not in index_data:
                index_data[title] = material_data[title]
                continue
            index_data[title] = self.compare_title(index_data[title], material_data[title])
        return index_data

    def all_date_index(self, group_info):
        schedule = self.setup_material.get_schedule(group_info)
        index_data = {}
        for date in schedule:
            if date > TODAY:
                return index_data
            today_name = self.setup_material.today_name(date)
            index_data[today_name] = self.compare_current_date(date)
        return index_data
    
    def write_date(self, date):
        to_date = datetime.datetime.strptime(date, "%Y%m%d")
        return "{}/{}/{}".format(to_date.year, to_date.month, to_date.day)

    def arrange_index(self, index_data):
        res_str = ""
        for date in index_data:
            res_str += "- {}\n".format(self.write_date(date))
            for title in index_data[date]:
                if len(index_data[date][title]) == 0:
                    continue
                res_str += "\t- {}\n".format(title)
                for line in index_data[date][title]:
                    res_str += "\t\t- {}\n".format(line)
        return res_str
