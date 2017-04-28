#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import twitter_analysis_func as ta
import time
import const as C


def run_analysys():
    friends = ta.analysys_follower_friends_ex1()

    # ログだと見辛いのでとりあえず今はCSVに書き出す
    with open('follower_analytics.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["ID", "Name", "Count", "FollowersCount", "Bio", "FollowRate[%]", "FollowerRatio", "Factor"]
        writer.writerow(header)

        for friend in friends:
            row = [friend.id,
                   unicode(friend.name).encode("utf-8"),
                   friend.count,
                   friend.followers_count,
                   unicode(friend.bio).encode("utf-8"),
                   friend.follow_rate,
                   friend.follow_ratio,
                   friend.factor]
            writer.writerow(row)


# 実行用
def main():
    start_time = time.time()

    run_analysys()

    elapsed_time = time.time() - start_time
    print ("elapsed_time:{0}".format(int(elapsed_time))) + "[sec]\n"


if __name__ == "__main__":
    main()
