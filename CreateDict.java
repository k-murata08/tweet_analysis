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
    int wordMaxLength = 5;

    public WordDict() {
        this.dict = new ArrayList<String>();
    }

    /**
    * 1行の文字列を単語ごとに分割する
    * @param line 分割したい文
    */
    public ArrayList<String> wordList(String line) {
        ArrayList<String> words = new ArrayList<String>();
        for (int wlen = 1; wlen <= this.wordMaxLength; wlen++) {
            for (int i = 0; i < line.length() - wlen + 1; i++) {
                String word = line.substring(i, i + wlen);
                words.add(word);
                String s = this.convertString(word);
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

    /**
    * 単語を正規化
    * @param str 正規化したい単語
    */
    public String convertString(String str) {
        StringBuilder sb = new StringBuilder(str);
        for (int i = 0; i < sb.length(); i++) {
            char c = this.convertChar(sb.charAt(i));
            sb.setCharAt(i, c);
        }
        return sb.toString();
    }

    /**
    * 文字を正規化
    * @param c 正規化したい文字
    */
    public char convertChar(char c) {
        if (c >= 'ァ' && c <= 'ン') {
            return (char)(c - 'ァ' + 'ぁ');
        } else if (c >= 'ｧ' && c <= 'ﾝ' ) {
            return (char)(c - 'ｧ' + 'ぁ');
        } else if (c == 'ヵ') {
            return 'か';
        } else if (c == 'ヶ') {
            return 'け';
        } else if (c >= 'A' && c <= 'Z') {
            return Character.toLowerCase(c);
        } else if (c >= 'ａ' && c <= 'ｚ') {
            return (char) (c - 'ａ' + 'a');
        } else if (c >= 'Ａ' && c <= 'Ｚ') {
            return Character.toLowerCase((char) (c - 'Ａ' + 'A'));
        } else {
            return c;
        }
    }
}
