"""Twitterで拾ってきたツイートがどういうものかを判定します
Falseのほうが扱いやすい(？)ツイートです
引数がtimeline系やsearchのようなエンドポイントから取得した
値になっていないとTypeErrorが発生します
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

    return tweet["user"]["protected"]


def isOwner(tweet, id_str="", screen_name=""):
    """拾ったツイートが自分のものでないかを判定します
    型ヒントがないのはデフォルト有の書き方がわからないからです

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
    if id_str:
        return tweet["user"]["id_str"] == id_str
    elif screen_name:
        return tweet["user"]["screen_name"] == screen_name
    else:
        raise Exception("引数エラー id_str か screen_name は必ず入力してください")


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


def isAllCheck_or(tweet, id_str="", screen_name="") -> bool:
    """入れたツイートをすべての関数でチェックして
    すべてorでかけたものを返します

    Parameter
    ---------
    tweet : dict
        (必須)確認するツイートの情報が入ったdict型を入れてください

    id_str : str
        (screen_nameかどちらか必須)ユーザーidの数字列を文字列型にして
        入れてください。どちらも入ってればこちらが優先されます
    
    screen_name : str
        (id_strかどちらか必須)スクリーンネーム(@Q55mEhQS の Q55mEhQS)
        を入れてください
    
    Return
    ------
    bool
        ここにある関数をすべてorでつないだものを返します
    """

    return (isProtect(tweet) or isOwner(tweet, id_str=id_str, screen_name=screen_name) or 
            isReply(tweet) or isForeignLanguage(tweet))


# if __name__ == "__main__":
#     from twitters import Twitter
#     import tokens
#     twitter = Twitter(tokens.CK, tokens.CS,
#             tokens.AT, tokens.AS)

#     tweet = twitter.user_timeline(screen_name="Q55mEhQS", count=10, no_catch_reply=False)[0]
#     print(tweet["text"])

#     print("Protected: %s" % str(isProtect(tweet)))
#     print("Owner: %s" % str(isOwner(tweet, screen_name="Q55mEhQS")))
#     print("Reply: %s" % str(isReply(tweet)))
#     print("Lang!=ja: %s" % str(isForeignLanguage(tweet)))
#     print("all: %s" % str(isAllCheck_or(tweet, screen_name="Q55mEhQS")))
