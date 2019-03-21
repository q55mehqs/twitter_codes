# coding: utf-8

from twitters import timeline

res = timeline(count=1)

PATH = "./id_kijun.log"

with open(PATH, mode="w") as f:
    f.write(res[0]["id_str"])
