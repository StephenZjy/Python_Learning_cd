import os
import pandas as pd


def write_csv(data, csv_file='user_info.csv'):
    columns = ['username', 'password', 'tel', 'email']
    df_info = pd.DataFrame(data, columns=columns)
    if not os.path.exists(csv_file):
        df_info.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        df_info.to_csv(csv_file, mode='a', header=False, index=False)


def read_csv(csv_file='user_info.csv'):
    df_info = pd.read_csv(csv_file)
    return df_info

def update_csv()