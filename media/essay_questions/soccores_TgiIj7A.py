import requests
from bs4 import BeautifulSoup

with requests.session() as req:
  try:
    information = ["fixtures", "results"]
    info = int(input("""\t____WELCOME to SOCCORES____
> Which information do you need?
1) Fixtures     2) Results
=> """))
    url = "https://www.skysports.com/football"+"/"+information[info-1]
    print(f"""+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Establishing Connection with '{url}' site..""")
    r = req.get(url)
    print("""Connection Successful...!
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++""")
    print(f"""Obtaining Scores from '{url}' site...
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++""")
    soup = BeautifulSoup(r.content, 'html.parser')
    number = int(input('''
> How many match results do you need?
=> '''))
    cards = soup.find_all('div', attrs={'class': 'fixres__item'})[:number]
    for card in cards:
      team = card.find_all('span', attrs={'class': "swap-text__target"})
      score = card.find_all('span', attrs={'class': "matches__teamscores-side"})
      print(f'''{team[0].get_text(strip=True)} <==> {team[1].get_text(strip=True)}
\t{score[0].get_text(strip=True)}  <==>  {score[1].get_text(strip=True)}''')
  except IndexError:
    print('ERROR!, Give either option 1 or 2!')
  except ValueError:
    print('ERROR!, Pass in a numerical Value!')
  except:
    print('Connection Error! Check your Connection and try again!')
