from janome.tokenizer import Tokenizer


analyzer = Tokenizer()


def noum_check(text):
    """引数の文字列を解析し、そのツイートの名詞を返します。

    Parameter
    ---------
    text : str
        解析したい文字列です
    
    Return
    ------
    bool
    """

    analyzeds = analyzer.tokenize(text)

    for token in analyzeds:
        part = token.part_of_speech.split(",")
        if part[0] == "名詞":
            return True
    else:
        print("名詞がありません")
        return False


def lists_getter(text):
    noum_list = []
    adj_list = []
    adv_list = []
    joshi_list = []
    aux_list = [] # 助動詞
    verv_list = []

    analyzeds = analyzer.tokenize(text)

    for token in analyzeds:
        part = token.part_of_speech.split(",")
        if part[0] == "名詞":
            noum_list.append(token.surface)
        elif part[0] == "形容詞":
            adj_list.append(token.surface)
        elif part[0] == "副詞":
            adv_list.append(token.surface)
        elif part[0] == "助動詞":
            joshi_list.append(token.surface)
        elif part[0] == "助詞":
            aux_list.append(token.surface)
        elif part[0] == "動詞":
            verv_list.append(token.surface)
        else:
            pass
    
    return noum_list, adj_list, adv_list, joshi_list, aux_list, verv_list


if __name__ == "__main__":
    # print(noum_check("すもも,も,もも,も,もも,の,うち"))
    print(lists_getter("すもももももももものうち"))