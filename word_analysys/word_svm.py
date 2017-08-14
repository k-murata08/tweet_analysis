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

    tuned_parameters = [{'n_estimators': [10, 30, 50, 70, 90, 110, 130, 150], 'max_features': ['auto', 'sqrt', 'log2', None]}]

    clf = GridSearchCV(RandomForestClassifier(), tuned_parameters, cv=2, scoring='accuracy', n_jobs=-1)
    clf.fit(data_train, label_train)

    print "ベストパラメタを表示"
    print clf.best_estimator_

    print("トレーニングデータでCVした時の平均スコア")
    for params, mean_score, all_scores in clf.grid_scores_:
        print "{:.3f} (+/- {:.3f}) for {}".format(mean_score, all_scores.std() / 2, params)

    y_true, y_pred = label_test, clf.predict(data_test)
    print classification_report(y_true, y_pred)

    #dic = corpora.Dictionary(training_x)

    # 単語辞書から出現頻度の少ない単語及び出現頻度の多すぎる単語を排除
    #dic.filter_extremes(no_below=5, no_above=0.3)

    # Bag of Wordsベクトルの作成

    #bow_corpus = [dic.doc2bow(d) for d in documents]

    # TF-IDFによる重み付け
    #tfidf_model = models.TfidfModel(bow_corpus)
    #tfidf_corpus = tfidf_model[bow_corpus]

    # LSIによる次元削減
    #lsi_model = models.LsiModel(tfidf_corpus, id2word=dic, num_topics=1000)
    #lsi_corpus = lsi_model[tfidf_corpus]

    #svc = svm.SVC()
    #cs = [0.001, 0.01, 0.1, 1]
    #gammas = [0.001, 0.01, 0.1, 1]
    #parameters = {'kernel': ['rbf'], 'C': cs, 'gamma': gammas}
    #clf = grid_search.GridSearchCV(svc, parameters)
    #clf.fit(tfidf_corpus, training_y)


    #score = clf.score(test_x, test_y)
    #print ('Test score: ' + str(score))


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
