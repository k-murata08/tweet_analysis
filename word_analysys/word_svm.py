# -*- coding: utf-8 -*-

import csv
from natto import MeCab
from gensim import corpora, models, matutils
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def main():
    document_words = list()
    document_labels = list()

    count = 0
    with open('tweets_label.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            document_words.append(parse_word_list(row[0]))
            document_labels.append(row[1])
            count += 1
            if count == 1000:
                break

    dictionary = corpora.Dictionary(document_words)
    dictionary.filter_extremes(no_below=3, no_above=0.4)

    vecs = list()
    for wordlist in document_words:
        bow = dictionary.doc2bow(wordlist)
        dense = list(matutils.corpus2dense([bow], num_terms=len(dictionary)).T[0])
        vecs.append(dense)

    data_train, data_test, label_train, label_test = train_test_split(vecs, document_labels, test_size=0.3)

    tuned_parameters = [
        {
            'n_estimators': [5, 10, 30, 50, 70, 90, 130, 300],
            'max_features': ['auto', 'sqrt', 'log2', None],
            'n_jobs': [1],
            'random_state': [0],
            'min_samples_split': [3, 5, 10, 15, 20, 25, 30, 40, 50, 100],
            'max_depth': [3, 5, 10, 15, 20, 25, 30, 40, 50, 100]
        }
    ]

    clf = GridSearchCV(RandomForestClassifier(), tuned_parameters, cv=2, scoring='accuracy')
    clf.fit(data_train, label_train)

    print "ベストパラメタを表示"
    print clf.best_estimator_
    print ""

    print("トレーニングデータでCVした時の平均スコア")
    for params, mean_score, all_scores in clf.grid_scores_:
        print "{:.3f} (+/- {:.3f}) for {}".format(mean_score, all_scores.std() / 2, params)
    print ""

    y_true, y_pred = label_test, clf.predict(data_test)
    print classification_report(y_true, y_pred)


def parse_word_list(text):
    words = list()
    nm = MeCab()
    with MeCab('-F%m,%f[0]') as nm:
        for n in nm.parse(text, as_nodes=True):
            node = n.feature.split(',');
            if node[0] != 'EOS' and is_valid_speech(node[1]):
                words.append(node[0])

    return words


def is_valid_speech(hinshi):
    if hinshi in ['名詞', '形容詞', '動詞', '記号']:
        return True
    return False


if __name__ == "__main__":
    main()
