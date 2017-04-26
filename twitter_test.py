#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import twitter_analysis_func as ta
import const

# 実行用
def main():
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


if __name__ == "__main__":
    main()
