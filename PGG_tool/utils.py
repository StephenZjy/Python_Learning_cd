def save_data(data, filename):
    with open(filename, 'a+') as f:
        print(data)
        f.write(data+'\n')


def next_filename(filename):
    if '_' not in filename:
        return filename
    splits = filename.split('_')
    try:
        num_str = splits[-1]
        num = int(num_str)
    except:
        return filename
    num += 1
    len_num = len(num_str)
    num_str = str(num).zfill(len_num)
    splits[-1] = num_str
    filename = '_'.join(splits)
    return filename




