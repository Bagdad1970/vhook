import typer

import src.utilities as utilities
from src.providers.youtube_provider import YoutubeProvider
from src.config import get_settings

app = typer.Typer()

@app.command()
def main(
        url: str = typer.Option(None, '--url', help="URL of the resource"),
):
    if url is None:
        raise typer.BadParameter("You must specify a URL")

    provider = YoutubeProvider(api_key=get_settings().youtube_api_key)

    format_container = utilities.get_formats(url=url)

    format_container.print_formats()
    chosen_formats = typer.prompt("Choose formats: ")

    if not format_container.is_chosen_formats_valid(chosen_formats):
        pass

    options = {
        "format": format_container.get_format_ids(chosen_formats),
        "merge_output_format": "mp4",
    }

    provider.download_by_url(url=url, user_options=options)


if __name__ == "__main__":
    typer.run(main)