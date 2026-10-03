import typer

from src.config import get_settings
from src.providers.youtube_provider import YoutubeProvider


def main(
        url: str = typer.Option(None, '--url', help="URL of the resource"),
):
    if url is None:
        raise typer.BadParameter("You must specify a URL")

    provider = YoutubeProvider(api_key=get_settings().youtube_api_key)

    format_info_container = provider.get_formats(url=url)

    format_info_container.print_formats()
    chosen_formats = typer.prompt("Choose formats: ")

    chosen_formats_from_container = format_info_container.get_format_ids(chosen_formats)
    if not chosen_formats_from_container:
        pass

    options = {
        "format": chosen_formats_from_container,
        "merge_output_format": "mp4",
    }

    provider.download_by_url(url=url, user_options=options)


if __name__ == "__main__":
    typer.run(main)