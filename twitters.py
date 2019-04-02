"""
Twitters
========
ツイッターサーバーとHTTP通信でPOST/GETのやりとりをします
"""

# try:
#     import tokens as test
# except ImportError:
#     pass

from requests_oauthlib import OAuth1Session
import json


class Twitter:
    """Twitterに関する操作の実行をします。

    使い方
    ======
    最初に、インスタンスをこのような書式で生成してください

        >>> from twitters import Twitter
        >>> t = Twitter("{Consumer Key}", "{Consumer Key Secret}",
        ...         "{Access Token}", "{Access Token Secret}")

    ツイートをする
    --------------
        >>> t.tweet("ツイート文")
        ... # 画像ツイート、返信の指定方法はtweetのdocstringを
        ... # 参照してください

    検索
    ----
        >>> t.search("検索ワード")
        [{'created_at': 'Mon Mar 04 16:02:06 +0000 2019', ... }]

    ふぁぼ
    ------
        >>> t.favorite("{Tweet ID}")
    """
    def __init__(self, CK, CS, AT, AS):
        self.__t = OAuth1Session(CK, CS, AT, AS)


    def __pic_makeid(self, pic_path):
        """画像ツイートに必要なアップロード、
        アップロードした画像のID取得をします。
        この関数で行うのはTwitterサーバーに画像をアップロード
        するだけです。ツイートはされないのでご注意ください。

        Parameter
        ---------
        pic_path : str
            アップロードする画像のファイルパスを入れる引数。
        
        Returns
        -------
        media_id : str
            Twitterサーバーに画像を上げたとき生成されたIDを返します。
            このIDをツイートのパラメータに入れることで画像ツイートが
            できます。
            アップロード失敗時は空文字列 ("") を返します。
        """

        URL = "https://upload.twitter.com/1.1/media/upload.json"

        # 画像が開ければ続行、開けなければ例外処理し、
        # Falseを返す
        try:
            data = open(pic_path, "rb")
        except:
            print("error file can't open")
            return ""

        # 開いた画像ファイルをそのままパラメータに格納
        _pic_up_params = {"media": data}

        # 画像をアップロード
        _pic_up_req = self.__t.post(URL, files = _pic_up_params)

        # 画像アップロードが成功したらmedia_idを、
        # 失敗してたらFalseを返します
        if _pic_up_req.status_code == 200:
            media_id = json.loads(_pic_up_req.text)["media_id_string"]
            return media_id
        else:
            print("failed upload pic(Error Code: %s)" % str(_pic_up_req.status_code))
            return ""


    def tweet(self, text, pic_paths=[], reply_id=""):
        """ツイートの送信をします。
        引数にツイートの投稿内容を入れてください。

        Parameter
        ---------
        text : str
            ツイートするワードを入れる引数。

        pic_paths : list
            アップロードする画像のファイルパスを入れる引数。
            list型で画像のパスの文字列を入れてください。(1枚でもlistに)
            デフォルトは空文字列。(画像投稿なし)

        reply_id : str
            ツイートへの返信をするときの返信元のidを入れる引数。
            デフォルトは空文字列。(返信なし)
        
        Returns
        -------
        bool
            投稿成功したらTrue、失敗ならFalseが返ります。
            ちなみにそれぞれ結果がターミナルに出力されます。
        """

        # status/update エンドポイントURLです
        URL = "https://api.twitter.com/1.1/statuses/update.json"

        # パラメータをつくります
        _params = {"status" : text}

        # 画像ツイの対応をします
        if pic_paths:
            pic_data = ""
            for pic_path in pic_paths:
                if not pic_data:
                    pic_data = self.__pic_makeid(pic_path)
                else:
                    pic_data = "%s,%s" % (pic_data, self.__pic_makeid(pic_path))
            _params.update({"media_ids": pic_data})

        # 返信の対応
        if reply_id:
            _params.update({"in_reply_to_status_id": reply_id})

        # 投げます
        req = self.__t.post(URL, params = _params)

        # 投稿が成功したら req のstatus_codeが
        # 200になるので、成功か失敗かを判別します。
        if req.status_code == 200:
            print("success")
            res_id = json.loads(req.text)["id_str"]
            return res_id
        else:
            print("failed (Error Code: %s)" % str(req.status_code))
            return False


    def search(self, word, count=10, _type="recent"):
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
        req = self.__t.get(URL, params = _params)

        if req.status_code == 200:
            # json形式で帰ってきた値をdict型にした後、
            # ツイートの内容が入っているstatusキーのvalueを格納します
            res_data = json.loads(req.text)["statuses"]

            # 上で格納したstatusキーの中身を返します
            return res_data


    def timeline(self, count=10, since_id="", max_id="", no_catch_reply=True):
        """タイムラインを表示します。

        Parameters
        ----------
        count : int
            何件のツイートを取得するか設定します。
            デフォルトは10(件)です。

        since_id : str (or int)
            ツイートのid(数字列)を選択すると、そのツイートを含まず、
            これより未来のツイートを取得できます。
            指定なしでも問題なく取得できます。デフォルトは指定なしです。

        max_id : str
            ツイートのid(数字列)を選択すると、そのツイートを含まず、
            これより過去のツイートを取得できます。
            指定なしでも問題なく取得できます。デフォルトは指定なしです。

        no_catch_reply : bool
            取得するタイムラインに返信ツイートを含めるか指定します。
            Trueにすると除外、Falseにすると除外せず表示します。
            デフォルトは除外のTrueです。

        Returns
        -------
        res_data : list, dict
            [{ツイートのデータ}, {ツイートのデータ}, ... *countの数]
            みたいに、countの数の分だけのdictの要素があるlistに
            なって返ってます。
            公式Docs <https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-home_timeline.html>
            の値を返しているので、詳しくはそちらを参照し、
            適宜、値を取り出してください。
        """

        URL = "https://api.twitter.com/1.1/statuses/home_timeline.json"

        # 公式Docsに沿ってパラメータを指定します
        _params = {
            "count": str(count),
        }

        # dict1.update(dict2) <- dict1 に dict2 の中身を追加
        # 一致するキーがあればvalueをdict2側に変更
        if since_id:
            _params.update({"since_id": since_id})
        if max_id:
            _params.update({"max_id": max_id})

        if no_catch_reply:
            _params.update({"exclude_replies": "true"})
        else:
            _params.update({"exclude_replies": "false"})

        req = self.__t.get(URL, params = _params)

        if req.status_code == 200:
            # json形式で帰ってきた値をdict型にした後、
            # ツイートの内容が入っているstatusキーのvalueを格納します
            res_data = json.loads(req.text)

            # 上で格納したstatusキーの中身を返します
            return res_data


    def user_timeline(self, user_id="", screen_name="", count=10, since_id="", max_id="", no_catch_reply=True, catch_rt=False):
        """ユーザーを指定してタイムラインを取得します。
        
        Parameters
        ----------
        user_id : str (or int) // どっちでもいい
            (screen_name かどちらか必須)取得したいユーザーをユーザーid(数字列)で選択します。
            user_id も screen_name もどちらも入力されたときはこちらを優先します。
            片方だけでいいです。

        screen_name : str
            (user_id かどちらか必須)取得したいユーザーをスクリーンネーム
            (@Q55mEhQS の Q55... など)で選択します。

        count : int (or str) // どっちでもいい
            ツイートを取得する件数を選択します。デフォルトは10です。

        since_id : str (or int)
            ツイートのid(数字列)を選択すると、そのツイートを含まず、
            これより未来のツイートを取得できます。
            指定なしでも問題なく取得できます。デフォルトは指定なしです。

        max_id : str (or int)
            ツイートのid(数字列)を選択すると、そのツイートを含まず、
            これより過去のツイートを取得できます。
            指定なしでも問題なく取得できます。デフォルトは指定なしです。
        
        no_catch_reply : bool
            取得するツイートに返信ツイートを含めるか選択します。
            Trueだと含まない、Falseだと含みます。デフォルトはTrueです。
        
        catch_rt : bool
            取得するツイートにリツイートを含めるか選択します。
            Trueだと含む、Falseだと含みません。デフォルトはFalseです。
        

        Returns
        -------
        res_data : list, dict
            [{ツイートのデータ}, {ツイートのデータ}, ... *countの数]
            みたいに、countの数の分だけのdictの要素があるlistに
            なって返ってます。
            公式Docs <https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline>
            の値を返しているので、詳しくはそちらを参照し、
            適宜、値を取り出してください。
        """

        URL = "https://api.twitter.com/1.1/statuses/user_timeline.json"

        # 引数に合わせてパラメータを作っていきます
        _params = {
            "count": str(count)
        }


        # dict1.update(dict2) <- dict1 に dict2 の中身を追加
        # 一致するキーがあればvalueをdict2側に変更

        # ユーザー指定
        if user_id:
            _params.update({"user_id": user_id})
        elif screen_name:
            _params.update({"screen_name": screen_name})
        else:
            print("ユーザーidかスクリーンネームのどちらかは必ず指定してください。")
            return []

        # since_id and max_id
        if since_id:
            _params.update({"since_id": since_id})
        if max_id:
            _params.update({"max_id": max_id})

        # 返信の有無
        if no_catch_reply:
            _params.update({"exclude_replies": "true"})
        else:
            _params.update({"exclude_replies": "false"})

        # RTの有無
        if catch_rt:
            _params.update({"include_rts": "true"})
        else:
            _params.update({"include_rts": "false"})

        req = self.__t.get(URL, params = _params)

        if req.status_code == 200:
            # json形式で帰ってきた値をdict型にした後、
            # ツイートの内容が入っているstatusキーのvalueを格納します
            res_data = json.loads(req.text)

            # 上で格納したstatusキーの中身を返します
            return res_data
        else:
            print("failed catch (Error Code: %s)" % str(req.status_code))
            return []


    def favorite(self, tweet_id):
        """引数で送られたidのツイートにファボを飛ばします。"""

        URL = "https://api.twitter.com/1.1/favorites/create.json"

        _params = {
            "id": tweet_id
        }

        req = self.__t.post(URL, params=_params)

        if req.status_code == 200:
            return True
        else:
            print("failed fav (Error Code: %s)" % str(req.status_code))
            return False


# if __name__ == "__main__":
#     import tokens
#     t = Twitter(tokens.CK, tokens.CS, tokens.AT, tokens.AS)

#     t.tweet("てすと")
#     print(t.search("#RakutenEagles", count=2))
#     print(t.timeline(count=3))
#     user_tweets = t.user_timeline(screen_name="Q55mEhQS", count=2)

#     for user_tweet in user_tweets:
#         t.favorite(user_tweet["id_str"])
