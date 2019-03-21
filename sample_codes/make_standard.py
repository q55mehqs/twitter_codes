# coding: utf-8

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

res = twitter.timeline(count=1)

PATH = "./id_kijun.log"

with open(PATH, mode="w") as f:
    f.write(res[0]["id_str"])
