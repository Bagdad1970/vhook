import pytest

from src.format_info_container import FormatInfoContainer
from src.models.format_info import FormatInfo


@pytest.fixture(scope="function")
def format_container():
    format_info1 = { 'format_id': '1', 'ext': 'mp3', 'resolution': 'audio only', 'vcodec': 'none', 'acodec': 'mp3', 'filesize': 1456 }
    format_info2 = { 'format_id': '2', 'ext': 'mp3', 'resolution': 'audio only', 'vcodec': 'none', 'acodec': 'opus', 'filesize': 12589 }
    format_info3 = { 'format_id': 'fi1', 'ext': 'mp4', 'resolution': '1920x720', 'vcodec': 'h264', 'acodec': 'none', 'filesize': 24867 }
    format_info4 = { 'format_id': '4', 'ext': 'mp4', 'resolution': '720x720', 'vcodec': 'h264', 'acodec': 'none', 'filesize': 169875 }
    format_info5 = { 'format_id': 'srd-12', 'ext': 'webm', 'resolution': '1920x1080', 'vcodec': 'av1', 'acodec': 'none', 'filesize': 679416 }

    format_infos = [ format_info1, format_info2, format_info3, format_info4, format_info5 ]
    
    formats = [FormatInfo.create_from_dict(format_info) for format_info in format_infos]

    return FormatInfoContainer(formats)


class TestFormatInfoContainer:

    @pytest.mark.parametrize("chosen_formats, expected", [
        ('', False),
        ('1,2', False),
        ('1.2', False),
        (' - ', False),
        ('1++2', False),
        (' + ', False)
    ])
    def test_chosen_formats_with_wrong_input_is_invalid(self, format_container, chosen_formats, expected):
        is_valid = format_container._is_chosen_formats_valid(chosen_formats)

        assert is_valid == expected


    @pytest.mark.parametrize("chosen_formats, expected", [
        ('1', True),
        ('  1  ', True),
        ('1+5', True),
        (' 1 + 2 ', True),
    ])
    def test_chosen_formats_with_formats_in_bounds_is_valid(self, format_container, chosen_formats, expected):
        is_valid = format_container._is_chosen_formats_valid(chosen_formats)

        assert is_valid == expected

    def test_chosen_formats_with_similar_formats_in_bounds_is_valid(self, format_container):
        chosen_formats = '1+1'

        is_valid = format_container._is_chosen_formats_valid(chosen_formats)

        assert is_valid is True


    @pytest.mark.parametrize("chosen_formats, expected", [
        ('0', False),
        ('6', False),
        ('1+100', False),
        ('100+1', False),
        ('100+100', False),
        ('100+101', False)
    ])
    def test_chosen_formats_with_at_least_one_format_out_of_bounds_is_invalid(self, format_container, chosen_formats, expected):
        is_valid = format_container._is_chosen_formats_valid(chosen_formats)

        assert is_valid == expected


    @pytest.mark.parametrize("formats, expected", [
        ('', ''),
        ('   ', ''),
    ])
    def test_get_format_ids_with_empty_formats_returns_empty(self, format_container, formats, expected):
        format_ids = format_container.get_format_ids(formats)

        assert format_ids == expected


    @pytest.mark.parametrize("formats", [
        'invalid',
        '0',
        '6',
        '1+100',
        '100+1',
        '100+100',
        '100+101'
    ])
    def test_get_format_ids_with_invalid_formats_throws_exception(self, format_container, formats):
        with pytest.raises(ValueError):
            format_container.get_format_ids(formats)


    @pytest.mark.parametrize("formats, expected", [
        ('1', '1'),
        ('  1  ', '1'),
        ('3', 'fi1'),
        ('2+5', '2+srd-12'),
        ('5+5+2', 'srd-12+2'),
        ('2+2', '2'),
    ])
    def test_get_format_ids_with_formats_returns_unique_ids(self, format_container, formats, expected):
        format_ids = format_container.get_format_ids(formats)

        assert format_ids == expected


