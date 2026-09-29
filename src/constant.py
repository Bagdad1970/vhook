YOUTUBE_URL_PREFIX = "https://www.youtube.com/watch?v="

YOUTUBE_YT_DLP_OPTIONS = {
    "outtmpl": "%(title)s",
    "cookiesfrombrowser": ("firefox",),
    "js_runtimes": {
        "deno": {"path": "/home/bagdad/.deno/bin/deno"},
    },
    "remote_components": [ "ejs:github" ],
}