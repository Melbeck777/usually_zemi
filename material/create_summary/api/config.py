import os


class SystemConfig:
    setting_path = 'dbSetting.txt'
    db_set_list = []
    with open(setting_path, 'r', encoding='utf-8') as f:
        read = f.read().split('\n')
        for line in read:
            db_set_list.append(line.split(",")[1])
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(
        user=db_set_list[0],
        password=db_set_list[1],
        host=db_set_list[2],
        db_name=db_set_list[3]
    )

Config = SystemConfig
