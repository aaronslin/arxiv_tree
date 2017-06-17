import re
import pyPdf
import urllib2 as UL

doc_fname="test_docs/1706.03762.pdf"
text1 = "arXiv:1308.0850, 2013."
test_id = "1706.03762"


# arXiv

class arxiv_obj:
	def __init__(self):
		self.regex = r"(?i)(arxiv:[0-9]{4}\.[0-9]{4,5}v?[0-9]{0,2})"
		self.url_prefix = "https://arxiv.org/pdf/"
		self.pdf = ".pdf"
		self.directory = "./saved_pdfs/"

	def get_url(self, id):
		return self.url_prefix + id + self.pdf

	def get_dir(self, id):
		return self.directory + id + self.pdf

arxiv = arxiv_obj()


# Search PDF for arXiv citations

def pdf_to_text(id):
	filename = arxiv.get_dir(id)
	pdfDoc = pyPdf.PdfFileReader(file(filename, "rb"))
	content = ""
	for i in range(0, pdfDoc.getNumPages()):
		content += pdfDoc.getPage(i).extractText().encode("ascii", "ignore")
		content += "\n"
	return content

def all_arxiv_matches(text):
	pattern = arxiv.regex
	return re.findall(pattern, text)

def _strip_arxiv(id):
	return re.sub('^arxiv:', '', id, flags=re.IGNORECASE)

def _rm_self(arxiv_ids, id):
	# Given id of article and a list of arxiv_ids, remove self
	pass

def get_arxiv_citations(id):
	content = pdf_to_text(id)
	matches = all_arxiv_matches(content)
	matches = _rm_self([_strip_arxiv(id) for id in matches], id)
	return matches

#print get_arxiv_citations(doc_fname)




# Web modules to interact with arxiv.org

def download_pdf(id):
	url = arxiv.get_url(id)
	writeAddress = arxiv.get_dir(id)

	file = UL.urlopen(arxiv.get_url(id))
	with open(writeAddress, "wb") as output:
		output.write(file.read())

download_pdf(test_id)

"""

TODO:

 - check to make sure that the list of arxiv things that an article cites 
 	doesn't include itself
 - [optimization] search only the last few pages of PDF file


"""