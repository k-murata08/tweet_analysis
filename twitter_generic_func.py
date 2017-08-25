#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
import const as C

def get_followers(user_id, users_count):
    """15分間に15回回せる"""
    url = "https://api.twitter.com/1.1/followers/list.json?"
    params = {
        "user_id": user_id,
        "count": users_count
        }
    oath = create_oath_session(C.OATH_KEY_DICT)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    followers = json.loads(responce.text, 'utf-8')
    return followers['users']


def get_follower_ids(user_id, users_count, cursor):
    """
    15分間に15回回せる
    フォロワーidsとページングに使うnext_cursorが返る。次のページがないときにはnext_cursorは0で返る
    最初はcursorに-1を設定
    """
    url = "https://api.twitter.com/1.1/followers/ids.json?"
    params = {
        "user_id": user_id,
        "count": users_count,
        "cursor": cursor
        }
    oath = create_oath_session(C.OATH_KEY_DICT)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    follower_ids = json.loads(responce.text, 'utf-8')
    return [follower_ids['ids'], follower_ids['next_cursor']]


def get_friends(user_id, users_count):
    """
    15分間に15回回せる
    user_idのユーザがフォローしているユーザ
    """
    url = "https://api.twitter.com/1.1/friends/list.json?"
    params = {
        "user_id": user_id,
        "count": users_count
        }
    oath = create_oath_session(C.OATH_KEY_DICT)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    friends = json.loads(responce.text, 'utf-8')
    return friends['users']


def get_friend_ids(user_id, users_count, cursor):
    """15分間に15回回せる"""
    url = "https://api.twitter.com/1.1/friends/ids.json?"
    params = {
        "user_id": user_id,
        "count": users_count,
        "cursor": cursor
        }
    oath = create_oath_session(C.OATH_KEY_DICT)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    friend_ids = json.loads(responce.text, 'utf-8')
    return [friend_ids['ids'], friend_ids['next_cursor']]


def get_user_profile(user_id):
    """15分間に900回回せる"""
    url = "https://api.twitter.com/1.1/users/show.json?"
    params = {
        "user_id": user_id,
        "include_entities": False
        }
    oath = create_oath_session(C.OATH_KEY_DICT)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    profile = json.loads(responce.text, 'utf-8')
    return profile


def get_user_profiles(user_ids):
    """15分間に900回回せる"""
    url = "https://api.twitter.com/1.1/users/lookup.json?"
    params = {
        "user_id": user_ids,
        "include_entities": False
        }
    oath = create_oath_session(C.OATH_KEY_DICT)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    profiles = json.loads(responce.text, 'utf-8')
    return profiles


def get_user_timeline(user_id, tweets_count, include_rts):
    """15分間に900回回せる"""
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
    params = {
        "user_id": user_id,
        "trim_user": True,
        "count": tweets_count,
        "exclude_replies": True,
        "include_rts": include_rts
        }
    oath = create_oath_session(C.OATH_KEY_DICT)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    timeline = json.loads(responce.text, 'utf-8')
    return timeline


def get_favorite_tweets(user_id, count):
    """15分間に75回回せる(1回200件が上限)"""
    url = "https://api.twitter.com/1.1/favorites/list.json?"
    params = {
        "user_id": user_id,
        "count": count,
        "include_entities": False
    }
    oath = create_oath_session(C.OATH_KEY_DICT)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    favolites = json.loads(responce.text, 'utf-8')
    return favolites


def get_tweet(tweet_id):
    """
    ツイートの詳細を取得
    15分間に900回回せる
    """
    url = "https://api.twitter.com/1.1/statuses/show.json?"
    params = {
        "id": tweet_id,
        "include_my_retweet": False,
        "include_entities": False
    }
    oath = create_oath_session(C.OATH_KEY_DICT)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    tweet = json.loads(responce.text, 'utf-8')
    return tweet


def create_oath_session(oath_key_dict):
    """クエリを飛ばす時にしか使わない"""
    oath = OAuth1Session(
        oath_key_dict["consumer_key"],
        oath_key_dict["consumer_secret"],
        oath_key_dict["access_token"],
        oath_key_dict["access_token_secret"]
    )
    return oath
