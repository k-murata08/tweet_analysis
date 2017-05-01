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

# --------- 共通 ------------------
REQUIRE_FOLLOWER_COUNT = 30  # フォロワーのうち、上位何人について分析するか(フォロイーの多い順)
VALID_USER_MAX_CREATED_AT = 2015 # 何年までに登録されたユーザで絞り込むか
# ----------------------------------

# --------- フォロワーのフォロイー分析-------------------------
MIN_COUNT_LIMIT = 2          # CSVに書き出すのはCountが最低いくつ以上のユーザか
FACTOR_CONST = 1000          # 係数用定数
# -------------------------------------------------------------

# --------- フォロワーのツイートの形態素解析分析---------------
TWEETS_COUNT_PER_USER = 20    # フォロワー1人あたり幾つの最新ツイートを取得するか
VALID_WORD_CLASS = ["名詞", "形容詞", "動詞"] # 有効な形態素の品詞
MIN_WORD_COUNT = 3 # countがいくつ以上のワードをcsvに吐き出すか
# -------------------------------------------------------------
