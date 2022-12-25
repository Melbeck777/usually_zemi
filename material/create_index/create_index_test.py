from module.write_index import md_index
from module.write_index import write_index

group_info = ["Test1", "a"]
reference_folder = "."
zemi_folder = ".\\zemi"
extension = "md"
make = write_index(reference_folder, zemi_folder,extension,group_info)
make.write_index_file()
mi = md_index(reference_folder,zemi_folder,group_info)
mi.mark_to_pdf()