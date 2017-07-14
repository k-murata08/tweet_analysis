#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
from time import sleep
from datetime import datetime as dt
import collections
import traceback

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


class Favorite:
    def __init__(self, tweet_id, count, text, tweet_user_name):
        self.tweet_id = tweet_id
        self.count = count
        self.text = text
        self.tweet_user_name = tweet_user_name


class Morpheme:
    def __init__(self, user_id, word, hinshi, count):
        self.user_id = user_id
        self.word = word
        self.hinshi = hinshi
        self.count = count


class Tweet:
    def __init__(self, tweet_id, text, count):
        self.id = tweet_id
        self.text = text
        self.count = count


def create_users_from_ids(user_ids):
    users = []
    for index, user_id in enumerate(user_ids):
        utils.print_step_log("CreateUsersList", index, len(user_ids))
        try:
            prof = tg.get_user_profile(user_id)
        except:
            traceback.print_exc()
            sleep(1)
            continue

        if prof == None or prof == []:
            sleep(1)
            continue

        user = User(
            id=prof['id'],
            name=prof['name'],
            description=prof['description'],
            friends_count=prof['friends_count'],
            created_at=dt.strptime(prof['created_at'], "%a %b %d %H:%M:%S +0000 %Y"),
            is_protected=prof['protected']
        )
        users.append(user)
        sleep(1)

    return users


def get_favorites_from_users(users):
    favorite_tweet_ids = []
    for index, user in enumerate(users):
        utils.print_step_log("CreateFavoritesList", index, len(users))
        try:
            favs = tg.get_favorite_tweets(user.id, 200)
        except:
            traceback.print_exc()
            sleep(12)
            continue

        if favs == None or favs == []:
            sleep(12)
            continue

        for fav in favs:
            favorite_tweet_ids.append(fav['id'])
        sleep(12)

    return favorite_tweet_ids


# 時間が100分の1になったやつ(プロフィールのクエリだけまとめてIDを飛ばせることに気づいた)
def improved_create_users_from_ids(user_ids):
    users = []
    user_ids_list = utils.split_list(user_ids, 100)
    for index, ids in enumerate(user_ids_list):
        utils.print_step_log("CreateUsersList", index, len(user_ids_list))
        try:
            profs = tg.get_user_profiles(ids)
        except:
            traceback.print_exc()
            sleep(1)
            continue

        if profs == None or profs == []:
            continue

        for prof in profs:
            user = User(
                id=prof['id'],
                name=prof['name'],
                description=prof['description'],
                friends_count=prof['friends_count'],
                created_at=dt.strptime(prof['created_at'], "%a %b %d %H:%M:%S +0000 %Y"),
                is_protected=prof['protected']
            )
            users.append(user)
        sleep(1)

    return users


# usersたちのフォロイーのID(重複可)のリストを生成
def create_friend_ids_from_users(users):
    friend_ids = []

    for index, user in enumerate(users):
        utils.print_step_log("CreateFriendID", index, len(users))
        cursor = -1
        # 一回のフォロイーID取得上限が5000件なので、5000件以上あればループ
        for i in range(10):
            try:
                ids_cursor = tg.get_friend_ids(user.id, 5000, cursor)
            except:
                traceback.print_exc()
                break

            if ids_cursor == None or ids_cursor == []:
                break

            friend_ids.extend(ids_cursor[0])
            cursor = ids_cursor[1]
            if cursor == 0:
                break
            print "Friend count over 5000 creating..."
            sleep(60)

    return friend_ids


def get_follower_ids(user_id):
    follower_ids = []
    cursor = -1

    # 一回のフォロワーID取得上限が5000件なので、5000件以上あればループs
    for i in range(10):
        print "CreateFollowerIDs"
        try:
            f_ids_cursor = tg.get_follower_ids(user_id, 5000, cursor)
        except:
            traceback.print_exc()
            break

        if f_ids_cursor == None or f_ids_cursor == []:
            break

        follower_ids.extend(f_ids_cursor[0])
        if f_ids_cursor[1] == 0: # 全てのfollower_idsを取得したらbreak
            break
        cursor = f_ids_cursor[1]
        sleep(1)

    return follower_ids


# フォロワーの中で2016年以前の登録ユーザをフォロー数の降順に並べて
# 分析したアカウントをFriendインスタンスにしてリストで返す
def analysys_follower_friends():
    follower_ids = get_follower_ids(user_id=C.ANALYSYS_USER_ID)
    followers = improved_create_users_from_ids(user_ids=follower_ids)

    # 2016年以前のユーザで絞り込み,
    # 非公開アカウントを弾き,
    # フォロー数の多い順で並べる
    followers = filter(lambda obj:obj.created_at.year <= C.VALID_USER_MAX_CREATED_AT, followers)
    followers = filter(lambda obj:obj.is_protected == False, followers)
    followers = sorted(followers, key=lambda obj: obj.friends_count, reverse=True)

    followers = followers[0:C.REQUIRE_FOLLOWER_COUNT]

    # フォロワーがフォローしている人
    friend_ids = create_friend_ids_from_users(users=followers)

    # 一応メモリ解放
    del follower_ids
    del followers
    gc.collect()

    # フォロイーのIDをキーにして、フォロイーが何人にフォローされているかを格納
    friends_counter_dict = collections.Counter(friend_ids)

    del friend_ids
    gc.collect()

    # 自分をFriendオブジェクトに登録するのは係数計算の部分で情報が必要なため
    my_prof = tg.get_user_profile(C.ANALYSYS_USER_ID)
    me_as_friend_obj = Friend(
        id=C.ANALYSYS_USER_ID,
        name=my_prof['name'],
        count=friends_counter_dict[C.ANALYSYS_USER_ID],
        followers_count=my_prof['followers_count'],
        bio=my_prof['description'].replace('\n', '').replace('\r', ''),
        follow_rate=100.00,
        follow_ratio=1.0,
        factor=C.FACTOR_CONST
    )
    sleep(1)

    # フレンドのクラスの配列を作る
    # FIXME:ここも関数にしたかったが関数にしたらcountとidの挙動がおかしくなったので直書き
    friends = []
    step=0 # FIXME:辞書のループ用インデックス。friends_counter_dict.keys().index(key)で取りたかったが何故か無限ループするようになってしまったのでstepでやってる

    for key, value in friends_counter_dict.items():
        step += 1
        utils.print_step_log("CreateFriendList", step, len(friends_counter_dict))
        # 何人以上のアカウントをとってくるか
        if value <= C.MIN_COUNT_LIMIT:
            continue

        try:
            prof = tg.get_user_profile(key)
        except:
            traceback.print_exc()
            sleep(1)
            continue

        if prof == None or prof == []:
            sleep(1)
            continue

        # フォロー率、フォロー比、係数を計算
        if me_as_friend_obj.count != 0:
            follow_rate = float(value) / float(me_as_friend_obj.count)
        else:
            follow_rate = 0

        if me_as_friend_obj.followers_count != 0:
            follow_ratio = float(prof['followers_count']) / float(me_as_friend_obj.followers_count)
        else:
            follow_ratio = 0

        if follow_ratio != 0:
            factor = follow_rate / follow_ratio * C.FACTOR_CONST
        else:
            factor = 0

        friend = Friend(
            id=key,
            name=prof['name'],
            count=value,
            followers_count=prof['followers_count'],
            bio=prof['description'].replace('\n', '').replace('\r', ''),
            follow_rate=round(follow_rate*100, 2),
            follow_ratio=round(follow_ratio, 1),
            factor=round(factor, 1)
        )
        friends.append(friend)
        sleep(1)

    # フォローされている数の降順に並び替え
    friends = sorted(friends, key=lambda u: u.count, reverse=True)
    return friends


# フォロワーのツイートを形態素解析して、単語の多い順のMorpheme(形態素)クラスで返す
def analysys_follower_morpheme():
    follower_ids = get_follower_ids(C.ANALYSYS_USER_ID)
    followers = improved_create_users_from_ids(user_ids=follower_ids)

    # 2016年以前のユーザで絞り込み,
    # 非公開アカウントを弾き,
    # フォロー数の多い順で並べる
    followers = filter(lambda obj:obj.created_at.year <= C.VALID_USER_MAX_CREATED_AT , followers)
    followers = filter(lambda obj:obj.is_protected == False, followers)
    followers = sorted(followers, key=lambda obj: obj.friends_count, reverse=True)

    followers = followers[0:C.REQUIRE_FOLLOWER_COUNT]

    # 全followersの指定した数のツイートを形態素解析して重複考えずに全部word_listにぶち込む。対応する品詞もhinshi_listにぶち込む
    word_list = []
    hinshi_list = []
    user_id_list = []

    for index, follower in enumerate(followers):
        utils.print_step_log("CreateWordList", index, len(followers))
        try:
            follower_tweets = tg.get_user_timeline(user_id=follower.id, tweets_count=C.TWEETS_COUNT_PER_USER)
        except:
            traceback.print_exc()
            sleep(1)
            continue

        if follower_tweets == None or follower_tweets == []:
            sleep(1)
            continue

        tweet_texts = [tweet['text'] for tweet in follower_tweets]

        # followerのツイートを形態素解析してword_listに入れる
        for text in tweet_texts:
            text = text.encode('utf-8').replace('\n', '').replace('\r', '').strip()
            keitaiso_list = utils.get_keitaiso_list_from_juman(text)

            word_list.extend(keitaiso_list[0])
            hinshi_list.extend(keitaiso_list[1])
            user_id_list.extend([follower.id] * len(keitaiso_list[0]))

        sleep(1)

    # 形態素と品詞を紐づけたまま単語数を数えたいので"形態素/品詞"の文字列で1単語とする
    word_hinshi_list = []

    # 一つの単語を”単語/品詞/ユーザID”の形にする
    for word, hinshi, user_id in zip(word_list, hinshi_list, user_id_list):
        word_hinshi_list.append(word + "/" + hinshi + "/" + str(user_id))

    # 単語をキーにして、単語が何回登場したかを辞書に格納
    word_counter_dict = collections.Counter(word_hinshi_list)

    morphemes = []
    for key, value in word_counter_dict.items():
        if value < C.MIN_WORD_COUNT:
            continue

        # 形態素と品詞とuser_idを分ける
        # rsplitにすることで、もし"htt:///名詞"みたいな文字列があってもちゃんと分けられる
        splited_key = key.rsplit("/", 2)
        morphemes.append(Morpheme(user_id=splited_key[2], word=splited_key[0], hinshi=splited_key[1], count=value))

    # ユーザ毎にまとめ、単語出現回数の多い順に並べて返す
    morphemes = sorted(morphemes, key=lambda u: (u.user_id, u.count), reverse=True)
    return morphemes


def analysys_follower_favorite():
    follower_ids = get_follower_ids(user_id=C.ANALYSYS_USER_ID)
    followers = improved_create_users_from_ids(user_ids=follower_ids)

    # 2016年以前のユーザで絞り込み,
    # 非公開アカウントを弾き,
    # フォロー数の多い順で並べる
    followers = filter(lambda obj:obj.created_at.year <= C.VALID_USER_MAX_CREATED_AT , followers)
    followers = filter(lambda obj:obj.is_protected == False, followers)
    followers = sorted(followers, key=lambda obj: obj.friends_count, reverse=False)
    followers = followers[0:C.REQUIRE_FOLLOWER_COUNT]

    favorites = get_favorites_from_users(followers)

    # ファボツイートのIDをキーにして、ファボツイートが何人にファボされているかを格納
    favorites_counter_dict = collections.Counter(favorites)

    favorites = []
    step=0
    for key, value in favorites_counter_dict.items():
        utils.print_step_log("GetFavosTweet", step, len(favorites_counter_dict))
        step += 1
        if value < C.MIN_FAVORITE_COUNT_LIMIT:
            continue

        try:
            tweet = tg.get_tweet(key)
        except:
            traceback.print_exc()
            sleep(1)
            continue

        if tweet == None or tweet == []:
            sleep(1)
            continue

        favorite = Favorite(tweet_id=key, count=value, text=tweet['text'], tweet_user_name=tweet['user']['name'])
        favorites.append(favorite)
        sleep(1)

    favorites = sorted(favorites, key=lambda u: u.count, reverse=True)
    return favorites


def analysys_follower_retweet():
    follower_ids = get_follower_ids(user_id=C.ANALYSYS_USER_ID)
    followers = improved_create_users_from_ids(user_ids=follower_ids)

    # 2016年以前のユーザで絞り込み,
    # 非公開アカウントを弾き,
    # フォロー数の多い順で並べる
    followers = filter(lambda obj:obj.created_at.year <= C.VALID_USER_MAX_CREATED_AT , followers)
    followers = filter(lambda obj:obj.is_protected == False, followers)
    followers = sorted(followers, key=lambda obj: obj.friends_count, reverse=False)
    followers = followers[0:C.REQUIRE_FOLLOWER_COUNT]

    retweet_ids = []
    for index, follower in enumerate(followers):
        utils.print_step_log("CreateRetweetList", index, len(followers))
        try:
            follower_tweets = tg.get_user_timeline(user_id=follower.id, tweets_count=C.TWEETS_COUNT_PER_USER)
            follower_retweets = filter(lambda obj:obj.has_key("retweeted_status"), follower_tweets)
            retweet_tweets = [retweet["retweeted_status"] for retweet in follower_retweets]
        except:
            traceback.print_exc()
            sleep(1)
            continue

        if retweet_tweets == None or retweet_tweets == []:
            sleep(1)
            continue

        ids = [retweet['id'] for retweet in retweet_tweets]
        retweet_ids.extend(ids)
        sleep(1)

    retweet_counter_dict = collections.Counter(retweet_ids)

    retweets = []
    step = 0
    for key, value in retweet_counter_dict.items():
        utils.print_step_log("GetTweet", step, len(retweet_counter_dict))
        step += 1
        if value < C.MIN_RETWEET_COUNT_LIMIT:
            continue

        try:
            tweet = tg.get_tweet(key)
        except:
            traceback.print_exc()
            sleep(1)
            continue

        if tweet == None or tweet == []:
            sleep(1)
            continue

        tweet = Tweet(tweet_id=key, count=value, text=tweet['text'])
        retweets.append(tweet)
        sleep(1)

    retweets  = sorted(retweets, key=lambda obj:obj.count, reverse=True)
    return retweets
