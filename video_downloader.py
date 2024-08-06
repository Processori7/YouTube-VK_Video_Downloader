import traceback
import sys
import os
import yt_dlp
from yt_dlp import YoutubeDL


while True:
    try:
        def ans(url):
            try:
                # Создаем объект YoutubeDL для получения информации о канале
                ydl = yt_dlp.YoutubeDL()
                # Получаем информацию о канале
                channel_info = ydl.extract_info(url, download=False)
                # Проверяем, что это действительно канал
                if 'entries' in channel_info:
                    x = 0
                    total_videos = len(channel_info['entries'])  # Общее количество видео
                    for entry in channel_info['entries']:
                        x += 1
                        video_url = entry['url']
                        print(f'{x}) {video_url}')
                        # Отправляем ссылку в функцию, для получения нужной информации по каждому видео
                        download(video_url)
                    print(f'Всего на канале {total_videos} видео.')

                # Определяем способ обработки ссылки исходя из значений, содержащихся в ней.
                if '&list=' in url or 'https://youtube.com/playlist?list=' in url or 'https://www.youtube.com/playlist?list=' in url:
                    x = 0
                    ydl_opts = {
                        'format': 'best',
                        'quiet': True,
                        'extract_flat': True,  # Извлечение информации о видео без загрузки
                    }

                    with YoutubeDL(ydl_opts) as ydl:
                        playlist_info = ydl.extract_info(url, download=False)
                        for video in playlist_info['entries']:
                            x += 1
                            video_url = video['url']
                            print(f'{x}) {video_url}')
                            count_che_in_video = len(video_url)
                            if count_che_in_video > 43:
                                break
                            else:
                                ydl.download([video_url])  # Загрузка видео

                if 'watch?v=' in url or 'https://youtu.be/' in url or 'shorts/' in url:
                    download(url)

                if 'https://www.youtube.com/channel/' in url:
                    download(url)

                if 'выход' in url:
                    sys.exit()

                # Если происходит ошибка, запишем ее в errors.log
            except Exception as e:
                print(f'Ошибка: {e}\n')
                with open('errors.log', 'a') as f:
                    f.write('{}\n'.format(traceback.format_exc()))

        def download(video_url):
            try:
                print("Начинаю загрузку видео...\n")
                ydl_opts = {
                    'format': 'best',  # Скачивание в наилучшем качестве
                    'outtmpl': 'Загруженные_видео_и_информация_о_них/%(title)s.%(ext)s',  # Путь и имя файла
                    'noplaylist': True,  # Скачивать плейлист, если это плейлист
                    'quiet': True,  # Выводить информацию о процессе
                    'writethumbnail': True  # Скачивание миниатюры
                }

                # Скачивание видео и получение информации
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)  # Скачивание видео
                    title = info_dict.get('title', 'Неизвестное название')
                    description = info_dict.get('description', 'Нет описания')

                    # Формируем конечный результат
                    info = f'Название: {title} \nОписание:\n {description} \nСсылка: {video_url}\n\n'
                    write(info)  # Запись информации в файл

                    print(f'Видео успешно загружено: {title}\n')

            except Exception as e:
                print(f'Ошибка: {e}\n')
                with open('errors.log', 'a') as f:
                    f.write('{}\n'.format(traceback.format_exc()))

        def write(info):
            File_chek = os.path.exists('Загруженные_видео_и_информация_о_них')
            if File_chek:
                # Название файла
                ofname = r'Загруженные_видео_и_информация_о_них/Информация.txt'
                with open(ofname, "a", encoding="utf-8") as files:
                    print(info, file=files)
                print(info + '\n')
            else:
                os.mkdir('Загруженные_видео_и_информация_о_них')
                # Название файла
                ofname = r'Загруженные_видео_и_информация_о_них/Информация.txt'
                with open(ofname, "a", encoding="utf-8") as files:
                    print(info, file=files)
                print(info + '\n')

        if __name__ == '__main__':
            # Получаем ссылку и подтвержение на загрузку видео.
            url = input('Вставьте ссылку или напишите выход: ')
            print('\n')
            # Отправляем данные в функцию для их обработки
            ans(url)

    except Exception as e:
        # Логируем все ошибки в программе
        print(f'Ошибка: {e}\n')
        with open('errors_info.log', 'a') as f:
            f.write('{}\n'.format(traceback.format_exc()))
