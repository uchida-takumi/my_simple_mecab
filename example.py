#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使い方の例
"""

from src.my_simple_mecab import keitaiso

text = "今日は何時に帰ってきますか？　と彼女は尋ねてくる"
use_PoW = ['名詞','動詞','形容詞','副詞','記号',]
stop_words = ['*','よう','上','の','様','こちら','際','ところ','はず','\u3000',]

k = keitaiso(use_PoW=use_PoW,stop_words=stop_words)

print('以下をmecabを使って形態素解析します。')
print(text)
print('ーーーー')
print('結果１：')
print(k.basic_tokenize(text))
print('ーーーー')
print('結果２：')
print(k.tokenize(text))
