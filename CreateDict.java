import java.io.*;
import java.util.*;

public class CreateDict {
    public static void main(String[] args) {
        File readfile = new File("tweets.txt");
        File writefile = new File("dictionary.csv");
        WordDict wordDict = new WordDict();
        wordDict.makeDict(readfile, writefile);
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
                String word = line.substring(i, i + wlen).trim();
                if (word.length() != 0) {
                    words.add(word);
                }
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
    public void makeDict(File readfile, File writefile) {
        FileReader fr = null;
        FileWriter fw = null;
        BufferedReader br = null;
        PrintWriter pw = null;
        try {
            fr = new FileReader(readfile);
            fw = new FileWriter(writefile, false);
            br = new BufferedReader(fr);
            pw = new PrintWriter(new BufferedWriter(fw));

            // 辞書リスト作成
            String line;
            while ((line = br.readLine()) != null) {
                ArrayList<String> wds = this.wordList(line);
                for (int i = 0; i < wds.size(); i++) {
                    String convertStr = this.convertString(wds.get(i));
                    wds.set(i, convertStr);
                }
                this.dict.addAll(wds);
            }
            this.printDict();

            // ファイル書き込み
            pw.print("word"); // ヘッダs
            pw.println();
            for (int i = 0; i < this.dict.size(); i++) {
                String word = this.dict.get(i);
                pw.print(word);
                pw.println();
            }

        } catch(FileNotFoundException e) {
            System.out.println(e);
        } catch(IOException e) {
            System.out.println(e);
        } finally {
            try {
                br.close();
                fr.close();
                fw.close();
                pw.close();
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
    * カタカナは全角ひらがなに
    * アルファベットは全角小文字に
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
        } else if (c == '！') {
            return '!';
        } else if (c == '？') {
            return '?';
        } else {
            return c;
        }
    }
}
