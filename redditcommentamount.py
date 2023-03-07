import mechanicalsoup
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import PySimpleGUI as sg
import re

#opens url 
def openURL(browser, user):
  url = "https://old.reddit.com/user/" + user
  page = browser.open(url)
  print(browser.url)
  return page

#finds all comments on the users first page 
def parseAccount(page):
    soup = BeautifulSoup(page.content, "html.parser")
    comments = soup.find_all('div', class_="md")
    a = ""
    for texts in comments:
      a = a + " " +texts.p.text
    a = a.replace(",","")
    a = a.replace(".","")
    splitted = re.findall("\w+", a)
    return splitted

#sort based on amount of times that word is used in all comments
def amount(arr):
  newarr = {}
  for i in range(len(arr)):
    if arr[i] in newarr:
         newarr[arr[i]] = newarr[arr[i]] +1
    else:
         newarr[arr[i]] = 1
  sortarr = {key: val for key, val in sorted(newarr.items(), key = lambda ele: ele[1], reverse=True)}
  return sortarr

#finds next page is available
def nextpage(browser):
  arr = []
  try:
    while(browser.find_link(rel = "nofollow next")):
      next = browser.follow_link(rel = "nofollow next")
      arr = arr + parseAccount(next)
  except:
      print("finished finding all words")
  return arr
   
#plots values
def plotcomments(arr, canvas):
  data = (amount(arr))
  newpd = pd.DataFrame(data.items(), columns=['Word', 'Amount'])
  print(newpd)
  newpd.plot(x = "Word", y = 'Amount', kind='bar')
  plt.show()
  # figure_canvas_agg = FigureCanvasTkAgg(plt.csd,canvas)
  # figure_canvas_agg.draw()
  # figure_canvas_agg.get_tk_widget().pack(expand=1)
  # return figure_canvas_agg
         
layout = [[sg.Canvas(key = "image")],
   [sg.Text('reddit comment visualiser')],
   [sg.Text('Enter a username')],
   [sg.Text(key="username")],
   [sg.Text(key="text")],
   [sg.InputText(), sg.Button("OK")],
   
   ]

def main():
  browser = mechanicalsoup.StatefulBrowser(
          soup_config={'features': 'lxml'},
          raise_on_404=True,
      )
  browser.set_user_agent('Mozilla/5.0')
  window = sg.Window("reddit comments",layout)
  while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
      break
    if event == "OK":
      page = openURL(browser, values[0])
      window["username"].Update(browser.url)
      arr = parseAccount(page)
      arr = arr + nextpage(browser)
      window["text"].Update("Finished finding all words")
      matplotlib.use("TkAgg")
      plotcomments(arr, window["image"].TKCanvas)

  window.close()








if __name__ == "__main__":
    main()