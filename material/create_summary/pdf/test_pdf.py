from PyPDF2 import PdfFileReader
import os
from pathlib import Path


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


people_data = {}
for now in Path().glob('*'):
    if os.path.isdir(now) == False:
        continue
    data = {'進捗報告':[],'今後の予定':[],'外部調査':[],'参考文献':[]}
    
    for pdf_file in Path(now).glob('*.pdf'):
        people_data[os.path.basename(pdf_file).split('_')[0]] = get_data(pdf_file)
print(people_data)

