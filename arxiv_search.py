import re
import pyPdf

doc_fname="test_docs/1706.03762.pdf"
text1 = "arXiv:1308.0850, 2013."

#print convert(doc_fname)

def pdf_to_text(filename):
	PageFound = -1
	pdfDoc = pyPdf.PdfFileReader(file(filename, "rb"))
	content = ""
	for i in range(0, pdfDoc.getNumPages()):
		content += pdfDoc.getPage(i).extractText().encode("ascii", "ignore")
		content += "\n"
	return content

def all_arxiv_matches(text):
	pattern = r"(?i)(arxiv:[0-9]{4}\.[0-9]{4,5}v?[0-9]{0,2})"
	return re.findall(pattern, text)

def get_arxiv_citations(filename):
	content = pdf_to_text(filename)
	return all_arxiv_matches(content)