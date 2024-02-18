import base64

import requests
import yaml


def read_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def filter_config(config_data, keywords):
    return {key: value for key, value in config_data.items() if keywords in key}


def download_csv(api_url, api_key, output_file="results.csv"):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"文件下载成功，保存为 {output_file}")
    else:
        print(f"文件下载失败，状态码：{response.status_code}")
        print(response.text)

# 调用方法
# api_url = "http://192.168.2.202:5000/api/queries/41/results.csv"
# api_key = "RCnSbqcBUF6cPB9Qk0C2c5mO0DQ4HVcM2pkmwn45"
#
# download_csv(api_url, api_key)
