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


def pure_latex(bot, update):
    res = render(update.message.text[7:], update.update_id)
    bot.send_photo(chat_id=update.message.chat_id, photo=res)


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
    print(text)
    res = render(text, update.update_id)
    bot.send_photo(chat_id=update.message.chat_id, photo=res)


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
    print("==BEGIN==")
    print(text)
    print("==END==")
    res = render(text, update.update_id)
    bot.send_photo(chat_id=update.message.chat_id, photo=res)


def render(tex, job_id):
    import tempfile
    import shutil
    # TODO add program prefix etc.
    tempdir = tempfile.mkdtemp(suffix="_{:d}".format(job_id))
    os.chdir(tempdir)

    texdoc = "temp.tex"
    f = open(texdoc, "w")
    f.write(tex)
    f.close()

    return open(pdf_to_png(latex_to_pdf(texdoc)), "rb")
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
    dispatcher.add_handler(pure_latex_handler)
    math_handler = CommandHandler('math', math)
    dispatcher.add_handler(math_handler)
    latex_handler = CommandHandler('latex', latex)
    dispatcher.add_handler(latex_handler)

    updater.start_polling()


if __name__ == "__main__":
    server()

# TODO:
# possibly add inline LaTeX?
#from telegram.ext import MessageHandler, Filters
#
#from telegram import InlineQueryResultArticle, InputTextMessageContent
# def inline_caps(bot, update):
#    query = update.inline_query.query
#    if not query:
#        return
#    results = list()
#    results.append(
#        InlineQueryResultArticle(
#            id=query.upper(),
#            title='Caps',
#            input_message_content=InputTextMessageContent(query.upper())
#        )
#    )
#    bot.answerInlineQuery(update.inline_query.id, results)
#
#from telegram.ext import InlineQueryHandler
#inline_caps_handler = InlineQueryHandler(inline_caps)
# dispatcher.add_handler(inline_caps_handler)
