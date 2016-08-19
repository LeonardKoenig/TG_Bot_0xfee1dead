# Telegram Bot [0xfee1dead](https://web.telegram.org/#/im?p=@fee1dead_bot)

This bot is mostly just a testbed/collection for ideas.
Currently implemented is compiling LaTeX code and converting the result into
a PNG.

## Set-up:

### Requirements:

You need to have some tools installed:
 - LaTeX (usually TeXLive)
 - ImageMagick
 - Python 3
 - [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)

The code is only tested on Linux but should at least work on any similarly
UNIX-ish or UNIX OS (macOS, BSD, ...) as long as the needed programs are there.

### Configuration:

Your Telegram bot-token, say XYZ, goes into `./.private/token.json` as "XYZ" (ie.: quoted).

### Running:

Just run
```
$ ./server.py
```
in the source directory, your server should be up and running for his life.
