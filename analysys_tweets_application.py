#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import twitter_analysis_func as ta
import time
import const as C


def run_analysys():
    morphemes = ta.analysys_follower_morpheme()

    # ログだと見辛いのでとりあえず今はCSVに書き出す
    with open('follower_analytics_mopheme.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        header = ["Word", "Count"]
        writer.writerow(header)

        for morpheme in morphemes:
            print str(morpheme.word) + " " + morpheme.count
            row = [unicode(morpheme.word).encode("utf-8"),
                   morpheme.count]
            writer.writerow(row)


# 実行用
def main():
    start_time = time.time()

    run_analysys()

    elapsed_time = time.time() - start_time
    print ("elapsed_time:{0}".format(int(elapsed_time))) + "[sec]"


if __name__ == "__main__":
    main()
