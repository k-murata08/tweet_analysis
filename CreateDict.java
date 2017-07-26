import java.io.*;
import java.util.*;

public class CreateDict {
    public static void main(String[] args) {
        File file = new File("tweets.txt");
        WordDict wordDict = new WordDict();
        wordDict.makeDict(file);
    }
}

class WordDict {
    ArrayList<String> dict;

    public WordDict() {
        this.dict = new ArrayList<String>();
    }

    /**
    * 1行の文字列を単語ごとに分割する
    * @param line 分割したい文
    */
    public ArrayList<String> wordList(String line) {
        ArrayList<String> words = new ArrayList<String>();
        for (int wlen = 1; wlen <= 4; wlen++) {
            for (int i = 0; i < line.length() - wlen + 1; i++) {
                String word = line.substring(i, i + wlen);
                words.add(word);
            }
        }
        return words;
    }

    public void printDict() {
        for (int i = 0; i < dict.size(); i++) {
            System.out.println(dict.get(i));
        }
    }

    /**
    * テキストファイルから辞書dictを作成
    * @param file 辞書を作成したいテキストファイル
    */
    public void makeDict(File file) {
        FileReader fr = null;
        BufferedReader br = null;
        try {
            fr = new FileReader(file);
            br = new BufferedReader(fr);

            String line;
            while ((line = br.readLine()) != null) {
                ArrayList<String> wds = this.wordList(line);
                this.dict.addAll(wds);
            }
            this.printDict();
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
}
