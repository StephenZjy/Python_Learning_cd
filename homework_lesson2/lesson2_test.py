import os
import csv
import pandas as pd


def get_file(path, types='.csv'):
    file_list = []

    for roots, dirs, files in os.walk(path):
        for file in files:
            suffix = os.path.splitext(file)[-1]
            if types == suffix:
                file_list.append(os.path.join(roots, file))

    return sorted(file_list)


def parse_filename(file):
    filepath, _ = os.path.splitext(file)
    person, light_level, position, label = filepath.split('/')[-4:]

    return person, light_level, position, label


def get_filter_list(file_list, lights=[], positions=[], persons=[], labels=[]):
    filter_list = list(filter(lambda x: filter_by_attributes(x, lights, positions, persons, labels), file_list))
    return filter_list


def filter_by_attributes(filename, lights=[], positions=[], persons=[], labels=[]):
    person, light_level, position, label = parse_filename(filename)
    if lights:
        if light_level not in lights:
            return False
    if positions:
        if position not in positions:
            return False
    if persons:
        if person not in persons:
            return False
    if labels:
        if label not in labels:
            return False
    return True


def get_Dataframe(file):
    '''
    读取csv文件，按照classification_Time结构存入dataframe
    '''
    df_file = pd.read_csv(file)
    classification_Time = {'person': parse_filename(file)[0],
                           'classification': df_file['classification'],
                           'Time': df_file['endTime'] - df_file['startTime']}
    classification_Time = pd.DataFrame(classification_Time)

    data = pd.DataFrame(classification_Time.groupby(['person', 'classification']).sum())
    data = data.reset_index()

    return data


def main():
    path = './20211228'         ###  原文件路径

    value_dict = {}             ###  person对应的label和时间
    classification_Time = {}    ###  label对应的时间
    class_list = ['class0', 'class2', 'class3', 'class4', 'class5']  ### label种类

    file_list = get_file(path)
    filter_list = get_filter_list(file_list,  lights=['l01'], positions=['p04'])

    '''生成value_dict, 拿到person对应的label和时间'''
    for file in filter_list:
        for value in get_Dataframe(file).values:
            person = value[0]
            classification = 'class' + str(value[1])
            Time = value[2]

            if classification != 'class1':
                if person not in list(value_dict.keys()):
                    classification_Time = {}
                classification_Time.update({classification: Time})
                value_dict.update({person: classification_Time})

    '''将value_dict存为dataframe'''
    df_result = pd.DataFrame.from_dict(value_dict).transpose()
    df_result = df_result.loc[:, class_list]     ###  设置列名
    df_result.index.name = 'person'
    df_result.to_csv('result.csv', na_rep=0)     ###  缺失值设为0


if __name__ == '__main__':
    main()
