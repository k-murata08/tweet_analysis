#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import collections
import twitter_generic_func as tg
import const as C

class Friend:
    def __init__(self, id, name, count, bio):
        self.id = id
        self.name = name
        self.count = count
        self.bio = bio


# 例: 自分のフォロワーのA,B,Cについて分析する時
# A, B, Cがそれぞれフォローしている人は、
# A, B, Cのうち何人にフォローされているのかを分析する。
# Friendオブジェクト(ID, 名前, 人数)の配列を返す。
def analysys_follower_friends():

    # 上限の5000人分取得
    follower_ids = tg.get_follower_ids(C.ANALYSYS_USER_ID, 5000)
    sleep(2)

    # フォロワーがフォローしている人
    friend_ids = []

    # 1回クエリを飛ばすごとに1分1秒休む
    # テスト用に5人分回している(本来は全員に対して回す)
    for f_id in follower_ids[5:6]:
        try:
            ids = tg.get_friend_ids(f_id, 5000) # 5000件取得できるIDの方を使う
            friend_ids.extend(ids)
        except:
            print "No Responce(USER_ID: " + str(f_id) + ")"
        sleep(60)


    # フレンドのIDをキーにして、フレンドがフォロワーにフォローされている人数を格納
    friends_counter_dict = collections.Counter(friend_ids)

    # フレンドのクラスの配列を作る
    # もっと良い書き方がありそう
    friends = []
    for key, value in friends_counter_dict.items()[0:2]:
        # 一人以下の時には追加しない
        if value <= 1:
            continue

        prof = tg.get_user_profile(key) # プロフィール取得は何故か15分間に900回も回せる
        friend = Friend(id=key, name=prof['name'], count=value, bio=prof['description'])
        friends.append(friend)
        sleep(1.5)

    # フォローされている数の昇順に並び替え
    friends = sorted(friends, key=lambda u: u.count, reverse=True)
    return friends
