# Twitterを制御するやつ(develop 版)

正直こんな関数作るのに労力はたいしてかかりませんが、公開したら公開したでちょっと便利かなぁって思ったので作りました

develop版は、各関数をクラス化して、コンストラクタで各キー、トークンを入力する仕様にしています。

個人で使っていたものですが、よければ使ってみてください


## 使い方

### Twitterに投稿するためにAPIをつくる

[Twitter Developers のAPIのページ](https://developer.twitter.com/en/apps) で、APIを作ってください。

ここが結構めんどくさいです。英語ができないと苦戦するので頑張ってください。

調べればこれの解説をしてるページがたぶん出てきます。なんとかして作りましょう。


### 作ったAPIから各トークンを拾う

先程のAPIのページで、できたアプリの「Details」ボタンを押して、そこから「Permission」で権限をえらびます

ReadとWriteは必ずできるようにしてください。

そうしたら、「Keys And Tokens」ページに行き、適当に操作して各種キーを表示させます。

できた「API key」「API secret key」「Access token」「Access token secret」を控えてください。

なお、これから「API key」「API secret key」を、これの旧称である「Consumer key」「Consumer key secret」にあやかり、それぞれ「CK」「CS」と、

「Access token」「Access token secret」を「AT」「AS」と略します。

これはコード内でも同一です。


### クローンする

git の操作ができる環境で、適当なディレクトリに移り、

    git clone -b branch https://github.com/q55mehqs/twitter_codes.git

と入力してください。


### 各キー、トークンの処理

このコードでは、先述のとおりコンストラクタでキー、トークンを入力してから動作を行います。

なんかちゃんと権限を取ってて、うまく設定をデキる人は環境変数でキー、トークンを保存しておくといいでしょう。

(セキュリティ的にどうなのかなぁとは思いますが) Linuxの人は setting.sh を実行し、そのとおりに入力するとファイルが出来上がります。

ファイルor環境変数を利用して、これから作成するプログラムから各種取り出せるようにしておいてください。


### コード作成

    .
    ├ twitter_example
      └ ...
    └ making_code.py

のようなディレクトリ構成で、making_code.pyを作成するとして進めていきます

making_code.py

    from twitter_example import Twitter

    # CK, CS, AT, AS 変数にキー、トークンを代入

    twitter = Twitter(CK, CS, AT, AS)

    # ツイートする
    twitter.send("ツイート")

このように始めることができます。
