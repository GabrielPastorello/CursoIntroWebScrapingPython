import bs4
import requests
import smtplib
import time

cyber = 'https://store.steampowered.com/app/1091500/Cyberpunk_2077/' # Jogo sem desconto
wolf = 'https://store.steampowered.com/app/1056960/Wolfenstein_Youngblood/' # Jogo com desconto (2)
insur = 'https://store.steampowered.com/app/581320/Insurgency_Sandstorm/' # Jogo com desconto (1)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'} # Estamos informando ao site que somos um navegador 
cookies = {'birthtime': '568022401', 'mature_content': '1'} # Estamos informando ao site que temos mais que 18 anos e podemos pular as telas de verificação de idade da Steam

# Função que irá pegar o preço
def getPrice(url): 
    res = requests.get(url, headers=headers, cookies=cookies) # Baixa a página da internet (objeto "Response")
    res.raise_for_status() # Irá criar uma exceção caso não tenha sido possível a obtenção da página
    soup = bs4.BeautifulSoup(res.text, 'html.parser') # Converte o que obtivemos no requests.get()
    price = soup.select_one('#game_area_purchase > div.game_area_purchase_game_wrapper > div > div.game_purchase_action > div > div.game_purchase_price.price')
    if price == None:
        price = soup.select_one('#game_area_purchase > div:nth-child(1) > div > div.game_purchase_action > div > div.discount_block.game_purchase_discount > div.discount_prices > div.discount_final_price')
        if price == None:
            price = soup.select_one('#game_area_purchase > div:nth-child(2) > div > div.game_purchase_action > div > div.discount_block.game_purchase_discount > div.discount_prices > div.discount_final_price')
    price = price.text.strip()
    price = price.replace(',', '.').replace(' ', '') # Troca a , por . e tira os espaços
    price = float(price[2:]) # Transforma a string price em um número float
    return price

# Função que irá mandar o email
def sendEmail(price, url):
    title = gameTitle(url)
    conn = smtplib.SMTP('smtp.gmail.com', 587) # Se for gmail
    conn.ehlo() 
    conn.starttls() 
    conn.login('EMAIL@gmail.com', 'SENHA') # Email e senha
    from_ = 'EMAIL@gmail.com'
    to_ = 'EMAIL@gmail.com'
    subject = title + '!' # Assunto do email
    body = '{} está a R${} no momento.\nConfira no link: {}\n\n-Steam Store Price Bot'.format(title, price, url) # Texto do email
    msg = 'Subject: {}\n\n{}'.format(subject, body)
    conn.sendmail(to_, from_, msg.encode('utf-8'))
    print('Email has been sent!')
    conn.quit()

# Função que irá pegar o título
def gameTitle(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    title = soup.title.text.strip()
    return title

# Função que irá checar se o preço é menor
def checkPrice(games):
    for game in games:
        if game['email'] != True:
            price = getPrice(game['url'])
            if price < game['price']:
                sendEmail(price, game['url'])
                game['email'] = True

# Dicionário onde estão os jogos
games = [{'url': cyber, 'price': 150, 'email': False},
         {'url': wolf, 'price': 80, 'email': False},
         {'url': insur, 'price': 10, 'email': False}]

while(True):

    checkPrice(games)
    time.sleep(3600) # O programa irá rodar a cada 1h (3600s)

