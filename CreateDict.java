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
        if (Character.isAlphabetic(c)) {
            return Character.toUpperCase(c);
        } else {
            switch(c) {
                case "ア": return "あ";
                case "イ": return "い";
                case "ウ": return "う";
                case "エ": return "え";
                case "オ": return "お";
                case "カ": return "か";
                case "キ": return "き";
                case "ク": return "く";
                case "ケ": return "け";
                case "コ": return "こ";
                case "サ": return "さ";
                case "シ": return "し";
                case "ス": return "す";
                case "セ": return "せ";
                case "ソ": return "そ";
                case "タ": return "た";
                case "チ": return "ち";
                case "ツ": return "つ";
                case "テ": return "て";
                case "ト": return "と";
                case "ナ": return "な";
                case "ニ": return "に";
                case "ヌ": return "ぬ";
                case "ネ": return "ね";
                case "ノ": return "の";
                case "ハ": return "は";
                case "ヒ": return "ひ";
                case "フ": return "ふ";
                case "ヘ": return "へ";
                case "ホ": return "ほ";
                case "ヤ": return "や";
                case "ユ": return "ゆ";
                case "ヨ": return "よ";
                case "マ": return "ま";
                case "ミ": return "み";
                case "ム": return "む";
                case "メ": return "め";
                case "モ": return "も";
                case "ラ": return "ら";
                case "リ": return "り";
                case "ル": return "る";
                case "レ": return "れ";
                case "ロ": return "ろ";
                case "ワ": return "わ";
                case "ヲ": return "を";
                case "ン": return "ん";
                case "ガ": return "が";
                case "ギ": return "ぎ";
                case "グ": return "ぐ";
                case "ゲ": return "げ";
                case "ゴ": return "ご";
                case "ザ": return "ざ";
                case "ジ": return "じ";
                case "ズ": return "ず";
                case "ゼ": return "ぜ";
                case "ゾ": return "ぞ";
                case "ダ": return "だ";
                case "ヂ": return "ぢ";
                case "ヅ": return "づ";
                case "デ": return "で";
                case "ド": return "ど";
                case "バ": return "ば";
                case "ビ": return "び";
                case "ブ": return "ぶ";
                case "ベ": return "べ";
                case "ボ": return "ぼ";
                case "パ": return "ぱ";
                case "ピ": return "ぴ";
                case "プ": return "ぷ";
                case "ペ": return "ぺ";
                case "ポ": return "ぽ";
                case "ァ": return "ぁ";
                case "ィ": return "ぃ";
                case "ゥ": return "ぅ";
                case "ェ": return "ぇ";
                case "ォ": return "ぉ";
                case "ヮ": return "ゎ";
                case "ャ": return "ゃ";
                case "ュ": return "ゅ";
                case "ョ": return "ょ";
                case "ッ": return "っ";
                case "ｱ": return "あ";
                case "ｲ": return "い";
                case "ｳ": return "う";
                case "ｴ": return "え";
                case "ｵ": return "お";
                case "ｶ": return "か";
                case "ｷ": return "き";
                case "ｸ": return "く";
                case "ｹ": return "け";
                case "ｺ": return "こ";
                case "ｻ": return "さ";
                case "ｼ": return "し";
                case "ｽ": return "す";
                case "ｾ": return "せ";
                case "ｿ": return "そ";
                case "ﾀ": return "た";
                case "ﾁ": return "ち";
                case "ﾂ": return "つ";
                case "ﾃ": return "て";
                case "ﾄ": return "と";
                case "ﾅ": return "な";
                case "ﾆ": return "に";
                case "ﾇ": return "ぬ";
                case "ﾈ": return "ね";
                case "ﾉ": return "の";
                case "ﾊ": return "は";
                case "ﾋ": return "ひ";
                case "ﾌ": return "ふ";
                case "ﾍ": return "へ";
                case "ﾎ": return "ほ";
                case "ﾔ": return "や";
                case "ﾕ": return "ゆ";
                case "ﾖ": return "よ";
                case "ﾏ": return "ま";
                case "ﾐ": return "み";
                case "ﾑ": return "む";
                case "ﾒ": return "め";
                case "ﾓ": return "も";
                case "ﾗ": return "ら";
                case "ﾘ": return "り";
                case "ﾙ": return "る";
                case "ﾚ": return "れ";
                case "ﾛ": return "ろ";
                case "ﾜ": return "わ";
                case "ｦ": return "を";
                case "ﾝ": return "ん";
                case "ｶﾞ": return "が";
                case "ｷﾞ": return "ぎ";
                case "ｸﾞ": return "ぐ";
                case "ｹﾞ": return "げ";
                case "ｺﾞ": return "ご";
                case "ｻﾞ": return "ざ";
                case "ｼﾞ": return "じ";
                case "ｽﾞ": return "ず";
                case "ｾﾞ": return "ぜ";
                case "ｿﾞ": return "ぞ";
                case "ﾀﾞ": return "だ";
                case "ﾁﾞ": return "ぢ";
                case "ﾂﾞ": return "づ";
                case "ﾃﾞ": return "で";
                case "ﾄﾞ": return "ど";
                case "ﾊﾞ": return "ば";
                case "ﾋﾞ": return "び";
                case "ﾌﾞ": return "ぶ";
                case "ﾍﾞ": return "べ";
                case "ﾎﾞ": return "ぼ";
                case "ﾊﾟ": return "ぱ";
                case "ﾋﾟ": return "ぴ";
                case "ﾌﾟ": return "ぷ";
                case "ﾍﾟ": return "ぺ";
                case "ﾎﾟ": return "ぽ";
                case "ｧ": return "ぁ";
                case "ｨ": return "ぃ";
                case "ｩ": return "ぅ";
                case "ｪ": return "ぇ";
                case "ｫ": return "ぉ";
                case "ｬ": return "ゃ";
                case "ｭ": return "ゅ";
                case "ｮ": return "ょ";
                case "ｯ": return "っ";
                default: return c;
            }
        }
    }
}
