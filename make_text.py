#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import traceback

import twitter_generic_func as tg
import twitter_analysis_func as ta
import const as C
import utils
import time
import csv


# フォロワーのツイートをテキストファイルに吐き出す
def make_follower_text():
    follower_ids = ta.get_follower_ids(C.ANALYSYS_USER_ID)
    followers = ta.improved_create_users_from_ids(user_ids=follower_ids)

    # 非公開アカウントを弾き,
    # フォロー数の多い順で並べる
    followers = filter(lambda obj:obj.created_at.year <= C.VALID_USER_MAX_CREATED_AT , followers)
    followers = filter(lambda obj:obj.is_protected == False, followers)
    followers = sorted(followers, key=lambda obj: obj.friends_count, reverse=True)

    texts = []
    for index, follower in enumerate(followers):
        utils.print_step_log("CreateText", index, len(followers))
        try:
            follower_tweets = tg.get_user_timeline(user_id=follower.id, tweets_count=C.TWEETS_COUNT_FOR_MAKE_TEXT, include_rts=False)
            if follower_tweets is not None:
                for tweet in follower_tweets:
                    texts.append(tweet['text'])

        except:
            traceback.print_exc()
        sleep(1)

    with open('tweets.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["tweet", "label"]
        writer.writerow(header)

        for text in texts:
            row = [unicode(text).encode('utf-8'), 1]
            writer.writerow(row)


if __name__ == "__main__":
    start_time = time.time()
    make_follower_text()
    elapsed_time = time.time() - start_time
    print "Output file is [tweets.csv]"
    print ("elapsed_time:{0}".format(int(elapsed_time))) + "[sec]\n"
