from bs4 import BeautifulSoup
import requests

req = input()

url = f'https://yandex.ru/search/?text={req}&clid=2270455&banerid=6302000000%3A654ca234416b79f523a301f7&win=619&lr=50'

page = requests.get(url)
print(page.text)

soup = BeautifulSoup(page.text, 'html.parser')

answer = soup.find('div', class_ = 'FactFold-Container')

print(answer)