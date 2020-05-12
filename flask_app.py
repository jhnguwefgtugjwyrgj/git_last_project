from flask import Flask, request
import logging
import json
import pymorphy2

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response, 'слон')
    handle_dialog(request.json, response, 'кролик')
    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res, word):
    word_ = pymorphy2.MorphAnalyzer().parse(word)[0].inflect({'gent'})
    user_id = req['session']['user_id']
    print(req['session'])
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = f'Привет! Купи {word_}!'
        res['response']['buttons'] = get_suggests(user_id, word)
        return
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
        'Я покупаю',
        'Я куплю'
    ]:
        res['response']['text'] = f'{word_} можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return
    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи {word_}!"
    res['response']['buttons'] = get_suggests(user_id, word)


def get_suggests(user_id, word):
    session = sessionStorage[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": f"https://market.yandex.ru/search?text={word}",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
