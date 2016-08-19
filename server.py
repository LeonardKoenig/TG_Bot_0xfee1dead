#! /usr/bin/env python3

"""Telegram-Bot server module for a LaTeX bot

   Supported commands:
    - /pure_latex: allows compilation of any latex code
    - /latex: no need for boiler plate, just type
    - /math: same, but already in $-$ mathmode

    Environment + conversion inspired by:
        https://tonicdev.com/npm/mathmode
"""


from tex_convert import *

description = """\
This bot will be doing embarrassing things to you. Among these are:
 - compile LaTeX code and send you the result as png
 - nothing else for now. I know. Embarrassing.

source code (AGPLv3 licensed): https://github.com/LeonardKoenig/TG_Bot_0xfee1dead
"""

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=description)

def unknownc(bot, update):
    reply = """\
I see you are trying your best to talk to me, but I really do not understand\
this command.
If I may suggest anything, a look into /help might help.
"""
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def unknown(bot, update):
    confused = """\
I'm deeply sorry but it seems you got a little confused there.
It's not that I'm a real human, you know. I do not understand
your gibberish. No offense meant.

Just in case, I'll send you a description of me.
"""
    bot.send_message(chat_id=update.message.chat_id, text=confused)
    bot.send_message(chat_id=update.message.chat_id, text=description)

def pure_latex(bot, update):
    res, tempdir = render(update.message.text[7:], update.update_id)
    bot.send_photo(chat_id=update.message.chat_id, photo=res)
    cleanup(tempdir)


def math(bot, update):
    text = r"""\documentclass{minimal}
    \usepackage[active,tightpage]{preview}
    \usepackage{amsmath}
    \usepackage[utf8]{inputenc}
    \usepackage{transparent}
    \begin{document}
    \begin{preview}
    $""" + update.message.text[6:] + r"""$
    \end{preview}
    \end{document}"""
    res, tempdir = render(text, update.update_id)
    bot.send_photo(chat_id=update.message.chat_id, photo=res)
    cleanup(tempdir)


def latex(bot, update):
    text = r"""\documentclass{minimal}
    \usepackage[active,tightpage]{preview}
    \usepackage{amsmath}
    \usepackage[utf8]{inputenc}
    \usepackage{transparent}
    \begin{document}
    \begin{preview}
    """ + update.message.text[6:] + r"""
    \end{preview}
    \end{document}"""
    res, tempdir = render(text, update.update_id)
    bot.send_photo(chat_id=update.message.chat_id, photo=res)
    cleanup(tempdir)


def render(tex, job_id):
    import tempfile
    prefix = "tg_bot_latex" + tempfile.gettempprefix()
    tempdir = tempfile.mkdtemp(suffix="_{:d}".format(job_id), prefix=prefix)
    print("tempdir:", tempdir)
    os.chdir(tempdir)

    texdoc = "temp.tex"
    f = open(texdoc, "w")
    f.write(tex)
    f.close()

    return (open(pdf_to_png(latex_to_pdf(texdoc)), "rb"), tempdir)


def cleanup(tempdir):
    import shutil
    os.chdir("..")
    shutil.rmtree(tempdir)


def server():
    import logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    import json
    from telegram.ext import Updater
    updater = Updater(token=json.load(open("./.private/token.json", "r")))
    dispatcher = updater.dispatcher

    from telegram.ext import CommandHandler
    pure_latex_handler = CommandHandler('pure_latex', pure_latex)
    math_handler = CommandHandler('math', math)
    latex_handler = CommandHandler('latex', latex)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', start)
    from telegram.ext import MessageHandler, Filters
    unknownc_handler = MessageHandler([Filters.command], unknownc)
    unknown_handler = MessageHandler([lambda x: True], unknown)

    handlers = [pure_latex_handler, math_handler, latex_handler, start_handler,
                help_handler, unknownc_handler, unknown_handler]

    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_polling()


if __name__ == "__main__":
    server()
