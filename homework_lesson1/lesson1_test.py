import os
import shutil


def get_file(path, types='.bin'):
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


def main():
    src_path = './20211223'         ### 原文件路径
    dst_path = './20211223_new'     ### 生成新文件的路径

    file_list = get_file(src_path)
    filter_list = get_filter_list(file_list, lights=['l01', 'l02', 'l04'], labels=['attentive'])

    for file in filter_list:
        person = parse_filename(file)[0]
        light = parse_filename(file)[1]
        position = parse_filename(file)[2]
        label = parse_filename(file)[3]
        path = os.path.join(dst_path, person, position, light)

        if not os.path.exists(path):
            os.makedirs(path)

        if os.path.exists(path):
            shutil.copyfile(os.path.abspath(file), os.path.join(path, label + '.bin'))


if __name__ == '__main__':
    main()
