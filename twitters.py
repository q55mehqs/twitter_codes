import test_token as test

from requests_oauthlib import OAuth1Session

import json


t = OAuth1Session(test.CK, test.CS, test.AT, test.AS)


def tweet(text):
    """文字のみのツイートの送信をします。
    引数にツイートの投稿内容を入れてください。

    Parameters
    ----------
    text : str
      ツイートするワードを入れる引数。
      ここに入れた文字がツイートされるだけです。
    
    Returns
    -------
    bool
      投稿成功したらTrue、失敗ならFalseが返ります。
      ちなみにそれぞれ結果がターミナルに出力されます。
    """

    # status/update エンドポイントURLです
    URL = "https://api.twitter.com/1.1/statuses/update.json"

    # 公式Docsからこのエンドポイントの説明が探し出せませんでした
    _params = {"status" : text}

    # 投げます
    req = t.post(URL, params = _params)

    # 投稿が成功したら req のstatus_codeが
    # 200になるので、成功か失敗かを判別します。
    if req.status_code == 200:
        print("success")
        return True
    else:
        print("failed Error Code: %s" % str(req.status_code))
        return False


def search(word, count=10, _type="recent"):
    """Twitterで検索する関数です
    word に探したい関数、countで検索したい件数を入れてください
    検索できたツイートの各種情報が返ってきます

    Parameters
    ----------
    word : str
      検索したいワードを入れる引数。
      since: やlang: など検索拡張子を入れても構いません。

    count : int
      何個のツイートを取得するかを入れる引数。
      範囲は 1~100、デフォルトは10です。

    _type : str
      検索するツイートの種類を入れる引数。
      "popular" 人気のツイート
      "recent" 最新のツイート
      "mixed" ミックス
      いずれかで指定してください。デフォルトは recent です。

    Returns
    -------
    res_data : list, dict
      [{ツイートのデータ}, {ツイートのデータ}, ... *countの数]
      みたいに、countの数の分だけのdictの要素があるlistに
      なって返ってます。
      公式Docs <https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html>
      のstatusキーの中身を返しているので、詳しくはそちらを参照し、
      適宜、値を取り出してください。
    """
    # search/tweets エンドポイントを使用して検索するので
    # エンドポイントURLは以下の通りになります
    URL = "https://api.twitter.com/1.1/search/tweets.json"

    # https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html
    # 公式Docsに沿ってパラメータの指定をdict型で行います
    _params = {
        "q": word,
        "count": count,
        "result_type": _type
    }

    # 上記パラメータで返る情報を格納しておきます
    req = t.get(URL, params = _params)

    if req.status_code == 200:
        # json形式で帰ってきた値をdict型にした後、
        # ツイートの内容が入っているstatusキーのvalueを格納します
        res_data = json.loads(req.text)["statuses"]

        # 上で格納したstatusキーの中身を返します
        return res_data


if __name__ == "__main__":
    reses = search("クソツイ", count=5)

    for res in reses:
        print("%s: %s\n" % (res["user"]["name"], res["text"]))

    tweet("こんなに説明を書きまくってるコード初めてって毎回言ってる気がする")