from PyPDF2 import PdfFileReader
import os
from pathlib import Path
import pandas as pd
import shutil
import datetime

template_path = "C:/Python/tools/usualy_zemi/material/create_summary/pdf/Test1/a/20221128"
pdf_folder = "C:/Python/tools/usualy_zemi/material/create_summary/pdf/Test1/a"
schedule_path = "../schedule/Test1/2022_schedule.csv"
group = 'a'

def get_data(pdf_file):
    data = {'進捗報告':[],'今後の予定':[],'外部調査':[],'参考文献':[]}

    reader = PdfFileReader(pdf_file)
    page_numbers = reader.getNumPages()
    for it in range(page_numbers):
        now_text = reader.getPage(it).extract_text().split('\n')
        for title in data:
            if title in now_text[0]:
                data[title].append(now_text[1:len(now_text)-2])
    return data

def get_schedule():
    schedule = pd.read_csv(schedule_path, encoding='utf-8')
    res = []
    for index, element in enumerate(schedule['day']):
        if type(schedule[group][index]) is float:
            continue
        res.append(element)
    return res

def list_to_date(date_list):
    return datetime.datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))

def date_to_path_name(date):
    return "{}{:0>2}{:0>2}".format(date.year, date.month, date.day)

def date_list_to_path_name(date_list):
    date = list_to_date(date_list)
    return date_to_path_name(date)

def change_path_date(date_path):
    current_dir = os.path.join(pdf_folder, date_path)
    for file_path in Path(current_dir).glob("*"):
        if os.path.isdir(file_path):
            continue
        base_path = os.path.basename(file_path)
        base_non_ex = os.path.splitext(base_path)[0]
        splitted_path = base_non_ex.split("_")
        new_base_name = base_path.replace(splitted_path[1], date_path)
        new_path = os.path.join(current_dir, new_base_name)
        os.rename(file_path, new_path)
        print(new_base_name)

def create_test_folder():
    schedule = get_schedule()
    for date in schedule:
        date_path = date_list_to_path_name(date.split("/"))
        date_folder = os.path.join(pdf_folder, date_path)
        if os.path.exists(date_folder):
            continue
        shutil.copytree(template_path, date_folder)
        change_path_date(date_path)
        print(date_path)

def get_people_data():
    people_data = {}
    for now in Path().glob('*'):
        if os.path.isdir(now) == False:
            continue
        data = {'進捗報告':[],'今後の予定':[],'外部調査':[],'参考文献':[]}

        for pdf_file in Path(now).glob('*.pdf'):
            people_data[os.path.basename(pdf_file).split('_')[0]] = get_data(pdf_file)
    print(people_data)

if __name__ == "__main__":
    create_test_folder()
