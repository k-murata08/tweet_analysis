#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import traceback

import twitter_generic_func as tg
import twitter_analysis_func as ta
import const as C
import utils


class User:
    def __init__(self, id, name, description, friends_count, created_at, is_protected):
        self.id = id
        self.name = name
        self.description = description
        self.friends_count = friends_count
        self.created_at = created_at
        self.is_protected = is_protected


# フォロワーのツイートをテキストファイルに吐き出す
def make_follower_text():
    follower_ids = ta.get_follower_ids(C.ANALYSYS_USER_ID)
    followers = ta.improved_create_users_from_ids(user_ids=follower_ids)

    # 2016年以前のユーザで絞り込み,
    # 非公開アカウントを弾き,
    # フォロー数の多い順で並べる
    followers = filter(lambda obj:obj.created_at.year <= C.VALID_USER_MAX_CREATED_AT , followers)
    followers = filter(lambda obj:obj.is_protected == False, followers)
    followers = sorted(followers, key=lambda obj: obj.friends_count, reverse=True)

    followers = followers[0:C.REQUIRE_FOLLOWER_COUNT]

    texts = []
    for index, follower in enumerate(followers):
        utils.print_step_log("CreateText", index, len(followers))
        try:
            follower_tweets = tg.get_user_timeline(user_id=follower.id, tweets_count=C.TWEETS_COUNT_FOR_MAKE_TEXT, include_rts=False)
        except:
            traceback.print_exc()
            sleep(1)
            continue

        for tweet in follower_tweets:
            texts.append(tweet['text'])

    with open('tweets.txt', 'w') as f:
        for text in texts:
            f.write(unicode(text).encode('utf-8'))
            f.write('\n')


if __name__ == "__main__":
    make_follower_text()
