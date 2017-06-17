import re
import pyPdf
import urllib2 as UL
import timeit

doc_fname="test_docs/1706.03762.pdf"
text1 = """     <id>http://arxiv.org/abs/0707.3536v1</id>
    <updated>2007-07-24T12:45:39Z</updated>
    <published>2007-07-24T12:45:39Z</published>
    <title>Degenerating families of dendrograms</title>
    <summary>  Dendrograms used in data analysis are ultrametric spaces, hence objects of
nonarchimedean geometry. It is known that there exist $p$-adic representation
of dendrograms. Completed by a point at infinity, they can be viewed as
subtrees of the Bruhat-Tits tree associated to the $p$-adic projective line.
The implications are that certain moduli spaces known in algebraic geometry are
$p$-adic parameter spaces of (families of) dendrograms, and stochastic
classification can also be handled within this framework. At the end, we
calculate the topology of the hidden part of a dendrogram.
</summary>
    <author>
      <name>Patrick Erik Bradley</name>
    </author>
    <arxiv:doi xmlns:arxiv="http://arxiv.org/schemas/atom">10.1007/s00357-008-9009-5</arxiv:doi>
    <link title="doi" href="http://dx.doi.org/10.1007/s00357-008-9009-5" rel="related"/>
    <arxiv:comment xmlns:arxiv="http://arxiv.org/schemas/atom">13 pages, 8 figures</arxiv:comment>
    <arxiv:journal_ref xmlns:arxiv="http://arxiv.org/schemas/atom">J. Classif. 25, 27-42 (2008)</arxiv:journal_ref>
    <link href="http://arxiv.org/abs/0707.3536v1" rel="alternate" type="text/html"/>
    <link title="pdf" href="http://arxiv.org/pdf/0707.3536v1" rel="related" type="application/pdf"/>
    <arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="stat.ML" scheme="http://arxiv.org/schemas/atom"/>
    <category term="stat.ML" scheme="http://arxiv.org/schemas/atom"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/0707.4072v1</id>
    <updated>2007-07-27T09:37:28Z</updated>
    <published>2007-07-27T09:37:28Z</published>
    <title>Families of dendrograms</title>"""
test_id = "1706.03762"


# arXiv

class arxiv_obj:
	def __init__(self):
		self.citation_regex = r"(?i)(arxiv:[0-9]{4}\.[0-9]{4,5}v?[0-9]{0,2})"
		self.rss_regex = r"<id>http:\/\/arxiv\.org\/abs\/(.*?)<\/id>"

		self.url_prefix = "https://arxiv.org/pdf/"
		self.pdf = ".pdf"
		self.directory = "./saved_pdfs/"
		self.category = "cat:cs.LG"
		self.rss_prefix = "http://export.arxiv.org/api/query?search_query="

	def get_url(self, id):
		return self.url_prefix + id + self.pdf

	def get_dir(self, id):
		return self.directory + id + self.pdf

	def get_rss(self, start, increment):
		maxKey = "max_results="
		startKey = "start="
		sortBy = "sortBy=submittedDate"
		queryItems = [self.category, maxKey+str(increment), startKey+str(start), sortBy]
		queryJoin = "&".join(queryItems)
		return self.rss_prefix + queryJoin


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
	pattern = arxiv.citation_regex
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

def fetch_pdfs(increment, safety_cap = 1500):
	start = 0
	while start < safety_cap:
		rss_url = arxiv.get_rss(start, increment)
		ids = search_rss(rss_url)
		if len(ids) == 0:
			# No more papers
			break
		else:
			[download_pdf(id) for id in ids]
			start += increment

def search_rss(rss_url):
	data = UL.urlopen(rss_url).read()
	pattern = arxiv.rss_regex
	return re.findall(pattern, data)


#download_pdf(test_id)

fetch_pdfs(100)
print search_rss(text1)

"""

TODO:

 - check to make sure that the list of arxiv things that an article cites 
 	doesn't include itself
 - [optimization] search only the last few pages of PDF file


"""