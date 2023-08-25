import shutil
from pathlib import *
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


def get_file_path_list(dir_path, file_types=['*.bin']):
    file_path_list = [file
                 for file_type in file_types
                 for file in Path(dir_path).rglob(file_type)]
    file_path_list = sorted(list(file_path_list))

    return file_path_list


def parse_file_path(dir_path, file_path):
    relative_path = file_path.relative_to(dir_path)
    path_components = relative_path.parts

    return path_components


def get_components(df):
    df_filled = df.fillna('')
    for index, row in df_filled.iterrows():
        for col in df_filled.columns:
            if isinstance(row[col], str) and '.bin' in row[col]:
                df_filled.at[index, col] = str(df.at[index, col]).split('_')[0]

    deduplicated_df = df_filled.groupby(0).apply(deduplicate_columns).reset_index(drop=True)
    deduplicated_df = deduplicated_df.applymap(lambda x: ', '.join(x))
    deduplicated_df.to_csv('result_deduplicated.csv', index=False)

    return deduplicated_df


def deduplicate_columns(group):
    deduplicated_group = group.apply(lambda col: col.drop_duplicates().tolist(), axis=0)
    return deduplicated_group


def get_ajusted_file_path(dir_path, df, column_order):
    # column_order = input('输入列号定义文件层级(例如 /0/1/2/4_5)：')
    symbols = [column_order[i] for i in range(len(column_order)) if i%2==0]
    numbers = [int(column_order[j]) for j in  range(len(column_order)) if j%2!=0]
    df = df.reindex(columns=numbers)
    df_list = df.values.tolist()
    path_list = [''.join([symbol + component for component, symbol in zip(components, symbols)]) for components in df_list]
    ajusted_file_path_list = [dir_path + '_ajusted' + path for path in path_list]

    return ajusted_file_path_list


def ajust_folder_level(original_path_list, ajusted_path_list):
    for ajusted_path in ajusted_path_list:
        folder_path = Path(ajusted_path).parent
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
    for original_path, ajusted_path in zip(original_path_list, ajusted_path_list):
        shutil.copyfile(original_path, ajusted_path)
        print(f'{ajusted_path} copy sccessful!')


def rename_file(replace_mapping, dir_path):
    file_path_list = get_file_path_list(dir_path)
    new_file_path_list = []

    for file_path in file_path_list:
        if file_path.is_file():
            filename = file_path.name

            for old_part, new_part in replace_mapping.items():
                if old_part in filename:
                    new_filename = filename.replace(old_part, new_part)
                    new_file_path = file_path.with_name(new_filename)
                    relative_path = new_file_path.relative_to(dir_path)
                    new_file_path = dir_path + '_renamed/' + str(relative_path)
                    new_file_path_list.append(new_file_path)

    ajust_folder_level(file_path_list, new_file_path_list)


def read_events_from_bin(filename):
    dtype = np.dtype([('x', 'u4'), ('y', 'u4'), ('p', 'u4'), ('t', 'u4')])
    with open(filename, "rb") as file:
        first_bytes = file.read(16)
        file.seek(-16, 2)
        last_bytes = file.read(16)
    data = np.frombuffer(first_bytes + last_bytes, dtype)
    events = make_structured_array(data['x'], data['y'], data['t'], data['p'])

    return events


def make_structured_array(x, y, t, p):
    events_struct = [("x", np.uint16), ("y", np.uint16), ("t", np.uint64), ("p", bool)]
    """
    Make a structured array given lists of x, y, t, p

    Args:
        x: List of x values
        y: List of y values
        t: List of times
        p: List of polarities boolean
    Returns:
        xytp: numpy structured array
    """
    return np.fromiter(zip(x, y, t, p), dtype=events_struct)


def get_duration(dir_path):
    file_path_list = get_file_path_list(dir_path)
    duration_info = []

    for file_path in file_path_list:
        project = parse_file_path(dir_path, file_path)[0]
        events = read_events_from_bin(file_path)
        startTime = events[0][2]
        endTime = events[1][2]
        duration = endTime - startTime
        print(project, duration)
        duration_info.append([project, duration])

    df_duration = pd.DataFrame(duration_info, columns=['project', 'duration'])
    df_duration.to_csv('result.csv', index=False)


def anaylze_result():
    df1 = pd.read_csv('result/result1.csv')
    df2 = pd.read_csv('result/result2.csv')

    df = pd.concat([df1,df2], ignore_index=True)
    df['duration'] = (df['duration'] / 1000000 / 3600).round(2)
    mean = df['duration'].mean()
    std = df['duration'].std()
    outlier_threshold = 3  # 可调整的阈值
    df_cleaned = df[(df['duration'] > mean - outlier_threshold * std) & (df['duration'] < mean + outlier_threshold * std)]
    group_project = df_cleaned.groupby('project')['duration'].sum().reset_index()
    total_duration = pd.DataFrame({'project': ['Total'],  'duration': df_cleaned['duration'].sum()})
    result = pd.concat([group_project, total_duration], ignore_index=True)
    result.to_csv("project_duration.csv", header=True)


def visualize_result(csv_file):
    result = pd.read_csv(csv_file, usecols=range(1,3))
    plt.figure(figsize=(20, 6))
    result = sns.barplot(x='project', y='duration', data=result)
    plt.title('Duration by Project')
    plt.xlabel('Project')
    plt.ylabel('Duration(h)')
    plt.xticks(rotation=45, ha='right')
    for p in result.patches:
        result.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center',
                    fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

    plt.tight_layout()
    plt.savefig('result.png')
    plt.show()


def main():
    dir_path = '/home/zhaojiayin/workspace/data/database/Backup_data/DVS/Gesture_control/data/speck-2f/20230418'

    file_path_list = get_file_path_list(dir_path)
    path_components_list = []

    for file_path in file_path_list:
        path_components = parse_file_path(dir_path, file_path)
        path_components_list.append(path_components)

    df_components = pd.DataFrame(path_components_list)
    df_components.to_csv('result.csv', index=False)

    '''获取文件层级要素'''
    get_components(df_components)

    # '''调整文件层级'''
    # ajusted_file_path_list = get_ajusted_file_path(dir_path, df_components)
    # ajust_folder_level(file_path_list, ajusted_file_path_list)
    #
    # '''修改文件名'''
    # replace_mapping = {
    #     'c01':'c0001'
    # }
    # rename_file(replace_mapping, dir_path)


if __name__ == '__main__':
    main()
    # get_duration(dir_path = '/run/user/1001/gvfs/smb-share:server=192.168.8.162,share=liuyuhang/data/DVS/Projects/BMW_PoC')
    # anaylze_result()
    # visualize_result('project_duration.csv')


