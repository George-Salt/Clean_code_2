import os
import pygame
import requests
import time
from alive_progress import alive_bar
from dotenv import load_dotenv
load_dotenv()


BUFFER = 1024
FRAMERATE = 60
MORSE_SOUND = {
    '.': 'dot.ogg',
    '-': 'dash.ogg',
    '|': 'long_silence.ogg'
}

pygame.init()

os.system('cls||clear')
pygame.mixer.init(BUFFER)
morse_code = {
    'а': '.-',
    'б': '-...',
    'в': '.--',
    'г': '--.',
    'д': '-..',
    'е': '.',
    'ж': '...-',
    'з': '--..',
    'и': '..',
    'й': '.---',
    'к': '-.-',
    'л': '.-..',
    'м': '--',
    'н': '-.',
    'о': '---',
    'п': '.--.',
    'р': '.-.',
    'с': '...',
    'т': '-',
    'у': '..-',
    'ф': '..-.',
    'х': '....',
    'ц': '-.-.',
    'ч': '---.',
    'ш': '----',
    'щ': '--.-',
    'ъ': '.--.-.',
    'ы': '-.--',
    'ь': '-..-',
    'э': '..-..',
    'ю': '..--',
    'я': '.-.-',
    '1': '.----',
    '0': '-----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    ',': '--..--',
    '.': '.-.-.-',
    '?': '..--..',
    ';': '-.-.-.',
    ':': '---...',
    "'": '.----.',
    '-': '-....-',
    '/': '-..-.',
    '(': '-.--.-',
    ')': '-.--.-',
    ' ': '|',
    '_': '..--.-'
}

message = os.getenv('komanda', default='По-умолчанию').lower()

for letter in message:
    message = message.replace(letter, morse_code[letter])

address = 'http://195.161.68.58'


def contact_robot(address):
    answer = requests.get(address)
    soobshchenie = 'Проверка связи с роботом...'
    print(soobshchenie)
    with alive_bar(
        len(soobshchenie),
        bar='brackets',
        spinner='radioactive'
    ) as bar:
        for _ in range(len(soobshchenie)):
            time.sleep(0.06)
            bar()
    os.system('cls||clear')
    if answer.status_code == 200:
        print('Связь с роботом установлена!')
    else:
        print('Нет связи с роботом')


def play_sound(soundfile):
    sound = pygame.mixer.Sound(soundfile)
    clock = pygame.time.Clock()
    sound.play()
    while pygame.mixer.get_busy():
        clock.tick(FRAMERATE)


def play_morse_message(morz):
    for symbol in morz:
        with alive_bar(
            len(morz),
            bar='brackets',
            spinner='dots_waves2'
        ) as bar:
            play_sound(MORSE_SOUND[symbol])
            bar()


def otpravka_soobshcheniya_robotu(adres, message):
    print('Отправка сообщения роботу...')
    otvet = requests.post(adres, message.encode('utf-8'))
    if otvet.status_code == 200:
        print('Команда принята.'), time.sleep(1), print('Бегу к вам!')
    elif otvet.status_code == 501:
        print('Команда принята. Продолжаю выполнять прежнюю инструкцию.')
    else:
        print('Команда не принята. Не понял вас!')


contact_robot(address)
otpravka_soobshcheniya_robotu(address, message)
play_morse_message(message)
