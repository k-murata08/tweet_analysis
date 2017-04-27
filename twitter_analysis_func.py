#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
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
    def __init__(self, id, name, description, friends_count, created_at, is_protected):
        self.id = id
        self.name = name
        self.description = description
        self.friends_count = friends_count
        self.created_at = created_at
        self.is_protected = is_protected


def print_step_log(step_name, index, list_len):
    print step_name + " : " + str(index+1) + "/" + str(list_len)


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


def create_users_from_ids(user_ids, stage_num):
    users = []
    for index, user_id in enumerate(user_ids):
        print_step_log("CreateUsersList(stage"+str(stage_num)+")", index, len(user_ids))
        try:
            prof = tg.get_user_profile(user_id)
            user = User(id=prof['id'],
                        name=prof['name'],
                        description=prof['description'],
                        friends_count=prof['friends_count'],
                        created_at=dt.strptime(prof['created_at'], "%a %b %d %H:%M:%S +0000 %Y"),
                        is_protected=prof['protected'])
            users.append(user)
        except:
            print_query_error("get_user_profile", user_id)
        finally:
            sleep(1)
    return users


def create_friend_ids_from_users(users, stage_num):
    friend_ids = []
    for index, user in enumerate(users):
        print_step_log("CreateFriendIDs(stage"+str(stage_num)+")", index, len(users))
        try:
            ids = tg.get_friend_ids(user.id, 5000)
            friend_ids.extend(ids)
        except:
            print_query_error("get_friend_ids", user.id)
        finally:
            sleep(60)
    return friend_ids


# フォロワーの中で2016年以前の登録ユーザをフォロー数の降順に並べて
# 分析したアカウントをFriendインスタンスにしてリストで返す
def analysys_follower_friends_ex1():
    # 上限の5000人分取得
    follower_ids = tg.get_follower_ids(C.ANALYSYS_USER_ID, 5000)
    followers = create_users_from_ids(user_ids=follower_ids, stage_num=1)

    del follower_ids

    # 2016年以前のユーザで絞り込み,
    # ツイートとかフォロイーを公開にしているユーザで絞り込み,
    # フォロー数の多い順で並べる
    followers = filter(lambda obj:obj.created_at.year < 2016, followers)
    followers = filter(lambda obj:obj.is_protected == False, followers)
    followers = sorted(followers, key=lambda obj: obj.friends_count, reverse=True)

    # とりあえず400人に絞る
    followers = followers[0:400]

    # フォロワーがフォローしている人
    friend_ids = create_friend_ids_from_users(users=followers, stage_num=2)

    # 一応メモリ解放
    del followers
    gc.collect()

    # フレンドのIDをキーにして、フレンドがフォロワーにフォローされている人数を格納
    friends_counter_dict = collections.Counter(friend_ids)

    del friend_ids
    gc.collect()

    # フレンドのクラスの配列を作る
    # FIXME:ここも関数にしたかったけど関数にしたらcountとidの挙動がおかしなことになったのでとりあえず直書き
    friends = []
    step=0 # FIXME:辞書のループ用インデックス。、friends_counter_dict.keys().index(key)で取りたかったけど何故か無限ループするようになってしまったのでstepでやってる
    for key, value in friends_counter_dict.items():
        step += 1
        print_step_log("CreateFriendList(stage3)", step, len(friends_counter_dict))

        # とりあえず20人以上にフォローされているアカウントを取る
        if value > 20:
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
