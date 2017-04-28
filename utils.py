#!/usr/bin/env python
# -*- coding: utf-8 -*-

from natto import MeCab

def print_step_log(step_name, index, list_len):
    print step_name + " : " + str(index+1) + "/" + str(list_len)


def print_query_error(action_name, user_id):
    print "Exception(" + action_name + ") USER_ID:" + str(user_id)


# listをn個ずつの要素を持ったリストに分割する(余は余りでリストになる)
def split_list(list, n):
    return [list[x:x+n] for x in range(0, len(list), n)]


# textを形態素解析して返す
def get_keitaiso_list(text):
    """
    @param text type->string
    @return [[形態素1, 形態素2, ..., 形態素n], [品詞1, 品詞2, ..., 品詞n]]
    """
    mc = MeCab('-F%m,%f[0]')
    keitaiso_list = []
    hinshi_list = []

    for word_row in mc.parse(text, as_nodes=True):
        row_split = word_row.feature.split(',')
        # MeCabでは必ず最後にEOSが含まれる
        if (row_split[0] == 'EOS'):
            break
        if row_split[0].isdigit():
            row_split[0] = str(row_split[0])
        keitaiso_list.append(row_split[0])
        hinshi_list.append(row_split[1])

    return [keitaiso_list, hinshi_list]
