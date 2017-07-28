import java.io.*;
import java.util.*;

public class Negaposi {
    public static void main(String args[]) {
        SentenceManager sentenceManager = new SentenceManager();
        sentenceManager.excute();
    }
}

/***
 * 文章管理クラス
 * ネガポジ判定したい文章をsentensesとして管理する
 **/
class SentenceManager {
    ArrayList<String> sentences;
    ArrayList<String> words;

    SentenceManager() {
        this.sentences = new ArrayList<String>();
        this.words = new ArrayList<String>();
    }

    void loadInput() {
        Scanner sc = new Scanner(System.in);
        System.out.println(sc.nextLine());
    }

    void loadSentences() {
        FileReader fr = null;
        BufferedReader br = null;
        try {
            File file = new File("tweets.txt");
            fr = new FileReader(file);
            br = new BufferedReader(fr);

            String line;
            while ((line = br.readLine()) != null) {
                this.sentences.add(line);
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
    }

    void createWords() {
        for (String s : this.sentences) {
            System.out.println(s);
        }
    }

    void excute() {
        this.loadSentences();
        this.createWords();
    }
}

/***
 * 感情単語感情極性対応辞書クラス
 * dictMapに[単語 -> 極性値]をもつ
 **/
class EmotionDict {
    HashMap<String, Double> dictMap;

    EmotionDict() {
        this.dictMap = new HashMap<String, Double>();
    }

    void loadDict() {
        FileReader fr = null;
        BufferedReader br = null;
        try {
            File file = new File("emo_dict_jp.txt");
            fr = new FileReader(file);
            br = new BufferedReader(fr);

            String line;
            while ((line = br.readLine()) != null) {
                String[] elements = line.split(":");
                String word = elements[0];
                double value = Double.parseDouble(elements[3]);
                this.dictMap.put(word, value);
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
    }

    void printDict() {
        for (String key : this.dictMap.keySet()) {
            System.out.println(key + " " + this.dictMap.get(key));
        }
    }
}
