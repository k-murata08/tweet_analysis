import java.io.*;
import java.util.*;

public class Negaposi {
    public static void main(String args[]) {
        excute();
    }

    static void excute() {
        SentenceManager sentenceManager = new SentenceManager("tweets.txt");
        ArrayList<String> sentences = sentenceManager.loadSentences();

        EmotionDict emotionDict = new EmotionDict("emo_dict_jp.txt");
        HashMap<String, Double> dictMap = emotionDict.loadDict();

        for (String sentence : sentences) {
            ArrayList<String> words = sentenceManager.createWords(sentence);
            double score = 0;
            for (String word : words) {
                if (word.length() == 1) {
                    continue;
                }
                if (dictMap.containsKey(word)) {
                    score += dictMap.get(word);
                    System.out.println("sentence: " + sentence);
                    System.out.println(word);
                }
            }
            if (score != 0) {
                System.out.println("score: " + String.valueOf(score));
            }
        }
    }
}

/***
 * 文章管理クラス
 * ネガポジ判定したい文章をsentensesとして管理する
 **/
class SentenceManager {
    File file;
    int wordMaxLength = 12;

    SentenceManager(String filename) {
        this.file = new File(filename);
    }

    /***
     * テキストファイルから文を読み込む
     * return ArrayList<String> sentences (文章リスト)
     **/
    ArrayList<String> loadSentences() {
        ArrayList<String> sentences = new ArrayList<String>();
        FileReader fr = null;
        BufferedReader br = null;
        try {
            fr = new FileReader(this.file);
            br = new BufferedReader(fr);

            String line;
            while ((line = br.readLine()) != null) {
                if (!line.trim().equals("")) {
                    sentences.add(line);
                }
            }
        } catch(FileNotFoundException e) {
            System.out.println(e);
        } catch(IOException e) {
            System.out.println(e);
        } finally {
            try {
                br.close();
                fr.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return sentences;
    }

    /***
     * 文章から、単語配列を作成
     * return ArrayList<String> words (単語リスト)
     **/
    ArrayList<String> createWords(String sentence) {
        ArrayList<String> words = new ArrayList<String>();
        for (int wlen = 1; wlen <= this.wordMaxLength; wlen++) {
            for (int i = 0; i < sentence.length() - wlen + 1; i++) {
                String word = sentence.substring(i, i + wlen).trim();
                if (word.length() != 0) {
                    words.add(word);
                }
            }
        }
        return words;
    }
}

/***
 * 感情単語感情極性対応辞書クラス
 * dictMapに[単語 -> 極性値]をもつ
 **/
class EmotionDict {
    File file;
    EmotionDict(String filename) {
        this.file = new File(filename);
    }

    HashMap<String, Double> loadDict() {
        HashMap<String, Double> dictMap = new HashMap<String, Double>();
        FileReader fr = null;
        BufferedReader br = null;
        try {
            fr = new FileReader(this.file);
            br = new BufferedReader(fr);

            String line;
            while ((line = br.readLine()) != null) {
                String[] elements = line.split(":");
                String word = elements[0];
                double value = Double.parseDouble(elements[3]);
                dictMap.put(word, value);
            }
        } catch(FileNotFoundException e) {
            System.out.println(e);
        } catch(IOException e) {
            System.out.println(e);
        } finally {
            try {
                br.close();
                fr.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return dictMap;
    }
}
