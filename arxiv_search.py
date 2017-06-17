import re
import pyPdf
import urllib2 as UL
import timeit
import glob
import os
import json

doc_fname="test_docs/1706.03762.pdf"
test_id = "1706.03762"


# arXiv

class Arxiv_obj:
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
arxiv = Arxiv_obj()


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

def _rm_self(ids, id):
	if id in ids:
		ids.remove(id)
	return ids

def _strip_version(id):
	return id.split("v")[0]

def get_arxiv_citations(id):
	content = pdf_to_text(id)
	matches = all_arxiv_matches(content)
	matches = [_strip_arxiv(file) for file in matches]
	matches = [_strip_version(file) for file in matches]
	matches = _rm_self(matches, id)
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






# Keeping track of the tree of arxiv papers


class Paperset:
	def __init__(self, repo):
		self.sourceKey = "source"
		self.init_ids = self.initial_repo_to_ids(repo)
		self.ancestors = self.initialize_ancestors()
		self.queue = self.init_ids

	def initial_repo_to_ids(self, initial_repo):
		filepaths = glob.glob(initial_repo)
		filenames = [file.split("/")[-1] for file in filepaths]
		ids = [_strip_version(file.replace(".pdf", "")) for file in filenames]
		return ids

	def initialize_ancestors(self):
		ancestors = {}
		#ancestors[self.sourceKey] = self.init_ids
		return ancestors

	def search_ancestors(self):
		visited = self.queue
		while len(self.queue) > 0:
			paperID = self.queue.pop(0)
			if not os.path.isfile(arxiv.get_dir(paperID)):
				download_pdf(paperID)
			citations = get_arxiv_citations(paperID)
			for parent in citations:
				if parent not in visited:
					self.queue.append(parent)
					visited.append(parent)
			if paperID not in self.ancestors:
				self.ancestors[paperID] = citations
			self.save_ancestors()
			print "Saved!"

	def save_ancestors(self, childName):
		with open('data.json', 'w') as filepath:
			json.dump(self.ancestors, filepath)



#June2017 = Paperset("./june_2017/*.pdf")
#print June2017.init_ids

July = Paperset("./july_2017/*.pdf")
July.search_ancestors()
July.save_ancestors()





#download_pdf(test_id)

#fetch_pdfs(100)

"""

TODO:

 - check to make sure that the list of arxiv things that an article cites 
 	doesn't include itself
 - [optimization] search only the last few pages of PDF file


"""