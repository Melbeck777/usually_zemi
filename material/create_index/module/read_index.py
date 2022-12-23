import os
import datetime
from .setup_material import setup_material

class read_index:
    def __init__(self,reference_folder,zemi_folder):
        self.setup_material = setup_material(reference_folder, zemi_folder)

    # Get data from index.md
    def get_each_day_contents(self):
        each_days_contents = {}
        sep_date = datetime.datetime(2022,10,19,0,0)
        bullets = self.setup_material.get_bullet_name()
        with open(self.setup_material.index_file,'r', encoding='utf-8') as f:
            index_str = f.read()
            row = index_str.split('\n')
            current_date = ''
            for now in row:
                if now[0] == '-':
                    current_date = now.split(' ')[1]
                    current = datetime.datetime.strptime(current_date, '%Y/%m/%d')
                    current_bullet = ''
                    if sep_date < current:
                        each_days_contents[current_date] = {}
                    else:
                        each_days_contents[current_date] = []
                elif sep_date < current:
                    bullet_flag = False
                    for bullet in bullets:
                        if bullet in now:
                            current_bullet = bullet
                            each_days_contents[current_date][current_bullet] = []
                            bullet_flag = True
                            continue
                    if bullet_flag:
                        continue
                    each_days_contents[current_date][current_bullet].append(now.split(' ')[1])
                else:
                    each_days_contents[current_date].append(now.split(' ')[-1])
        return each_days_contents