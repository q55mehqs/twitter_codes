#!/bin/bash


SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR


if [ ! -f $SCRIPT_DIR/tokens.py ]; then
    echo "# coding: utf-8" > tokens.py
    echo "" >> tokens.py

    #入力待ちにメッセージを表示
    echo "Twitter APIの 'Consumer Key' を入力してください"
    read ck
    echo "# Consumer Key" >> tokens.py
    echo "CK = '$ck'" >> tokens.py
    echo "" >> tokens.py

    echo "Twitter APIの 'Consumer Key Secret' を入力してください"
    read cs
    echo "# Consumer Key Secret" >> tokens.py
    echo "CS = '$cs'" >> tokens.py
    echo "" >> tokens.py

    echo "Twitter APIの 'Access Token' を入力してください"
    read at
    echo "# Access Token" >> tokens.py
    echo "AT = '$at'" >> tokens.py
    echo "" >> tokens.py

    echo "Twitter APIの 'Access Token Secret' を入力してください"
    read as
    echo "# Access Token Secret" >> tokens.py
    echo "AS = '$as'" >> tokens.py
    echo "" >> tokens.py


    echo "設定ファイルが作成されました"
else
    echo "設定ファイルは存在しています。tokens.py を書き換えてください"
fi