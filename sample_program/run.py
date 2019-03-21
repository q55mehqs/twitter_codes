from twitters import timeline, user_timeline, tweet, favorite
from twitter_option import isAllCheck_or

from numpy import random
import re

from kaiseki import noum_check, lists_getter


def format_text(text):
    '''
    ツイートのURL等を削除する
    '''

    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub('RT', "", text)
    text=re.sub('お気に入り', "", text)
    text=re.sub('まとめ', "", text)
    text=re.sub(r'[!-~]', "", text)#半角記号,数字,英字
    text=re.sub(r'[︰-＠]', "", text)#全角記号
    text=re.sub('\n', " ", text)#改行文字

    return text


def random_maker(_list):
    return int(random.randint(0, (len(_list))))


PATH = "./id_kijun.log"
# 30分前のやつ
with open(PATH) as f:
    bef_id = f.read()

# acq = timeline(since_id=bef_id)
acq = timeline(count=200)

while True:
    rand = random.randint(0, len(acq))

    tweet_text = acq[rand]["text"]
    tweet_trim = format_text(tweet_text)

    # if acq[rand]["entities"]
    noum_aru = noum_check(tweet_trim)

    if noum_aru and (not isAllCheck_or(acq[rand], screen_name="Q55mEhQS")): #if noum_aru == True:
        break

print(tweet_trim)

youso_list = lists_getter(tweet_trim)


using_noum = []
using_adj = []
using_adv = []
using_joshi = []
using_aux = []
using_verv = []
# 使う名詞を選ぶ
use = youso_list[0][random_maker(youso_list[0])]
youso_list[0].remove(use) # 選択したやつを消す
using_noum.append(use)

while True:
    if (random.choice([True, False])) and (youso_list[1] == True): # 形容詞
        use = youso_list[1][random_maker(youso_list[1])]
        youso_list[1].remove(use)
        using_adj.append(use)
    
        if (random.choice([True, False])) and (youso_list[2] == True):
            use = youso_list[2][random_maker(youso_list[2])]
            youso_list[2].remove(use)
            using_adv.append(use)
        
    if youso_list[3] or youso_list[4]:
        route = random.randint(0, 2)
        if route == 0:
            pass
        elif route == 1:
            use = youso_list[4][random_maker(youso_list[4])]
            youso_list[4].remove(use)
            using_aux.append(use)

            if youso_list[5] and random.choice([True, False]):
                use = youso_list[5][random_maker(youso_list[5])]
                youso_list[5].remove(use)
                using_verv.append(use)
        else:
            use = youso_list[3][random_maker(youso_list[3])]
            youso_list[3].remove(use)
            using_joshi.append(use)
    
    if youso_list[0]:
        if random.choice([True, False]):
            use = youso_list[0][random_maker(youso_list[0])]
            youso_list[0].remove(use) # 選択したやつを消す
            using_noum.append(use)
        else:
            break
    else:
        break

word = ""

while using_noum:
    if using_adv:
        _use = using_adv[random_maker(using_adv)]
        using_adv.remove(_use)
        word += _use
    if using_adj:
        _use = using_adj[random_maker(using_adj)]
        using_adj.remove(_use)
        word += _use
    if using_noum:
        _use = using_noum[random_maker(using_noum)]
        using_noum.remove(_use)
        word += _use
    if using_joshi:
        _use = using_aux[random_maker(using_aux)]
        using_aux.remove(_use)
        word += _use
        if using_verv:
            _use = using_verv[random_maker(using_verv)]
            using_verv.remove(_use)
            word += _use
    if using_aux:
        _use = using_aux[random_maker(using_aux)]
        using_aux.remove(_use)
        word += _use

print(word)

# favorite(acq[rand]["id_str"])

# id_str = tweet("ばぬゆー%sやんないよ" % word)

# with open(PATH, mode="w") as f:
#     f.write(id_str)
