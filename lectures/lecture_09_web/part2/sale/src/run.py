# TODO: код где-нибудь здесь. Если есть желание, можно и на ином языке.
# Требуется создать ручку с произвольным именем, которое вы в последствии передадите на мой сервис для проверки.
# В обработчике ручки необходимо кинуть запрос на auth сервис и получить информацию о себе
# с помощью ручки about_me (авторизация по кукам).
# Вернуть json в котором указать username, age и sale, которая рассчитывается по формуле round(age / 7).
# Кука при запросе на сервис auth должна быть вида
# {'session': '<длинный id>', 'technoatom': '<длинный id2>'}, её можно получить из запроса к сервису.
from flask import Flask, request, jsonify
import requests
import json

HOST = '0.0.0.0'
app = Flask(__name__)


@app.route('/sale')
def sale():
    cookies = request.cookies
    resp = requests.get('http://auth:5000/about_me', cookies=cookies)
    pars_resp = json.loads(resp.text)
    age = int(pars_resp['age'])
    user = pars_resp['username']
    s = round(age/7)
    return jsonify({'username': user, 'age': age, 'sale': s})


if __name__ == '__main__':
    app.run(host=HOST)

