# -*- coding: utf-8 -*-
"""
MeCabを使った形態素解析でテキストをベクトル化するやつです。
"""
import MeCab
from collections import Counter


class keitaiso:
    def __init__(self, use_PoW=['名詞','動詞','形容詞','副詞','記号'], stop_words=[], use_words=[], user_dic_files=[]):
        """
        ARGUMENT
        ----------------
        use_PoW [list]:
            .tokenize(text) で出力される品詞を指定する。
            ex) use_PoW=['名詞','動詞'] なら名詞と動詞しか出力しない。
        stop_words [list]:
            .tokenize(text) で出力しない単語を指定する。∂
        use_words [list]:
            .tokenize(text) で出力する単語の集合を指定する。
            defaultは空リスト([])であり、この場合は全ての単語が出力される。
        user_dic_files [list]:
            Mecabが形態素解析に用いるユーザー辞書を指定する場合に用いる。            
        
        EXAMPLE
        ----------------
        text = "すももも桃も桃の内です"
        use_PoW = ['名詞','動詞']
        stop_words = ['*','よう','上','の','様','こちら','際','ところ','はず','\u3000',]
    
        k = keitaiso(use_PoW=use_PoW,stop_words=stop_words)
        print(k.basic_tokenize(text))
         > [[0, '名詞', 'すもも'], [1, '助詞', 'も'], [2, '名詞', '桃'], [3, '助詞', 'も'], [4, '名詞', '桃'], [5, '助詞', 'の'], [6, '名詞', '内'], [7, '助動詞', 'です']]
        print(k.tokenize(text))
         > [[0, '名詞', 'すもも'], [2, '名詞', '桃'], [4, '名詞', '桃'], [6, '名詞', '内']]        
        print(k.tokenize_to_bag_of_words(text))
         > {'すもも': 1, '桃': 2, '内': 1}
        print(k.tokenize_to_wakachi(text))
         > "すもも 桃 桃 内"
        """
        self.use_PoW = use_PoW
        self.stop_words = stop_words
        self.use_words = use_words
        if len(user_dic_files)>0:
            arg_user_dic_files = '-u '+','.join(user_dic_files)
        else:
            arg_user_dic_files = ''
        self.tagger = MeCab.Tagger(arg_user_dic_files)

    def tokenize(self, text):
        """
        text を形態素分解した結果を返却する
        
        ARGUMENT
        ---------------
        text [str]:
            日本語の文章
        """
        processing = self.basic_tokenize(text)
        processing = self.filter_PoW(processing)
        processing = self.filter_stop_words(processing)
        processing = self.filter_use_words(processing)
            
        return processing
    
    def tokenize_to_bag_of_words(self, text):
        """
        text を形態素分解した結果を Bag of words で集計し、dictionary型として返却する。
        
        ARGUMENT
        ---------------
        text [str]:
            日本語の文章
        """
        processing = self.tokenize(text)
        processing = [p[2] for p in processing]
        processing = Counter(processing)
        return dict(processing)
    
    def tokenize_to_wakachi(self, text):
        """
        text を形態素分解した結果を わかち書き 形式のstrとして返却する。
        
        ARGUMENT
        ---------------
        text [str]:
            日本語の文章
        """
        processing = self.tokenize(text)
        processing = [p[2] for p in processing]
        return ' '.join(processing)                        

    def basic_tokenize(self, text):
        if not isinstance(text, str):
            parsed = [[1,'*','*'],]
        else:
            parsed = self.tagger.parse(text).split('\n')[:-2]
            parsed = [p.split('\t')[1] for p in parsed]
            parsed = [[idx, p.split(',')[0], p.split(',')[6]] for idx, p in enumerate(parsed)]
        return parsed

    def filter_PoW(self, basic_tokenized,):
        return [token for token in basic_tokenized if token[1] in self.use_PoW]

    def filter_stop_words(self, basic_tokenized,):
        return [token for token in basic_tokenized if token[2] not in self.stop_words]

    def filter_use_words(self, basic_tokenized,):
        if self.use_words == []:
            return basic_tokenized
        else:
            return [token for token in basic_tokenized if token[2] in self.use_words]

    def change_dict(self, tokenized,):
        words_list = [token[2] for token in tokenized]
        words_set = set(words_list)
        result_dict = dict()
        for word in words_set:
            result_dict[word] = words_list.count(word)
        return result_dict


if __name__ == "__main__":
    text = "今日は何時に帰ってきますか？　と彼女は尋ねてくる"
    use_PoW = ['名詞','動詞','形容詞','副詞','記号',]
    stop_words = ['*','よう','上','の','様','こちら','際','ところ','はず','\u3000',]

    k = keitaiso(use_PoW=use_PoW,stop_words=stop_words)
    print(k.basic_tokenize(text))
    print(k.tokenize(text))
