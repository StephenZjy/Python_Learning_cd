import os
import pandas as pd
from utils import *

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


def match_username(df, username):
    username_info = df[df['username'] == username]
    username = str(username_info['username'].values[0])
    password = str(username_info['password'].values[0])
    tel = str(username_info['tel'].values[0])
    email = str(username_info['email'].values[0])

    return username, password, tel, email


def update_csv(username, new_username, new_tel, new_email, new_password, csv_file='user_info.csv',
               is_change_password=False):
    df_info = read_csv(csv_file)
    mask = df_info['username'] == username
    if is_change_password:
        df_info.loc[mask, ['password']] = [new_password]
    else:
        df_info.loc[mask, ['username', 'tel', 'email']] = [new_username, new_tel, new_email]
    df_info.to_csv(csv_file, mode='w', header=True, index=False)
