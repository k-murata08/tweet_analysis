#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
from time import sleep
from datetime import datetime as dt
import collections
import twitter_generic_func as tg
import const as C
import utils

class Friend:
    def __init__(self, id, name, count, followers_count, bio, follow_rate, follow_ratio, factor):
        self.id = id
        self.name = name
        self.count = count
        self.followers_count = followers_count
        self.bio = bio
        self.follow_rate = follow_rate
        self.follow_ratio = follow_ratio
        self.factor = factor


class User:
    def __init__(self, id, name, description, friends_count, created_at, is_protected):
        self.id = id
        self.name = name
        self.description = description
        self.friends_count = friends_count
        self.created_at = created_at
        self.is_protected = is_protected


def create_users_from_ids(user_ids, stage_num):
    users = []
    for index, user_id in enumerate(user_ids):
        utils.print_step_log("CreateUsersList(stage"+str(stage_num)+")", index, len(user_ids))
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
            utils.print_query_error("get_user_profile", user_id)
        finally:
            sleep(1)
    return users


def create_friend_ids_from_users(users, stage_num):
    friend_ids = []
    for index, user in enumerate(users):
        utils.print_step_log("CreateFriendIDs(stage"+str(stage_num)+")", index, len(users))
        try:
            ids = tg.get_friend_ids(user.id, 5000)
            friend_ids.extend(ids)
        except:
            utils.print_query_error("get_friend_ids", user.id)
        finally:
            sleep(60)
    return friend_ids


# フォロワーの中で2016年以前の登録ユーザをフォロー数の降順に並べて
# 分析したアカウントをFriendインスタンスにしてリストで返す
def analysys_follower_friends_ex1():
    # 上限の5000人分取得
    follower_ids = tg.get_follower_ids(C.ANALYSYS_USER_ID, 50)
    followers = create_users_from_ids(user_ids=follower_ids, stage_num=1)

    # 2016年以前のユーザで絞り込み,
    # 非公開アカウントを弾き,
    # フォロー数の多い順で並べる
    followers = filter(lambda obj:obj.created_at.year < 2016, followers)
    followers = filter(lambda obj:obj.is_protected == False, followers)
    followers = sorted(followers, key=lambda obj: obj.friends_count, reverse=True)

    followers = followers[0:C.REQUIRE_FOLLOWER_COUNT]

    # フォロワーがフォローしている人
    friend_ids = create_friend_ids_from_users(users=followers, stage_num=2)

    # 一応メモリ解放
    del follower_ids
    del followers
    gc.collect()

    # フォロイーのIDをキーにして、フォロイーが何人にフォローされているかを格納
    friends_counter_dict = collections.Counter(friend_ids)

    del friend_ids
    gc.collect()

    my_prof = tg.get_user_profile(C.ANALYSYS_USER_ID)
    me_as_friend_obj = Friend(id=C.ANALYSYS_USER_ID,
                              name=my_prof['name'],
                              count=friends_counter_dict[C.ANALYSYS_USER_ID],
                              followers_count=my_prof['followers_count'],
                              bio=my_prof['description'].replace('\n', '').replace('\r', ''),
                              follow_rate=format(100, '.2f'),
                              follow_ratio=format(1, '.1f'),
                              factor=format(C.FACTOR_CONST, '.1f'))
    sleep(1)

    # フレンドのクラスの配列を作る
    # FIXME:ここも関数にしたかったが関数にしたらcountとidの挙動がおかしくなったので直書き
    friends = []
    step=0 # FIXME:辞書のループ用インデックス。friends_counter_dict.keys().index(key)で取りたかったが何故か無限ループするようになってしまったのでstepでやってる

    for key, value in friends_counter_dict.items():
        step += 1
        utils.print_step_log("CreateFriendList(stage3)", step, len(friends_counter_dict))
        # 何人以上のアカウントをとってくるか
        if value > C.MIN_COUNT_LIMIT:
            try:
                prof = tg.get_user_profile(key)

                # フォロー率、フォロー比、係数を計算
                follow_rate = float(value) / float(me_as_friend_obj.count)
                follow_ratio = float(prof['followers_count']) / float(me_as_friend_obj.followers_count)
                factor = follow_rate / follow_ratio * C.FACTOR_CONST

                friend = Friend(id=key,
                                name=prof['name'],
                                count=value,
                                followers_count=prof['followers_count'],
                                bio=prof['description'].replace('\n', '').replace('\r', ''),
                                follow_rate=format(follow_rate*100,'.2f'),
                                follow_ratio=format(follow_ratio, '.1f'),
                                factor=format(factor, '.1f'))
                friends.append(friend)
            except:
                utils.print_query_error("get_user_profile", key)
            sleep(1)

    # フォローされている数の昇順に並び替え
    friends = sorted(friends, key=lambda u: u.count, reverse=True)
    return friends
