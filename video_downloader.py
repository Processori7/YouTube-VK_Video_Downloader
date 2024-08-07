import sys
import os
import re
import yt_dlp
import webbrowser
import requests
import traceback
from yt_dlp import YoutubeDL
from packaging import version
from tkinter import messagebox


CURRENT_VERSION = "1.2"

def update_app(update_url):
   webbrowser.open(update_url)


def check_for_updates():
    try:
        # Получение информации о последнем релизе на GitHub
        response = requests.get("https://api.github.com/repos/Processori7/YouTube-VK_Video_Downloader/releases/latest")
        response.raise_for_status()
        latest_release = response.json()

        # Получение ссылки на файл exe последней версии
        assets = latest_release["assets"]
        for asset in assets:
            if asset["name"].endswith(".exe"):
                download_url = asset["browser_download_url"]
                break
        else:
            messagebox.showerror("Ошибка обновления", "Не удалось найти файл exe для последней версии.")
            return

        # Сравнение текущей версии с последней версией
        latest_version_str = latest_release["tag_name"]
        match = re.search(r'\d+\.\d+', latest_version_str)
        if match:
            latest_version = match.group()
        else:
            latest_version = latest_version_str

        if version.parse(latest_version) > version.parse(CURRENT_VERSION):
            # Предложение пользователю обновление
            if messagebox.showwarning("Доступно обновление",
                                      f"Доступна новая версия {latest_version}. Хотите обновить?", icon='warning',
                                      type='yesno') == 'yes':
                update_app(download_url)
    except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка при проверке обновлений", e)

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
                video_platforms = [
                    'watch?v=',
                    'https://youtu.be/',
                    'shorts/',
                    'https://vk.com/video',
                    'https://rutube.ru/video/',
                    'https://my.mail.ru//community/gotivim.mm/video/',
                    'http://ok.ru/video/'
                ]
                if any(platform in url for platform in video_platforms):
                    download(url)

                if 'https://www.youtube.com/channel/' in url or 'https://rutube.ru/channel/' in url:
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
            check_for_updates()
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
