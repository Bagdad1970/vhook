import datetime

from src.models import VideoQuery


class VideoFilter:

    def __init__(self, query: VideoQuery):
        self.query = query
        self.valid_video_infos = []
        self.left_ptr = -1
        self.right_ptr = -1


    def filter_video_infos_by_date(self, video_infos: list) -> list:
        # сначала проверим, что если самое первое видео имеет published_date >= to_date т.е. видео выпущено позже, чем правая граница фильтра, можно сразу завершать цикл


        # поскольку video_infos отсортирован, можно использовать бинарный поиск.
        # сначала ищем первый, который подходит пщ from_date. необходимо найти самое левое такое видео
        # затем ищем последнего, который подходит по to_date. необходимо найти самое правое такое видео

        # во первых такую проверку стоит вынести для первой проверки. если она не проходит, то все - весь набор данных неверный (наверное)
        # надо просто проверить первый элемент первого батча
        if video_infos[0]['published_at'] >= self.query.to_date or video_infos[-1]['published_at'] <= self.query.from_date:
            return []

        if self.left_ptr == -1:
            found_left_index = self.binary_search(video_infos, self.query.from_date)

            for i in range(found_left_index, 1, -1):
                if video_infos[i - 1]["published_date"] < self.query.from_date and video_infos[i]["published_date"] == self.query.from_date:
                    self.left_ptr = i

        elif self.right_ptr == -1:
            found_right_index = self.binary_search(video_infos, self.query.to_date)

            for i in range(0, found_right_index - 1):
                if video_infos[i]["published_date"] > self.query.to_date and video_infos[i + 1]["published_date"] == self.query.to_date:
                    self.right_ptr = i




    def filter_video_infos(self, video_infos: list):
        for video_info in video_infos:
            pass


    @classmethod
    def binary_search(cls, video_info_dates: list, target: datetime.date):
        if not video_info_dates:
            return -1

        left, right = 0, len(video_info_dates) - 1
        while left <= right:
            middle_index = left + (right - left) // 2

            if video_info_dates[middle_index] == target:
                return middle_index
            elif video_info_dates[middle_index] > target:
                right = middle_index - 1
            elif video_info_dates[middle_index] < target:
                left = middle_index + 1

        return -1