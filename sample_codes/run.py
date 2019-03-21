from twitters import Twitter

try:
    import tokens
    twitter = Twitter(tokens.CK, tokens.CS,
            tokens.AT, tokens.AS)
except ImportError:
    # tokensファイルを作成しない場合、
    # ここにキー、トークンを入力
    CK = ""
    CS = ""
    AT = ""
    AS = ""

    twitter = Twitter(CK, CS, AT, AS)

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

    if noum_aru and (not isAllCheck_or(acq[rand], screen_name="Q55mEhQS")):
        break

print(tweet_trim) # tweet_trim : すべてのCheckでFalseだった、かつ名詞がある文字列

youso_list = lists_getter(tweet_trim)


class Uses:
    using_noum = []
    using_adj = []
    using_adv = []
    using_joshi = []
    using_aux = []
    using_verv = []

    def __init__(self, youso_list):
        self.youso_list = youso_list

    def __random_maker(self, _list):
        return _list[int(random.randint(0, (len(_list))))]

    def use_set(self, num):
        __use = self.__random_maker(self.youso_list[num])
        self.youso_list[num].remove(__use)

        if num == 0:
            self.using_noum.append(__use)
        elif num == 1:
            self.using_adj.append(__use)
        elif num == 2:
            self.using_adv.append(__use)
        elif num == 3:
            self.using_joshi.append(__use)
        elif num == 4:
            self.using_aux.append(__use)
        elif num == 5:
            self.using_verv.append(__use)

    def make_text(self, _type):
        if _type == "noum":
            _list = self.using_noum
        elif _type == "adj":
            _list = self.using_adj
        elif _type == "adv":
            _list = self.using_adv
        elif _type == "joshi":
            _list = self.using_joshi
        elif _type == "aux":
            _list = self.using_aux
        elif _type == "verv":
            _list = self.using_verv

        _text = self.__random_maker(_list)
        _list.remove(_text)
        return _text

uses = Uses(youso_list)

# 名詞
uses.use_set(0)

while True:
    if (random.choice([True, False])) and uses.youso_list[1]: # 形容詞
        uses.use_set(1)
    
        if (random.choice([True, False])) and uses.youso_list[2]: # 副詞
            uses.use_set(2)
        
    if uses.youso_list[3] or uses.youso_list[4]:
        route = random.randint(0, 2)
        if route == 0:
            pass
        elif route == 1: # 助詞
            uses.use_set(4)

            if youso_list[5] and random.choice([True, False]):
                uses.use_set(5)
        else:
            uses.use_set(3)
    
    if uses.youso_list[0]:
        if random.choice([True, False]):
            uses.use_set(0)
        else:
            break
    else:
        break

word = ""

while uses.using_noum:
    if uses.using_adv:
        word += uses.make_text("adv")
    if uses.using_adj:
        word += uses.make_text("adj")
    if uses.using_noum:
        word += uses.make_text("noum")
    if uses.using_joshi:
        word += uses.make_text("joshi")
        if uses.using_verv:
            word += uses.make_text("verv")
    if uses.using_aux:
        word += uses.make_text("aux")

print(word)

twitter.favorite(acq[rand]["id_str"])

id_str = twitter.tweet("ばぬゆー%sやんないよ" % word)

with open(PATH, mode="w") as f:
    f.write(id_str)
