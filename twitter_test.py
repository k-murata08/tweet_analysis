#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import twitter_analysis_func as ta
import const


def run_analysys_base():
    friends = ta.analysys_follower_friends()

    # ログだと見辛いのでとりあえず今はCSVに書き出す
    with open('follower_analytics.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["ID", "Name", "Count", "Bio"]
        writer.writerow(header)

        for friend in friends:
            print str(friend.id) + " " + friend.name
            row = [str(friend.id), unicode(friend.name).encode("utf-8"), str(friend.count), unicode(friend.bio).encode("utf-8")]
            writer.writerow(row)


def run_analysys_ex1():
    friends = ta.analysys_follower_friends_ex1()

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
    run_analysys_ex1()


if __name__ == "__main__":
    main()
