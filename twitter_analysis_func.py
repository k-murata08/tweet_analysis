#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime as dt
import collections
import twitter_generic_func as tg
import const as C

class Friend:
    def __init__(self, id, name, count, followers_count, bio):
        self.id = id
        self.name = name
        self.count = count
        self.followers_count = followers_count
        self.bio = bio


class User:
    def __init__(self, id, name, description, friends_count, created_at):
        self.id = id
        self.name = name
        self.description = description
        self.friends_count = friends_count
        self.created_at = created_at


def print_step_log(step_name, index, list_len):
    print step_name + " step:" + str(index+1) + "/" + str(list_len)


def print_query_error(action_name, user_id):
    print "Exception(" + action_name + ") USER_ID:" + str(user_id)


# 例: 自分のフォロワーのA,B,Cについて分析する時
# A, B, Cがそれぞれフォローしている人は、
# A, B, Cのうち何人にフォローされているのかを分析する。
# Friendオブジェクト(ID, 名前, 人数, BIO)の配列を返す。
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
            print_query_error("get_friend_ids", f_id)
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


# フォロワーの中で2016年以前の登録ユーザをフォロー数の降順に並べて
# 分析したアカウントをFriendインスタンスにしてリストで返す
def analysys_follower_friends_ex1():
    # 上限の5000人分取得
    follower_ids = tg.get_follower_ids(C.ANALYSYS_USER_ID, 500)

    followers = []

    # Userクラスとしてリストを作っておくと絞り込みが楽そうだった
    for index, follower_id in enumerate(follower_ids):
        print_step_log("CreateFollowersList", index, len(follower_ids))
        try:
            prof = tg.get_user_profile(follower_id)
            user = User(id=prof['id'],
                        name=prof['name'],
                        description=prof['description'],
                        friends_count=prof['friends_count'],
                        created_at=dt.strptime(prof['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))
            followers.append(user)
            sleep(1)
        except:
            print_query_error("get_user_profile", follower_id)


    # 2016年以前のユーザで絞り込みしフォロー数の多い順で並べる
    followers = filter(lambda obj:obj.created_at.year < 2016, followers)
    followers = sorted(followers, key=lambda obj: obj.friends_count, reverse=True)

    # とりあえず150人に絞る
    followers = followers[0:30]

    # フォロワーがフォローしている人
    friend_ids = []

    # 1回クエリを飛ばすごとに1分休む
    for index, follower in enumerate(followers):
        print_step_log("CreateFriendIDs", index, len(followers))
        try:
            ids = tg.get_friend_ids(follower.id, 5000) # 5000件取得できるIDの方を使う
            friend_ids.extend(ids)
        except:
            print_query_error("get_friend_ids", follower.id)
        sleep(60)

    # フレンドのIDをキーにして、フレンドがフォロワーにフォローされている人数を格納
    friends_counter_dict = collections.Counter(friend_ids)

    # フレンドのクラスの配列を作る
    # もっと良い書き方がありそう
    friends = []
    step=0
    for key, value in friends_counter_dict.items():
        step += 1
        print_step_log("CreateFriendList", step, len(friends_counter_dict))

        # とりあえず5人以上にフォローされているアカウントを取る
        if value > 4:
            try:
                prof = tg.get_user_profile(key)
                friend = Friend(id=key, name=prof['name'], count=value, followers_count=prof['followers_count'], bio=prof['description'])
                friends.append(friend)
            except:
                print_query_error("get_user_profile", key)
            sleep(1)

    # フォローされている数の昇順に並び替え
    friends = sorted(friends, key=lambda u: u.count, reverse=True)
    return friends
