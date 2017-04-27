#!/usr/bin/env python
# -*- coding: utf-8 -*-

# $ python user_check.py [ユーザID]
# で指定するとユーザのプロフィール情報をターミナル上に吐く

import sys
import twitter_generic_func as tg


def print_profile(user_id):
    prof = tg.get_user_profile(user_id)
    for key, value in prof.items():
        print key, value


def main():
    args = sys.argv
    print_profile(args[1])


if __name__ == "__main__":
    main()
