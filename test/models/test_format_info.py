import pytest

from src.models.format_info import Format, FormatResolutionType


class TestFormat:

    def test_format_negative_bytes_throws_exception(self):
        with pytest.raises(ValueError):
            Format.format_bytes(-1)


    def test_format_zero_bytes_is_zero_bytes(self):
        assert Format.format_bytes(0) == "0 B"


    @pytest.mark.parametrize("bytes_size, expected", [
        (1, "1 B"),
        (1023, "1023 B"),
        (1024, "1.00 KB"),
        (1025, "1.00 KB"),
        (123456789, "117.74 MB"),
        (1024 ** 8, "1.00 YB"),
        (1024 ** 9, "1024.00 YB"),
    ])
    def test_format_positive_bytes_return_positive_bytes(self, bytes_size, expected):
        assert Format.format_bytes(bytes_size) == expected


    @pytest.mark.parametrize("resolution, extension, expected", [
        (None, None, None),
        (None, 'none', None),
        ('none', None, None),
        ('none', 'none', None),
        ('none', 'audio', FormatResolutionType.AUDIO),
        ('video', None, FormatResolutionType.VIDEO),
        ('video', 'audio', None),
    ])
    def test_get_resolution_type(self, resolution, extension, expected):
        assert Format.get_resolution_type(resolution, extension) == expected