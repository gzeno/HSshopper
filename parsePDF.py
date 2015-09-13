'''
	Author: Raymond Tse
	8/8/2015

	Program to parse through PDF and write info as text files


'''
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import re
import sys


# Function to generate text files of parsed table of contents files
def gen_TOC(path,pages):
	for p in pages:
		#print("reading page "+str(p))
		# Set filename, open it and write to it
		toc = open("toc_"+str(p)+".txt","w")
		# parse the page and write content to opened file
		t = convert_pdf_to_txt(path,pages=[p])
		t = parseTocText(t)
		toc.write(t)
		toc.close()
		#print("finished writing page "+str(p))

# Function to parse toc lines and remove extra new lines and "."
def parseTocText(t):
	# Convert to see \n s
	newt = repr(t)
	newt = re.sub(r"(\.)+",".",newt)
	#print(newt)
	newt = re.sub(r"\s+(\\n)+\s+"," ",newt)
	print(newt)
	# Convert back to normal strings
	return (eval(newt))

# Function to go through pages as listed by toc
def transTocToPages(pages):
	with open("schooldata.txt","w") as sd:
		for p in range(len(pages)):
			pgnm = "toc_"+str(pages[p])+".txt"
			lines = []
			with open(pgnm) as toc:
				lines = toc.read().splitlines()
			#print lines
			# store page numbers all into a list
			extractedPages = []
			for l in range(1,len(lines)-1):
				if lines[l] == "":
					pass
				else:
					extractedPages.append(extractPageNum(lines[l]))
			#print(extractedPages)
			# Calculate offset in pages from listed page number
			offset = (pages[p]+1) - extractedPages[0]
			for i in range(len(extractedPages)):
				text = ""
				if i == len(extractedPages) - 1:
					# Work up to next table of contents page
					text = convert_pdf_to_txt(path,pages=range(extractedPages[i]+offset,pages[p+1]))
				else:
					text = convert_pdf_to_txt(path,pages=range(extractedPages[i]+offset,extractedPages[i+1]+offset))
					#for j in range(extractedPages[i]+offset,extractedPages[i+1]+offset):
					#	print(j)
				text += "\n --- END --- \n"
				print(text)
				sd.writelines(text)
			print("\nFinished borough\n")


# Function to parse page number from line
def extractPageNum(line):
	i = [x for x, v in enumerate(line) if v == '.'][-1]
	#print(line)
	#print line[i+1:]
	return int(line[i+1:].strip())


# Code taken from stack overflow http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library/20905381#20905381
def convert_pdf_to_txt(path,pages=None):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    if pages==None:
    	pagenos=set(range(1,501))
    else:
    	pagenos=set(pages)
    #print(pagenos)
    
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


if __name__ == "__main__":
	# arg to parse a table of contents into a plain text
	path = "./2016HighSchoolDirectory_English.pdf"
	tocpages = [29,181,361,517,642]
	# generate TOC pages
	if sys.argv[1] == "toc":
		gen_TOC(path,tocpages)
	elif sys.argv[1] == "transPages":
		transTocToPages(tocpages)