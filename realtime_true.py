import requests
import json
import random
from pprint import pprint
import re
import sys
from util import *


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

if True:
    random_select_img()
    api = auth_api_v1(sys.argv[1])
    media_id = api.media_upload("dl.png").media_id_string
    api = auth_api_v2(sys.argv[1])
    try:
        post_tweet = api.create_tweet(
            text=tweet_text_140, media_ids=[media_id])
    except Exception as e:
        print(e)
else:
    api = auth_api_v2(sys.argv[1])
    try:
        post_tweet = api.create_tweet(text=tweet_text_140)
    except Exception as e:
        print(e)
