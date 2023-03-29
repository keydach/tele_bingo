# tele_bingo
telegram бот для генерации карточек музыкального бинго [@musicBingo_bot](https://t.me/musicBingo_bot)

### Требования

1. A Linux host
2. Docker: 18+
3. Docker-Compose: 1.24+
4. The deployment machine have access to the Internet

### Деплой

##### Создать каталог source вида:
    --app
    --source
        --example_songs.txt
        --example_card.png
        --example_back_card.png

##### Создать файл local.env в каталоге app вида:

    API_ID=********
    API_HASH=*********************
    BOT_TOKEN=*****:**************************
    
    EXAMPLE_SONGS=example_songs.txt
    EXAMPLE_CARD=example_card.png
    EXAMPLE_BACK_CARD=example_back_card.png
    
    MAX_CARD_CNT=200
    SOURCE_DIR=/../source/


##### Собрать и запустить приложение

    docker-compose build
    docker-compose up -d