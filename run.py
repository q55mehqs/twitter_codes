from twitters import Twitter
from twitter_option import isAllCheck_or

from numpy import random
import re

from kaiseki import noum_check, lists_getter


twitter = Twitter()

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
    return _list[int(random.randint(0, (len(_list))))]


PATH = "./id_kijun.log"
# 30分前のやつ
with open(PATH) as f:
    bef_id = f.read()

acq = twitter.timeline(since_id=bef_id)
# acq = twitter.timeline(count=200)

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
use = random_maker(youso_list[0])
youso_list[0].remove(use) # 選択したやつを消す
using_noum.append(use)

while True:
    if (random.choice([True, False])) and (youso_list[1] == True): # 形容詞
        use = random_maker(youso_list[1])
        youso_list[1].remove(use)
        using_adj.append(use)
    
        if (random.choice([True, False])) and (youso_list[2] == True):
            use = random_maker(youso_list[2])
            youso_list[2].remove(use)
            using_adv.append(use)
        
    if youso_list[3] or youso_list[4]:
        route = random.randint(0, 2)
        if route == 0:
            pass
        elif route == 1:
            use = random_maker(youso_list[4])
            youso_list[4].remove(use)
            using_aux.append(use)

            if youso_list[5] and random.choice([True, False]):
                use = random_maker(youso_list[5])
                youso_list[5].remove(use)
                using_verv.append(use)
        else:
            use = random_maker(youso_list[3])
            youso_list[3].remove(use)
            using_joshi.append(use)
    
    if youso_list[0]:
        if random.choice([True, False]):
            use = random_maker(youso_list[0])
            youso_list[0].remove(use) # 選択したやつを消す
            using_noum.append(use)
        else:
            break
    else:
        break

word = ""

while using_noum:
    if using_adv:
        _use = random_maker(using_adv)
        using_adv.remove(_use)
        word += _use
    if using_adj:
        _use = random_maker(using_adj)
        using_adj.remove(_use)
        word += _use
    if using_noum:
        _use = random_maker(using_noum)
        using_noum.remove(_use)
        word += _use
    if using_joshi:
        _use = random_maker(using_aux)
        using_aux.remove(_use)
        word += _use
        if using_verv:
            _use = random_maker(using_verv)
            using_verv.remove(_use)
            word += _use
    if using_aux:
        _use = random_maker(using_aux)
        using_aux.remove(_use)
        word += _use

print(word)

# twitter.favorite(acq[rand]["id_str"])

# id_str = twitter.tweet("ばぬゆー%sやんないよ" % word)

# with open(PATH, mode="w") as f:
#     f.write(id_str)
