#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyknp import Jumanpp
import csv
import traceback

import const as C


def print_step_log(step_name, index, list_len):
    print step_name + " " + str(index+1) + "/" + str(list_len)


def split_list(list, n):
    """listをn個ずつの要素を持ったリストに分割する(余は余りでリストになる)"""
    return [list[x:x+n] for x in range(0, len(list), n)]


def get_keitaiso_list_from_juman(text):
    """
    textを形態素解析して返す
    mecabでできない表記揺れの問題をjumanだと解決できる
    """

    jumanpp = Jumanpp()
    keitaiso_list = []
    hinshi_list = []
    exclusive_word_list = get_exclusive_word_list()

    # スペースがあるとエラー。先頭に#があると処理が動かなくなる(なんでだろう)
    text = text.replace(" ", "").replace("　", "").replace("#", "/")

    result = jumanpp.analysis(unicode(text, 'utf-8')) # pyknp-Jumanではユニコード文字列しか処理されない
    try:
        for mrph in result.mrph_list():
            keitaiso = mrph.genkei.encode('utf-8')
            hinshi = mrph.hinsi.encode('utf-8')
            # 形態素が設定した品詞リストやゴミワードリストに含まれるとき、数字のときにはスキップ
            if not is_valid_word_class(hinshi) or keitaiso in exclusive_word_list or keitaiso.isdigit():
                continue

            keitaiso_list.append(keitaiso)
            hinshi_list.append(hinshi)
    except:
        print traceback.print_exc()

    return [keitaiso_list, hinshi_list]


def get_exclusive_word_list():
    """ゴミワードリスト"""
    with open('exclusive_word.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        word_list = [row[0] for row in reader]

    return word_list


def is_valid_word_class(word_class):
    """抽出する品詞に当てはまるか"""
    if word_class in C.VALID_WORD_CLASS:
        return True
    return False
