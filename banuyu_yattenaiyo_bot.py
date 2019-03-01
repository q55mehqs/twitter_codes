"""特定ユーザーに粘着して、最新ツイートに「{user_name}は{text(noum.)}やってないよ」
って返信してくる意味わからないbot機能
拾ったツイートに名詞が入ってなかったときの例外処理などは書いていません。
twittersの関数の使用例として見てください。。。
"""

from twitters import tweet, user_timeline

from janome.tokenizer import Tokenizer


analyzer = Tokenizer()


def get_tweet_info(screen_name):
    """投げられたスクリーンネームからid、ユーザー名、
    ツイート文字列を返します。

    Parameter
    ---------
    screen_name : str
        粘着したいユーザーのスクリーンネーム(@Q55mEhQS の Q55mEhQS)
        を入れてください。

    Returns
    -------
    tuple
        [0]ツイートid、[1]ユーザー名、[2]ツイート文字列を返します。
        すべてstr型です。
    """
    tweet_data = user_timeline(screen_name=screen_name, count=1)[0]

    return tweet_data["id_str"], tweet_data["user"]["name"], tweet_data["text"]


def analyze_text(text):
    """引数の文字列を解析し、そのツイートの名詞を返します。

    Parameter
    ---------
    text : str
        解析したい文字列です
    
    Return
    ------
    noum : str
        解析した引数の名詞を一つ返します。
    """

    analyzeds = analyzer.tokenize(text)

    for token in analyzeds:
        part = token.part_of_speech.split(",")
        if part[0] == "名詞":
            return token.surface


if __name__ == "__main__":
    screen_name = "Q55mEhQS"

    tweet_info = get_tweet_info(screen_name)
    noum = analyze_text(tweet_info[2])

    rep_text = "@%s %sは%sやってないよ" % (screen_name ,tweet_info[1], noum)
    print(rep_text)

    tweet(rep_text, reply_id=tweet_info[0])
