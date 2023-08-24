import requests
from bs4 import BeautifulSoup
import streamlit as st
import time

#エラー137,172,177,428,458
#例外:1680,1826,2142,2318,3096,3240(完成)
#メモ:前回:3720,
base_url = "https://ryu.sega-online.jp/news/"
# start_index = st.number_input('https://ryu.sega-online.jp/news/<ここの数値>',3000,6000,3700,step=1)
# end_index = st.number_input('https://ryu.sega-online.jp/news/<ここの数値>',3000,6000,3700,step=1)
page_list = []

s = '装備名称'
st.write("https://ryu.sega-online.jp/news/<ここの数値>/を入力")
st.write("1680,1826,2142,2318,3096はエラーが出ることを確認、範囲に含まないように")
st.write("連続で押したり、広い範囲で検索しないように、サーバに負荷がかかります")
start = st.text_input("開始番号 例:3700", key = "例:3700")
end = st.text_input("終了番号 例:3800", key = "例:3701")

button = st.button("検索", key=0)
if button == True:
  start_index = int(start)
  end_index = int(end)
  for i in range(start_index, end_index + 1):
    time.sleep(0.2)
    url = base_url + str(i) + "/"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    tables = soup.select("table")

    sobi_tables = []
    N=0
    for table in tables:
      if s in table.text:
        sobi_tables.append(table)
        table_url = url
        N+=1
        if N==1:
          page_list.append(i)
          st.write("---------------------------------------------")
          st.write(table_url)

    for sobi_table in sobi_tables:
      columns = len(sobi_table.find_all("tr")[0].find_all("th"))
      if columns == 2:
        rows_name = sobi_table.find_all("th")
        rows_img = sobi_table.find_all("img")

        for k in range(2,len(sobi_table.find_all("th"))):
          st.write(rows_name[k].text.replace('NEW!','').replace('　','').replace(' ','').replace('※派遣報酬として店舗Lv.4から獲得可能になります。','').replace('※派遣報酬として店舗Lv.3から獲得可能になります。','').replace('※派遣報酬として店舗Lv.2から獲得可能になります。','').replace('\n\n','\n').replace('\t\t\t\t',''))
          st.write('https://ryu.sega-online.jp'+str(rows_img[k-2]).replace('<img alt="" src="','').replace('"/>',''))
          rows_status = sobi_table.find_all("td")[k-2].find_all("li")

          for n in range(len(rows_status)-2):
            st.write(rows_status[n].text)
          st.write(rows_status[len(rows_status)-1].text)
      else:
        rows = sobi_table.find_all("tr")
        #st.write(rows)
        for k in range(1,len(rows)):
          st.write(rows[k].find_all("th")[0].text.replace('NEW!','').replace('　','').replace(' ','').replace('※派遣報酬として店舗Lv.5から獲得可能になります。','').replace('※派遣報酬として店舗Lv.4から獲得可能になります。','').replace('※派遣報酬として店舗Lv.3から獲得可能になります。','').replace('※派遣報酬として店舗Lv.2から獲得可能になります。','').replace('\n\n','\n'))
          st.write('https://ryu.sega-online.jp'+str(rows[k].find_all("img")[0]).replace('<img alt="" src="','').replace('"/>',''))
          rows_status = rows[k].find_all("td")[0].find_all("li")
          for n in range(len(rows_status)-2):
            st.write(rows_status[n].text)
          st.write(rows_status[len(rows_status)-1].text)


