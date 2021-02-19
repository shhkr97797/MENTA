### 検索ツールサンプル
### これをベースに課題の内容を追記してください
import csv
# 検索ソース
source = ["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

### 検索ツール
def search():
    while True:
        word = input("鬼滅の登場人物の名前を入力してください >>> ")
        
        ### ここに検索ロジックを書く
        if word in source:
            print("「{}」が見つかりました".format(word))
        else:
            print("「{}」はありません".format(word))
            # csvに追加
            source.append(word)
            with open("./csv/task01.csv", "r", encoding="utf_8") as r:
                print(r.read())
                with open("./csv/task01.csv", "w", encoding="utf_8") as w:
                    for sources in source:
                        w.write(sources)
                    print("「{}」をcsvファイルに追加しました".format(word))


if __name__ == "__main__":
    search()



