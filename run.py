#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import twitter_analysis_func as ta
import time
import sys
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def run_analysys_followee():
    friends = ta.analysys_follower_friends()

    # ログだと見辛いのでとりあえず今はCSVに書き出す
    with open('follower_analytics.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["ID", "Name", "Count", "FollowersCount", "Bio", "FollowRate[%]", "FollowerRatio", "Factor"]
        writer.writerow(header)

        pltleft = []
        pltheight = []
        pltlabels = []

        for i, friend in enumerate(friends):
            if i < 5:
                pltleft.append(i)
                pltheight.append(friend.count)
                pltlabels.append(friend.name)

            row = [friend.id,
                   unicode(friend.name).encode("utf-8"),
                   friend.count,
                   friend.followers_count,
                   unicode(friend.bio).encode("utf-8"),
                   friend.follow_rate,
                   friend.follow_ratio,
                   friend.factor]
            writer.writerow(row)

        # グラフ設定
        fp = FontProperties(fname='/Users/murata.kazuma/Library/Fonts/ipag.ttf')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(pltleft, pltheight)
        ax.set_xticks(pltleft)
        ax.set_xticklabels(pltlabels, rotation=45)
        for label in ax.get_xticklabels():
            label.set_fontproperties(fp)
        fig.tight_layout()
        plt.savefig('followee_analitics.png')


def run_analysys_morpheme():
    morphemes = ta.analysys_follower_morpheme()

    # ログだと見辛いのでとりあえず今はCSVに書き出す
    with open('follower_analytics_mopheme.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["UserID", "Word", "Class", "Count"]
        writer.writerow(header)

        for morpheme in morphemes:
            row = [morpheme.user_id, morpheme.word, morpheme.hinshi, morpheme.count]
            writer.writerow(row)


def run_analysys_favorite():
    favorites = ta.analysys_follower_favorite()

    with open('follower_analytics_favorite.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["TweetID", "Count", "Text", "UserName"]
        writer.writerow(header)

        for favorite in favorites:
            row = [
                favorite.tweet_id,
                favorite.count,
                unicode(favorite.text).encode("utf-8"),
                unicode(favorite.tweet_user_name).encode("utf-8")
            ]
            writer.writerow(row)


def run_analysys_retweet():
    retweets = ta.analysys_follower_retweet()

    with open('follower_analytics_retweet.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["TweetID", "Count", "Text"]
        writer.writerow(header)

        for retweet in retweets:
            row = [
                retweet.tweet_id,
                retweet.count,
                unicode(retweet.text).encode('utf-8')
            ]
            writer.writerow(row)


def run_search_tweet(word):
    tweets = ta.search_follower_tweets(word)

    with open('follower_search_tweet.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["TweetID", "Text"]
        writer.writerow(header)

        for tweet in tweets:
            row = [
                tweet.tweet_id,
                unicode(tweet.text).encode('utf-8')
            ]
            writer.writerow(row)


# 実行用
def main():
    start_time = time.time()

    if sys.argv[1] == "followee":
        run_analysys_followee()
    elif sys.argv[1] == "morpheme":
        run_analysys_morpheme()
    elif sys.argv[1] == "favorite":
        run_analysys_favorite()
    elif sys.argv[1] == "retweet":
        run_analysys_retweet()
    elif sys.argv[1] == "tweet":
        if sys.argv[2] is None:
            print "prease input word"
        else:
            run_search_tweet(sys.argv[2])
    else:
        print "Invalid Argument."
        print "Collect is followee or morpheme."

    elapsed_time = time.time() - start_time
    print ("elapsed_time:{0}".format(int(elapsed_time))) + "[sec]\n"


if __name__ == "__main__":
    main()
