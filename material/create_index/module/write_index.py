import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
import pdfkit
import os
import datetime
from .setup_material import setup_material
from .make_index import make_index


class write_index:
    def __init__(self, reference_folder, zemi_folder, extension, group_info):
        self.make_index = make_index(reference_folder, zemi_folder)
        self.index_file = os.path.join(self.make_index.setup_material.index_folder, "index.{}".format(extension))
        self.extension = extension
        self.group_info = group_info

    def write_index_file(self):
        index_data = self.make_index.all_date_index(self.group_info)
        write_index_str = self.make_index.arrange_index(index_data)
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(write_index_str)

    
## mdのインデックスを作成し、pdf変換するクラス
class md_index:
    def __init__(self, reference_folder, zemi_folder, group_info):
        self.setup_material = setup_material(reference_folder, zemi_folder)
        self.file_name = os.path.join(self.setup_material.index_folder, "index.md")
        self.make_index = make_index(reference_folder, zemi_folder)
        self.index_data = self.make_index.all_date_index(group_info)
        self.index_str = self.make_index.arrange_index(self.index_data)

    def mark_to_html(self):
        style = HtmlFormatter(style='solarized-dark').get_style_defs('.codehilite')
        md = markdown.Markdown(extensions=['extra', 'codehilite'])
        body = md.convert(self.index_str)
        html = '<!doctype html><html lang="ja"><meta charset="UTF-8"><body>'
        html += '<style>{}</style>'.format(style)
        html += '''<style> table,th,td{
            border-collapse:collapse;
            border:1px solid #333;
            }</style> '''
        html += body+'</body></html>'
        return html

    def html_to_pdf(self, html:str,output_file_name):
        path_to_pdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_to_pdf)
        pdfkit.from_string(html,output_file_name,configuration=config)

    def mark_to_pdf(self):
        if os.path.exists(self.setup_material.index_folder) == False:
            os.makedirs(self.setup_material.index_folder)
        html = self.mark_to_html()
        self.html_to_pdf(html,self.file_name.replace('md','pdf'))