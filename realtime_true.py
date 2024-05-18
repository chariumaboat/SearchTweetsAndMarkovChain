import requests
import json
import random
from pprint import pprint
import re
import sys
from util import generate_text, wakati, auth_api_v2, reverse_retranslation, retranslation


def get_new_data():
    base_url = 'https://search.yahoo.co.jp/realtime/api/v1/pagination?p='
    keyword = random.choice(["毒ワクチン", "人工地震", "酸化グラフェン", "反グローバリズム", "イルミナティ"])
    r = requests.get(f'{base_url}{keyword}')
    j = json.loads(r.text)
    data = j['timeline']['entry']
    return data


def save_json_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def merge_data(data, local_data):
    combined_data = list(data)
    for item in local_data:
        if item not in combined_data:
            combined_data.append(item)
    return combined_data


def read_local_data(path):
    with open(path, 'r') as file:
        local_data = json.load(file)
        return local_data


def clean_string(input_string):
    # ハッシュタグを削除
    cleaned_string = re.sub(r'#(\w+)', r'\1', input_string)
    # URLを削除
    cleaned_string = re.sub(r'https?://\S+', '', cleaned_string)
    # タブと特定の文字列を削除
    cleaned_string = cleaned_string.replace(
        '\tSTART', '').replace('\tEND', '').replace('＃', '')
    return cleaned_string


# ローカルから真実を取得
local_true = read_local_data("./realtime_data.json")
# 新しい真実を取得
new_true = get_new_data()
# 真実を合体
merge_data_json = merge_data(new_true, local_true)
# JSONデータをファイルに保存
save_json_to_file(merge_data_json, 'realtime_data.json')
tw_pre_json = read_local_data("./realtime_data.json")
true_txt_list = [clean_string(i['displayTextBody']) for i in tw_pre_json]
realtime_true_txt = ''.join(true_txt_list)
tweet_text = retranslation(generate_text(wakati(realtime_true_txt)))
# trim
tweet_text_140 = tweet_text[0:139]
print("-----Post Text trimmed to 140 characters-----")
print(len(tweet_text_140))
print(tweet_text_140)
# tweet
api = auth_api_v2(sys.argv[1])
try:
    post_tweet = api.create_tweet(text=tweet_text_140)
except Exception as e:
    print(e)
