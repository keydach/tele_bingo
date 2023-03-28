import pdfkit
import pathlib
import random
import re
import logging
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

from settings import config


input_dir = '{}/{}'.format(pathlib.Path(__file__).parent.resolve(), config.source_dir)
template_dir = '{}/template'.format(pathlib.Path(__file__).parent.resolve())
environment = Environment(loader=FileSystemLoader(template_dir))

base_template = environment.get_template("base_template.html")
card_template = environment.get_template("card_template.html")
back_card_template = environment.get_template("back_card_template.html")


def parse_data(data):
    raw_songs = data.split('\n')
    songs = []
    win_songs = []
    w_fl = False

    for cur_song in raw_songs:
        cur_song = re.sub(r'(^.*[0-9]\.)', '', cur_song)
        cur_song = cur_song.strip(' ')
        if cur_song == 'Win':
            w_fl = True
        elif cur_song:
            if w_fl:
                win_songs.append(cur_song)
            else:
                songs.append(cur_song)

    return songs, win_songs


def make_bingo(bingo_options, win_options):
    if not win_options:
        x = random.sample(range(1, len(bingo_options)), 25)
        random.shuffle(x)
        params = {'cell{}'.format(str(i)): bingo_options[x[i]].strip() for i in range(0, 25)}
    else:
        x = random.sample(range(1, len(bingo_options)), 24)
        x_par = [bingo_options[i] for i in x]
        y = random.sample(range(1, len(win_options)), 1)
        y_par = [win_options[i] for i in y]
        itog_par = x_par + y_par
        random.shuffle(itog_par)
        params = {'cell{}'.format(str(i)): itog_par[i].strip() for i in range(0, 25)}

    return card_template.render(**params)


def print_cards(songs, win_songs, user_pref, card_cnt):
    output_dir = input_dir
    cards_body = []

    for _i in range(1, card_cnt + 1):
        card_body = make_bingo(songs, win_songs)
        back_cards_body = back_card_template.render()
        cards_body.append('{}{}'.format(card_body, back_cards_body))

    logging.info('Карточки с 1 по {} сгенерированы'.format(card_cnt))

    options = {
        'page-size': 'A5',
        'margin-top': '0cm', 'margin-right': '0cm', 'margin-bottom': '0cm', 'margin-left': '0cm',
        'encoding': "UTF-8",
        'no-outline': None,
        "enable-local-file-access": "",
        'dpi': 300,
    }

    body = base_template.render(**{
        'cards_data': cards_body,
        'img_path': '{}/bingo2.png'.format(template_dir),
        'back_img_path': '{}/bingo3.png'.format(template_dir)
    })

    logging.info('Собираем файл, подождите...')
    pdf_file_name = '{}{}.pdf'.format(user_pref, datetime.now().strftime("_bingo_%Y-%m-%d_%H:%M:%S"))
    pdfkit.from_string(body, '{}/{}'.format(output_dir, pdf_file_name), options=options)

    return pdf_file_name
