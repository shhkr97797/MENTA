import datetime
import os
import pandas as pd
import time
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager



# Chromeを起動する関数
def set_driver(driver_path, headless_flg):


    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument('--incognito')          # シークレットモードの設定を付与

    

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)


# main処理
def main():
    # ４　難易度★★☆☆☆
    # 任意のキーワードをコンソール（黒い画面）から指定して検索できるようにしてみましょう
    search_keyword = input("検索ワードを入力（例：大阪 エンジニア 在宅勤務）→")
    # driverを起動
    custom_path = "./"
    if os.name == 'nt': #Windows
        driver = set_driver(ChromeDriverManager(path=custom_path).install(), False)
    elif os.name == 'posix': #Mac
        driver = set_driver(ChromeDriverManager(path=custom_path).install(), False)
    # Webサイトを開く
    # driver.Chrome(ChromeDriverManager().install())
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)

    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    # ページ終了まで繰り返し取得
    exp_name_list = []
    link_tit_list = []
    emp_label_list = []
    first_income_list = []
    income_price_list = []

    # ページ監視変数
    current_page = 0

    # # ３　難易度★★★☆☆
    # ２ページ目以降の情報も含めて取得できるようにしてみましょう
    while True:
        current_page += 1
        
        # 検索結果の一番上の会社名を取得
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

        # #１　難易度★★☆☆☆
        # 会社名以外の項目を取得して画面にprint文で表示してみましょう。
        # 青文字タイトルを取得
        link_tit = driver.find_elements_by_xpath("//p[@class='cassetteRecruit__copy']/a")

        # ## ２　難易度★★★☆☆
        # for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう
        # 青文字タイトル横、緑ラベルを取得
        emp_label = driver.find_elements_by_class_name("labelEmploymentStatus")

        # テーブル内初年度年収を取得
        first_income = driver.find_elements_by_xpath("//table/tbody/tr[5]/th")
        income_price = driver.find_elements_by_xpath("//table/tbody/tr[5]/td")

        # 1ページ分繰り返し
        print(len(name_list))
        for name, tit, label, f_income, income in zip(
                                                        name_list,
                                                        link_tit,
                                                        emp_label,
                                                        first_income,
                                                        income_price
                                                    ):
            exp_name_list.append(name.text)
            link_tit_list.append(tit.text)
            emp_label_list.append(label.text)
            first_income_list.append(f_income.text)
            income_price_list.append(income.text)

            # ７　難易度★★☆☆☆
            # 処理の経過が分かりやすいようにログファイルを出力してみましょう<br>
            # ログファイルとは：ツールがいつどのように動作したかを後から確認するために重要なテキストファイルです。
            # ライブラリを用いることもできますが、テキストファイルを出力する処理で簡単に実現できるので、試してみましょう。
            # (今何件目、エラー内容、等を表示)
            dt = datetime.datetime.now()
            now_time = dt.strftime("%Y年%m月%d日 %H:%M:%S")
            with open("log.txt", "a", encoding="utf-8") as f:
                print(now_time, name.text, sep="　", file=f)

            # ５　難易度★★★★☆
            # 取得した結果をpandasモジュールを使ってCSVファイルに出力してみましょう
            df = pd.DataFrame({
                                "会社名": exp_name_list,
                                "概要": link_tit_list,
                                "雇用形態": emp_label_list,
                                "初年度年収": income_price_list,
                            })
            df.to_csv("mynavi.csv", sep="　", encoding="utf-8")

        if current_page == 2:
            break
    
        # ６　難易度★★☆☆☆
        # エラーが発生した場合に、処理を停止させるのではなく、スキップして処理を継続できるようにしてみましょう(try文)
        try:
            next_btn = driver.find_element_by_class_name("iconFont--arrowLeft").click()
        except:
            pass





# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
