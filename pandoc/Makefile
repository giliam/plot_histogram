# Makefile
# 
# Converts Markdown to other formats (HTML, PDF, DOCX, RTF, ODT, EPUB) using Pandoc
# <http://johnmacfarlane.net/pandoc/>
# source : https://gist.github.com/kristopherjohnson/7466917
#
# Run "make" (or "make all") to convert to all other formats
#
# Run "make clean" to delete converted files

# Convert all files in this directory that have a .md suffix
SOURCE_DOCS := $(wildcard *.md)
CURRENT_DIR := ${CURDIR}

EXPORTED_DOCS=\
 $(SOURCE_DOCS:.md=.html) \
 $(SOURCE_DOCS:.md=.pdf)

EXPORTED_DOCS_HTML=\
 $(SOURCE_DOCS:.md=.html)

PANDOC="C:\Users\matthieu.denoux\Anaconda3\Scripts\pandoc.exe"

PDFLATEX="C:\Users\matthieu.denoux\AppData\Local\Programs\MiKTeX 2.9\miktex\bin\x64\pdflatex"

FILTER=filter.bat

PANDOC_OPTIONS=-s --number-sections --toc --filter=pandoc-citeproc --csl=apapersonnalized.csl --from markdown+pipe_tables+footnotes

PANDOC_HTML_OPTIONS=--mathjax -c style.css
PANDOC_PDF_OPTIONS=--filter=pandoc-latex-admonition --filter=pandoc-latex-tip --pdf-engine=$(PDFLATEX)
PANDOC_DOCX_OPTIONS=
PANDOC_RTF_OPTIONS=
PANDOC_ODT_OPTIONS=
PANDOC_EPUB_OPTIONS=--to epub3


# Pattern-matching Rules

%.html : %.md
	$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_HTML_OPTIONS) -o $@ $<

%.pdf : %.md
	$(PANDOC) $(PANDOC_OPTIONS) -o $@ $< $(PANDOC_PDF_OPTIONS)

%.docx : %.md
	$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_DOCX_OPTIONS) -o $@ $<

%.rtf : %.md
	$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_RTF_OPTIONS) -o $@ $<

%.odt : %.md
	$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_ODT_OPTIONS) -o $@ $<

%.epub : %.md
	$(PANDOC) $(PANDOC_OPTIONS) $(PANDOC_EPUB_OPTIONS) -o $@ $<


# Targets and dependencies

.PHONY: all clean

all : $(EXPORTED_DOCS)

html : $(EXPORTED_DOCS_HTML)

clean: 
	- rm $(EXPORTED_DOCS)
