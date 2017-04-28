#!/usr/bin/env python
# -*- coding: utf-8 -*-

OATH_KEY_DICT = {
    "consumer_key": "lb26YD9K7h8JhNRFeGJlshWGX",
    "consumer_secret": "tcy6LZReXwELPtNBYk9MYz15w03kEJFdwmASdMaWRDzlQrhheV",
    "access_token": "1349624660-5fmFKCqnHaXTUMxyy9ESaCYYs65tZzXZqb5FWK3",
    "access_token_secret": "ifbZ4YwN2WIi6M8lpenyx2H9tWwWSFth3GMfU8K4AthTl"
}

# 分析するユーザのID
ANALYSYS_USER_ID = 740776275527237633

# フォロワーのうち、上位何人について分析するか
REQUIRE_FOLLOWER_COUNT = 5

# CSVに書き出すのはCountが最低いくつ以上のユーザか
MIN_COUNT_LIMIT = 2

# 係数用定数
FACTOR_CONST = 1000
