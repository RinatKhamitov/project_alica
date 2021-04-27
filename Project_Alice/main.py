import json
import random

from flask import Flask, request

app = Flask(__name__)

player_class = {
    'rogue': {
        'name': 'лучник',
        'img': '1521359/e79aef5247e60beb528e'
    },
    'warrior': {
        'name': 'воин',
        'img': '1652229/186e94218779aad3b839'
    },
    'mage': {
        'name': 'маг',
        'img': '1521359/40fc60d08c56f66f3a0f'
    }
}

enemy_list = [{'name': 'страшный огр', 'img': '1521359/37a734dbb1618996a16e'},
              {'name': 'пират', 'img': '1540737/8491e835c86c9ec4115b'}]

left = True

attempt = 1


def offer_class(user_id, req, res):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            if name := entity['value'].get('first_name'):
                name = name.capitalize()
                session_state[user_id]['first_name'] = name
                res['response']['text'] = f"приятно познакомиться {name}, выбери свой класс"
                res['response']['card'] = {
                    'type': 'ItemsList',
                    'header': {
                        'text': f"приятно познакомиться {name}, выбери свой класс"
                    },
                    'items': [
                        {
                            'image_id': player_class['mage']['img'],
                            'title': player_class['mage']['name'],
                            'description': 'Магия - опасное оружие',

                        },
                        {
                            'image_id': player_class['warrior']['img'],
                            'title': player_class['warrior']['name'],
                            'description': 'Меч - грозное оружие',

                        },
                        {
                            'image_id': player_class['rogue']['img'],
                            'title': player_class['rogue']['name'],
                            'description': 'Лук - коварное оружие',

                        }
                    ],
                    'footer': {
                        'text': 'не ошибись с выбором'
                    }
                }
                session_state[user_id] = {
                    'state': 2
                }
                return


def offer_adventure(user_id, req, res):
    while True:
        try:
            if req['request']['command'] == "маг" or req['request']['command'] == "mage":
                select_class = 'mage'
                break
            elif req['request']['command'] == "лучник" or req['request']['command'] == "rogue":
                select_class = 'rogue'
                break
            if req['request']['command'] == "воин" or req['request']['command'] == "warrior":
                select_class = 'warrior'
                break
        except Exception:
            res['response']['text'] = 'Пожалуйста, повторитите попытку'
    print(select_class)
    session_state[user_id].update({
        'class': select_class,
        'state': 3
    })
    res['response'] = {
        'text': f"{select_class.capitalize()} - прекрасный выбор",
        'card': {
            'type': 'BigImage',
            'image_id': player_class[select_class]['img'],
            'title': f'{select_class.capitalize()} -  прекрасный выбор'
        },
        'buttons': [{
            'title': 'Пойти в лес',
            'payload': {'fight': True},
            'hide': True
        },
            {
                'title': 'Завершить игру',
                'payload': {'fight': False},
                'hide': True

            }
        ]

    }


def offer_fight(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = 'Пожалуйста, выбери действие'
        return
    if not answer:
        res['response']['text'] = 'Ваше приключение закончилось'
        res['response']['end_session'] = True
    else:
        enemy = random.choice(enemy_list)
        req['request']['payload']['enemy'] = enemy
        session_state[user_id]['state'] = 4
        res['response'] = {
            'text': f'Ваш противник {enemy["name"]}',
            'card': {
                'type': 'BigImage',
                'image_id': enemy['img'],
                'title': f'Ваш противник {enemy["name"]}'
            },
            'buttons': [{
                'title': 'атаковать',
                'payload': {'fight': True},
                'hide': True
            },
                {
                    'title': 'Убежать',
                    'payload': {'fight': False},
                    'hide': True

                }
            ]

        }


def end_fight(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        enemy = random.choice(enemy_list)
        res['response'] = {
            'text': f'Ваш противник {enemy["name"]}',
            'card': {
                'type': 'BigImage',
                'image_id': enemy['img'],
                'title': f'Ваш противник {enemy["name"]}'
            },
            'buttons': [{
                'title': 'атаковать',
                'payload': {'fight': True},
                'hide': True
            },
                {
                    'title': 'Убежать',
                    'payload': {'fight': False},
                    'hide': True

                }
            ]

        }
        return
    if not answer:
        res['response']['text'] = 'Ваше приключение закончилось'
        res['response']['end_session'] = True
    else:
        res['response']['text'] = 'Вы победили противника'
        find_map(user_id, req, res)

    session_state[user_id]['state'] = 5


def find_map(user_id, req, res):
    res['response'] = {
        'text': f'Ваш противник, что-то прятал',
        'card': {
            'type': 'BigImage',
            'image_id': '965417/807c1e3eba32b303384a',
            'title': f'Ваш противник, что-то прятал'
        },
        'buttons': [{
            'title': 'обыскать',
            'payload': {'map': True},
            'hide': True
        }
        ]
    }

    session_state[user_id]['state'] = 6
    open_map(user_id, req, res)


def open_map(user_id, req, res):
    answer = False
    try:
        answer = req['request']['payload']['map']
    except KeyError:
        res['response'] = {
            'text': f'Ваш противник, что-то прятал',
            'card': {
                'type': 'BigImage',
                'image_id': '965417/807c1e3eba32b303384a',
                'title': f'Ваш противник, что-то прятал'
            },
            'buttons': [{
                'title': 'обыскать',
                'payload': {'map': True},
                'hide': True
            }
            ]
        }
    if answer:
        res['response'] = {
            'text': f'Вы нашли записку',
            'card': {
                'type': 'BigImage',
                'image_id': '1540737/f77991fa305e0c66ac7a',
                'title': f'Вы нашли записку'
            },
            'buttons': [{
                'title': 'открыть',
                'payload': {'map_open': True},
                'hide': True
            },
                {
                    'title': 'выбросить',
                    'payload': {'map_open': False},
                    'hide': True
                }]
        }
        session_state[user_id]['state'] = 7


def go_adventure(user_id, req, res):
    try:
        answer = req['request']['payload']['map_open']
    except KeyError:
        res['response'] = {
            'text': f'Вы нашли записку',
            'card': {
                'type': 'BigImage',
                'image_id': '1540737/f77991fa305e0c66ac7a',
                'title': f'Вы нашли записку'
            },
            'buttons': [{
                'title': 'открыть',
                'payload': {'map_open': True},
                'hide': True
            },
                {
                    'title': 'выбросить',
                    'payload': {'map_open': False},
                    'hide': True
                }]
        }
        return
    if not answer:
        res['response']['text'] = 'Жаль, Вы пропустили очень интересное приключение'
        res['response']['end_session'] = True
    else:
        res['response'] = {
            'text': 'В записке было написано: "Налево, направо,'
                    ' направо, налево", что бы это могло значить?',
            'card': {
                'type': 'BigImage',
                'image_id': '1030494/9b0e3d28ccc0ce9f8130',
                'title': 'В записке было написано: "Налево, направо,'
                         ' направо, налево", что бы это могло значить?'
            },
            'buttons': [{
                'title': 'Продолжить приключение',
                'payload': {'go_adventure': True},
                'hide': True
            },
                {
                    'title': 'Закончить приключение',
                    'payload': {'go_adventure': False},
                    'hide': True
                }]
        }
        session_state[user_id]['state'] = 8


def adventure1(user_id, req, res):
    global left, attempt
    try:
        answer = req['request']['payload']['go_adventure']
    except KeyError:
        res['response'] = {
            'text': 'В записке было написано: "Налево, направо,'
                    ' направо, налево", что бы это могло значить?',
            'card': {
                'type': 'BigImage',
                'image_id': '1030494/9b0e3d28ccc0ce9f8130',
                'title': 'В записке было написано: "Налево, направо,'
                         ' направо, налево", что бы это могло значить?'
            },
            'buttons': [{
                'title': 'Продолжить приключение',
                'payload': {'go_adventure': True},
                'hide': True
            },
                {
                    'title': 'Закончить приключение',
                    'payload': {'go_adventure': False},
                    'hide': True
                }]
        }
        return

    if not answer:
        res['response']['text'] = 'Ваше приключение закончилось'
        res['response']['end_session'] = True
    else:
        res['response'] = {
            'text': 'ты встретил табличку. Куда ты выберешь пойти?',
            'card': {
                'type': 'BigImage',
                'image_id': '213044/e6bd78f5c5de76b89ff4',
                'title': 'ты встретил табличку. Куда ты выберешь пойти?'
            },
            'buttons': [{
                'title': 'Налево',
                'payload': {'left': True},
                'hide': True
            },
                {
                    'title': 'Направо',
                    'payload': {'left': False},
                    'hide': True
                }]
        }
        session_state[user_id]['state'] = 9


def adventure2(user_id, req, res):
    try:
        answer = req['request']['payload']['left']
    except KeyError:
        res['response']['text'] = 'Пожалуйста выбери действие'
        return

    if not answer:
        res['response'] = {
            'text': 'Похоже ты ошибся путем, ты встретил армию нежити. Увы но тебе не сбежать :(',
            'card': {
                'type': 'BigImage',
                'image_id': '965417/595f22d62ed29d0acbb4',
                'title': 'Похоже ты ошибся путем, ты встретил армию нежити. Увы но тебе не сбежать :('
            }
        }
        res['response']['end_session'] = True
    else:
        res['response'] = {
            'text': 'Похоже ты выбрал правильнвый путь. Куда ты пойдешь на этот раз?',
            'card': {
                'type': 'BigImage',
                'image_id': '213044/e6bd78f5c5de76b89ff4',
                'title': 'Похоже ты выбрал правильнвый путь. Куда ты пойдешь на этот раз?'
            },
            'buttons': [{
                'title': 'Налево',
                'payload': {'right': False},
                'hide': True
            },
                {
                    'title': 'Направо',
                    'payload': {'right': True},
                    'hide': True
                }]
        }
        session_state[user_id]['state'] = 10


def adventure3(user_id, req, res):
    try:
        answer = req['request']['payload']['right']
    except KeyError:
        res['response']['text'] = 'Пожалуйста выбери действие'
        return

    if not answer:
        res['response'] = {
            'text': 'Похоже ты ошибся путем, ты встретил армию нежити. Увы но тебе не сбежать :(',
            'card': {
                'type': 'BigImage',
                'image_id': '965417/595f22d62ed29d0acbb4',
                'title': 'Похоже ты ошибся путем, ты встретил армию нежити. Увы но тебе не сбежать :('
            }
        }
        res['response']['end_session'] = True
    else:
        res['response'] = {
            'text': 'Вау, ты опять выбрал правильный путь, я уверен ты скоро будешь у цели!',
            'card': {
                'type': 'BigImage',
                'image_id': '213044/e6bd78f5c5de76b89ff4',
                'title': 'Вау, ты опять выбрал правильный путь, я уверен ты скоро будешь у цели!'
            },
            'buttons': [{
                'title': 'Налево',
                'payload': {'right': False},
                'hide': True
            },
                {
                    'title': 'Направо',
                    'payload': {'right': True},
                    'hide': True
                }]
        }
        session_state[user_id]['state'] = 11


def adventure4(user_id, req, res):
    try:
        answer = req['request']['payload']['right']
    except KeyError:
        res['response']['text'] = 'Пожалуйста выбери действие'
        return

    if not answer:
        res['response'] = {
            'text': 'Похоже ты ошибся путем, ты встретил армию нежити. Увы но тебе не сбежать :(',
            'card': {
                'type': 'BigImage',
                'image_id': '965417/595f22d62ed29d0acbb4',
                'title': 'Похоже ты ошибся путем, ты встретил армию нежити. Увы но тебе не сбежать :('
            }
        }
        res['response']['end_session'] = True
    else:
        res['response'] = {
            'text': 'Ты зашел так далеко, я верю ты сможешь пройти.'
                    'Это последний поворот!',
            'card': {
                'type': 'BigImage',
                'image_id': '213044/e6bd78f5c5de76b89ff4',
                'title': 'Ты зашел так далеко, я верю ты сможешь пройти.'
                         'Это последний поворот!'
            },
            'buttons': [{
                'title': 'Налево',
                'payload': {'left': True},
                'hide': True
            },
                {
                    'title': 'Направо',
                    'payload': {'left': False},
                    'hide': True
                }]
        }
        session_state[user_id]['state'] = 12


def end_game(user_id, req, res):
    try:
        answer = req['request']['payload']['left']
    except KeyError:
        res['response']['text'] = 'Пожалуйста выбери действие'
        return
    if not answer:
        res['response'] = {
            'text': 'Похоже ты ошибся путем, ты встретил армию нежити. Увы но тебе не сбежать :(',
            'card': {
                'type': 'BigImage',
                'image_id': '965417/595f22d62ed29d0acbb4',
                'title': 'Похоже ты ошибся путем, ты встретил армию нежити. Увы но тебе не сбежать :('
            }
        }
        res['response']['end_session'] = True
    else:
        res['response'] = {
            'text': 'Ты нашел сокровищницу! Вся сокровищница наполнена золотом. Теперь ты сказочно богатый!',
            'card': {
                'type': 'BigImage',
                'image_id': '1521359/60b68e44038bdfe0e54f',
                'title': 'Ты нашел сокровищницу! Вся сокровищница наполнена золотом. Теперь ты сказочно богатый!'
            }
        }


@app.route('/post', methods=['POST'])
def get_alice_request():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет, мы тут играем в игру. Назови свое имя!'
        session_state[user_id] = {
            'state': 1
        }
        return
    states[session_state[user_id]['state']](user_id, req, res)


states = {
    1: offer_class,
    2: offer_adventure,
    3: offer_fight,
    4: end_fight,
    5: find_map,
    6: open_map,
    7: go_adventure,
    8: adventure1,
    9: adventure2,
    10: adventure3,
    11: adventure4,
    12: end_game
}

session_state = {}
if __name__ == '__main__':
    app.run()
