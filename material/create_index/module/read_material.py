from PyPDF2 import PdfFileReader
import os

class read_material:
    def __init__(self, reference_folder):
        self.reference_folder = reference_folder
        self.bullet_file = os.path.join(self.reference_folder, 'bullet_marks.txt')
        self.ignore_file = os.path.join(self.reference_folder, 'ignore.txt')
        self.titles = self.get_title_name()
        self.bullet_point_marks = self.get_marks(self.bullet_file)


    def get_title_name(self):
        path = os.path.join(self.reference_folder,'READMe.md')
        bullets_name = {}
        target = '<!-- title -!>'
        with open(path, 'r', encoding='utf-8') as f:
            now_text = f.read().split('\n')
            rule_index = now_text.index('## Rule')
            for now_data in now_text[rule_index:]:
                if target in now_data:
                    res = now_data.replace(' {}'.format(target),'').split(' ')[-1]
                    bullets_name[res] = []
        return bullets_name
    
    def get_marks(self, mark_file):
        with open(mark_file, 'r', encoding='utf-8') as f:
            return f.read().split('\n')
    
    def remove_ignore(self, str):
        it = str
        ignores = self.get_marks(self.ignore_file)
        for ignore in ignores:
            if ignore in it:
                it = it[len(ignore)+1:]
        return it

    def judge_title(self, now_text):
        target_name = ''
        for title in self.titles:
            if title in now_text:
                target_name = title
            return target_name, self.modify_title(now_text)
        return target_name, '' 
    
    def modify_title(self, txt):
        if len(txt) > 2:
            return txt[1:-1]
        elif len(txt) == 2:
            return txt[1]
        return ''

    def get_target_title_page(self, txt):
        pre_bullet  = False
        res = []
        for it in txt:
            it = self.remove_ignore(it)
            bullet_flag = False
            for bullet in self.bullet_points_marks:
                if bullet not in it:
                    continue
                bullet_flag = True
                res.append(it[it.index(bullet)+1:])
            if bullet_flag:
                pre_bullet = bullet_flag
                continue
            if pre_bullet and bullet_flag == False:
                res[-1] += it 
                continue 
            res.append(it)
        return res

    # Get data from slide pdf
    def get_contents_value(self, file_name):
        current_contents = self.titles.copy()
        with open(file_name,'rb') as f:
            reader = PdfFileReader(f)
            page_numbers = reader.getNumPages()
            for index in range(page_numbers):
                now_text = reader.getPage(index).extract_text().split('\n')
                target_name, now_text = self.judge_title(now_text)
                if target_name == '':
                    continue
                current_contents[target_name] = self.get_target_title_page(now_text)
        return current_contents
    