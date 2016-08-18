#! /usr/bin/env python3

"""Small module for converting latex code

   This module provides functions to convert
    - LaTeX code to DVI
    - DVI to SVG
    - SVG to PNG
   all functions write into the CWD

   This is useful for distributing small snippets of LaTeX-renderings,
   especially in the web.
   The environment variables LATEX_BIN/DVISVGM_BIN/CONVERT_BIN can be set to
   override the fallback paths to the respective tools.

   Basic idea from:
       https://github.com/DMOJ/texoid
"""


import subprocess
import os

LATEX = os.environ.get('LATEX_BIN', '/usr/bin/latex')
PDFLATEX = os.environ.get('PDFLATEX_BIN', '/usr/bin/pdflatex')
DVISVGM = os.environ.get('DVISVGM_BIN', '/usr/bin/dvisvgm')
CONVERT = os.environ.get('CONVERT_BIN', '/usr/bin/convert')


def latex_to_dvi(filename):
    """Compile .tex file to .dvi"""
    subprocess.check_call([LATEX, "-halt-on-error",
                                       "-interaction=nonstopmode",
                                       filename])
    return filename.replace('.tex', '.dvi')

def latex_to_pdf(filename):
    """Run pdflatex on .tex file"""
    subprocess.check_call([PDFLATEX, "-halt-on-error",
                                     "-interaction=nonstopmode",
                                     filename])
    return filename.replace('.tex', '.pdf')

def pdf_to_png(filename):
    """Convert .pdf file to .png"""
    outfile = filename.replace(".pdf", ".png")
    subprocess.check_call([CONVERT, "-identify",
                                    "-density", "300",
                                    "-quality", "100",
                                    "pdf:{:s}".format(filename),
                                    "png:{:s}".format(outfile)])
    return outfile

def dvi_to_svg(filename):
    """Convert .dvi file (as created from TeX) to .svg"""
    subprocess.check_call([DVISVGM, "--no-fonts", filename])
    return filename.replace('.dvi', '.svg')


def svg_to_png(filename):
    """Convert .svg file to .png"""
    outfile = filename.replace('.svg', '.png')
    subprocess.check_call([CONVERT, "-identify",
                                    "-density", "300",
                                    "-quality", "100",
                                    "svg:{:s}".format(filename),
                                    "png:{:s}".format(outfile)])
    return outfile
