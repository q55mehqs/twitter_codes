"""Twitterで拾ってきたツイートがどういうものかを判定します
"""

def isProtect(tweet : dict) -> bool:
    """拾ったツイートのユーザーが鍵垢かどうかを判定します

    Parameter
    ---------
    tweet : dict
        search, timelineなどで拾ってきたツイートのdictを入れてください。
        複数件の配列になっているものは使用できません。
    
    Return
    ------
    bool
        鍵垢ならTrue, 鍵じゃないならFalseを返します。
    """

    if tweet:
        return tweet["user"]["protected"]
    else:
        raise Exception("引数エラー ツイートがありません")


def isOwner(tweet : dict, id_str : str, screen_name : str) -> bool:
    """拾ったツイートが自分のものでないかを判定します

    Parameters
    ----------
    tweet : dict
        (必須)1つのツイートのdictを入れてください
    
    id_str : str
        (screen_nameかどちらか必須)ユーザーidの数字列を文字列型にして
        入れてください。どちらも入ってればこちらが優先されます
    
    screen_name : str
        (id_strかどちらか必須)スクリーンネーム(@Q55mEhQS の Q55mEhQS)
        を入れてください

    Return
    ------
    bool
        引数に入れたユーザーと同じならTrue, ちがうならFalseを返します
    """
    if tweet:
        if id_str:
            return tweet["user"]["id_str"] == id_str
        elif screen_name:
            return tweet["user"]["id_str"] == screen_name
        else:
            raise Exception("引数エラー id_str か screen_name は必ず入力してください")
    else:
        raise Exception("引数エラー 比較するツイートがありません")


def isAlreadyFavorited(tweet : dict) -> bool:
    """すでにファボ済みかどうかを確認します

    Parameter
    ---------
    tweet : dict
        (必須)確認するツイートの情報が入ったdict型を入れてください
    
    Return
    ------
    bool
        ふぁぼ済みならTrue、まだならFalseを返します
    """

    return tweet["favorited"]


def isReply(tweet : dict) -> bool:
    """ツイートが返信ツイかどうか確かめます

    Parameter
    ---------
    tweet : dict
        (必須)確認するツイートの情報が入ったdict型を入れてください

    Return
    ------
    bool
        返信ならTrue、そうでなければFalseを返します
    """

    return bool(tweet["entities"]["user_mentions"])


def isForeignLanguage(tweet : dict) -> bool:
    """ツイートが日本語かどうか判定します
    日本語が含まれていないとTrueになります

    Parameter
    ---------
    tweet : dict
        (必須)確認するツイートの情報が入ったdict型を入れてください

    Return
    ------
    bool
        日本語が含まれていなければTrue、含まれていればFalseを返します
    """

    if not tweet["lang"] == "ja":
        return True
    else:
        return False
