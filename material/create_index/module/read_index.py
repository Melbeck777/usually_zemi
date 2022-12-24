import os
import datetime
from .setup_material import setup_material

class read_index:
    def __init__(self,reference_folder,zemi_folder):
        self.setup_material = setup_material(reference_folder, zemi_folder)
        self.index_file = os.path.join(self.setup_material.index_folder, "index.md")
        self.titles = self.setup_material.get_title_names()
        self.sep_date = datetime.datetime(2022,10,19,0,0)

    
    def is_title(self, line):
        for title in self.titles:
            if title in line:
                return True, title
        return False, ""
    
    def get_line_content(self, line):
        return line.split(" ")[-1]

    # Get data from index.md
    def get_each_day_contents(self):
        if os.path.exists(self.index_file) == False:
            return ""
        each_days_contents = {}
        with open(self.index_file,'r', encoding='utf-8') as f:
            index_str = f.read()
            row = index_str.split("\n")
            current_date = ""
            for line in row:
                if line[0] == "-":
                    current_date = line.split(' ')[1]
                    current = datetime.datetime.strptime(current_date, '%Y/%m/%d')
                    if self.sep_date < current:
                        each_days_contents[current_date] = {}
                    else:
                        each_days_contents[current_date] = []
                elif self.sep_date < current:
                    title_flag, tmp_title = self.is_title(line)
                    if title_flag:
                        current_title = tmp_title
                        each_days_contents[current_date][current_title] = []
                        continue
                    each_days_contents[current_date][current_title].append(self.get_line_content(line))
                else:
                    each_days_contents[current_date].append(self.get_line_content(line))
        return each_days_contents