#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import twitter_analysis_func as ta
import time


def run_analysys_ex1():
    friends = ta.analysys_follower_friends_ex1(400, 20)

    # ログだと見辛いのでとりあえず今はCSVに書き出す
    with open('follower_analytics.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["ID", "Name", "Count", "FollowersCount", "Bio"]
        writer.writerow(header)

        for friend in friends:
            print str(friend.id) + " " + friend.name
            row = [friend.id, unicode(friend.name).encode("utf-8"), friend.count, friend.followers_count, unicode(friend.bio).encode("utf-8")]
            writer.writerow(row)


# 実行用
def main():
    start_time = time.time()

    run_analysys_ex1()

    elapsed_time = time.time() - start_time
    print ("elapsed_time:{0}".format(int(elapsed_time))) + "[sec]"


if __name__ == "__main__":
    main()
