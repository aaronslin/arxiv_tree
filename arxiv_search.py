from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import re

doc_fname="test_docs/1706.03762.pdf"

#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 

#print convert(doc_fname)

def all_arxiv_matches(text):
    pattern = r"(?i)(arxiv:[0-9]{4}\.[0-9]{4,5}v?[0-9]{0,2})"
    return re.findall(pattern, text)

text1 = "arXiv:1308.0850, 2013."
print all_arxiv_matches(text1)