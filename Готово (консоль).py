import traceback
from pytube import Channel, Playlist
from pytube3 import YouTube
from youtube_dl import YoutubeDL
import youtube_dl
import sys
import os
import urllib.request
# pip install -r requirements.txt

while True:
    try:

        def ans(url):
            try:
                # Определяем способ обработки ссылки исходя из значений, содержащихся в ней.
                if 'videos' in url:
                    x = 0
                    c = Channel(url)
                    for video in c.videos:
                        x = x + 1
                        video = str(video)
                        # Преобразованный в строку объект видео преобразуем, убирая первые 41 символ и последний.
                        video = video[41::]
                        video = video[:-1]
                        # Формируем ссылку на видео
                        video_url = 'https://www.youtube.com/watch?v=' + video
                        print(f'{x}) {video_url}')
                        count_che_in_video = len(video_url)
                        if count_che_in_video > 43:
                            break
                        else:
                            # Отправляем ссылку в функцию, для получения нужной информации по каждому видео
                            get_info(video_url)
                            #Скачмваем видео
                            download(video_url)

                    print(f'Всего на канале {x} видео.')

                # Определяем способ обработки ссылки исходя из значений, содержащихся в ней.

                elif '&list=' in url:
                    x = 0
                    p = Playlist(url)
                    for video in p.videos:
                        x = x + 1
                        video = str(video)
                        video = video[41::]
                        video = video[:-1]
                        video_url = 'https://www.youtube.com/watch?v=' + video
                        print(f'{x}) {video_url}')
                        count_che_in_video = len(video_url)
                        if count_che_in_video > 43:
                            break
                        else:
                            get_info(video_url)
                            download(video_url)

                elif 'watch?v=' in url:
                    video_url = url
                    get_info(video_url)
                    download(video_url)

                elif 'https://www.youtube.com/channel/' in url:
                    video_url = url
                    get_info(video_url)

                elif 'https://youtu.be/' in url:

                    video_url = url
                    get_info(video_url)
                    download(video_url)

                elif 'https://youtube.com/playlist?list=' in url:
                    x = 0
                    p = Playlist(url)
                    for video in p.videos:
                        x +=1
                        video = str(video)
                        video = video[41::]
                        video = video[:-1]
                        video_url = 'https://www.youtube.com/watch?v=' + video
                        print(f'{x}) {video_url}')
                        count_che_in_video = len(video_url)
                        if count_che_in_video > 43:
                            break
                        else:
                            get_info(video_url)
                            download(video_url)

                elif 'https://vk.com/video-' in url:
                    ydl_opts = {}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

                elif 'выход' in url:
                    sys.exit()

                elif 'beta' or 'бета' in url:
                    print('Внимание! Активирована функция бета тестирования!\nПрограмма может работать некорректно!')
                    video_name = input("Введите название файла: ")
                    ras = 'Введите расширение файлы без точки: '
                    print('Начинается загрузка')
                    urllib.request.urlretrieve(url, video_name+'.'+ras)
                    print('Загрузка завершина!')

                else:
                   print('К сожалению, ссылка не поддерживается.')

                # Если происходит ошибка, запишем ее в errors.log
            except Exception:
                print('Ошибка\n')
                with open('errors.log', 'a') as f:
                    f.write('{}\n'.format(traceback.format_exc()))


        def get_info(video_url):

            try:
                # Инициализируем объект YoutubeDL

                with YoutubeDL({'quiet': True}) as ydl:
                    # Получаем всю возможную информацию
                    info_dict = ydl.extract_info(video_url, download=False)
                    # video_url = info_dict.get("url", None)
                    # video_id = info_dict.get("id", None)
                    # Получаем название
                    video_title = info_dict.get('title', None)
                    # Получаем описание
                    description = info_dict.get('description', None)
                    # Формируем конечный результат
                    info = f'Название: {video_title} \n Описание: {description} \n Ссылка: {video_url}\n\n'
                    # Передаем данные для записи
                    write(info)
                    return video_url

            except Exception:
                print('Ошибка\n')
                with open('errors_info.log', 'a') as f:
                    f.write('{}\n'.format(traceback.format_exc()))

        def download(video_url):
            try:
                print("Начинаю загрузку видео...\n")
                # Инициализируем объект YouTube и передаем в него ссылку
                try:
                    # yt = YouTube(video_url)
                    # # Разбиваем объект на потоки, ставим параметры загрузки видео как mp4, стараемся получить лучшее качество.
                    # streams = yt.streams
                    #
                    # video_1080 = streams.filter(res='1080p').desc().first()
                    # video_1080.download('Загруженные_видео_и_информация_о_них')
                    YouTube(video_url).streams.get_highest_resolution().download('Загруженные_видео_и_информация_о_них')
                    # yt.streams.filter(progressive=True, file_extension='mp4').first().download('Загруженные_видео')
                    print(f'Видео успешно загруженно по ссылке: {video_url}\n')
                except:
                    YouTube(video_url).streams.get_highest_resolution().download('Загруженные_видео_и_информация_о_них')

            except Exception:
                # Логируем все ошибки в программе
                print('Ошибка\n')
                with open('errors_download.log', 'a') as f:
                    f.write('{}\n'.format(traceback.format_exc()))


        def write(info):
            File_chek = os.path.exists('Загруженные_видео_и_информация_о_них')
            if File_chek == True:
                # Название файла
                ofname = r'Загруженные_видео_и_информация_о_них/Информация.txt'
                # Открываем файл для дозаписи и записываем в него полученные данне из переменной info
                with open(ofname, "a", encoding="utf-8") as files:
                    print(info, file=files)
                print(info + '\n')
            else:
                os.mkdir('Загруженные_видео_и_информация_о_них')
                # Название файла
                ofname = r'Загруженные_видео_и_информация_о_них/Информация.txt'
                # Открываем файл для дозаписи и записываем в него полученные данне из переменной info
                with open(ofname, "a", encoding="utf-8") as files:
                    print(info, file=files)
                print(info + '\n')


        if __name__ == '__main__':
            # Получаем ссылку и подтвержение на загрузку видео.
            url = input('Вставьте ссылку или напишите выход: ')
            print('\n')
            # Отправляем данные в функцию для их обработки
            ans(url)


    except Exception:
        # Логируем все ошибки в программе
        print('Ошибка\n')
        with open('errors_info.log', 'a') as f:
            f.write('{}\n'.format(traceback.format_exc()))
