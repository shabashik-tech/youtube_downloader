import os
import re

from pytube import YouTube


class YouTubeDownloader:

    def __init__(self, link):
        self.url = link
        self.video_trigger = None

    def run(self):
        video = self.video_init(self.url)
        self.user_choice(video)

    def user_choice(self, video):
        while True:
            print('Что скачать?')
            user_choice = input('1. Видео 2. Аудио: ')
            if user_choice == '1':
                self.video_trigger = 1
            elif user_choice == '2':
                self.video_trigger = None
            else:
                print('Введите корректные данные!')
                continue
            self.downloader(video)
            break

    def audio_downloader(self, youtube_url):
        file = youtube_url.streams.filter(only_audio=True).first()
        file.download(output_path='files/audio')
        os.rename(f'files/audio/{file.title}.mp4', f'files/audio/{file.title}.mp3')

    def video_downloader(self, youtube_url):
        file = youtube_url.streams.filter(progressive=True).desc().first()
        file.download(output_path='files/videos')

    def downloader(self, youtube_url):
        if self.video_trigger:
            self.video_downloader(youtube_url)
        else:
            self.audio_downloader(youtube_url)
        print('Файл скачан успешно!')

    def video_init(self, url):
        youtube = YouTube(url=url)
        print(youtube.title)
        return youtube


class GetLink:
    re_url = re.compile(r'(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|playlist\?|'
                        r'watch\?v=|watch\?.+(?:&|&#38;);v=))([a-zA-Z0-9\-_]{11})?(?:(?:\?|&|&#38;)'
                        r'index=((?:\d){1,3}))?(?:(?:\?|&|&#38;)?list=([a-zA-Z\-_0-9]{34}))?(?:\S+)?')

    def get_url(self):
        while True:
            url_from_user = input('Вставьте ссылку: ')
            match = re.match(self.re_url, url_from_user)
            if match:
                self.url = url_from_user
                return self.url
            else:
                print('Вставьте корректную ссылку!')
                continue


if __name__ == '__main__':
    # 'https://www.youtube.com/watch?v=HglA72ogPCE'
    link = GetLink().get_url()
    downloader = YouTubeDownloader(link)
    downloader.run()
