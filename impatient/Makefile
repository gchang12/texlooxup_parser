# $Id: Makefile,v 1.2 2020/01/03 22:17:40 karl Exp $
# public domain
all: book.dvi book.pdf #book.html

book.dvi: *.tex
	texfot tex '\nonstopmode\input book'
book.pdf: *.tex
	texfot pdftex '\nonstopmode\input book'
book.html:
	httex book.tex

files = ChangeLog Makefile NEWS README *.icn \
	*.tex book.aux book.idx book.toc book.ccs book.sdx book.pdf \
	diffs cn fr artwork

dist = impatient
dist: all
	rm -f x.tex
	tar -czf $(dist).tar.gz --transform='s,^,$(dist)/,' $(files)
	tar tf $(dist).tar.gz | head -4
