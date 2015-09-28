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


'''
Databases:

School: 
Name, ID, Address, phone, fax, email, website, sharedspace, totalStudents, gradeSpan, siteAccessibility, SpecialEducation, 
overview

Programs
Name, code, schoolID, grade, interest, admission method, seats, applicants, applicants per seat, description



'''
# Function to scan school to form DB
def createSchoolDB(text):
	print("createSchoolDB")

def createProgDB(text):
	print("createProgDB")

def createSubDB(text):
	print("createSubDB")

def createBusDB(text):
	print("createBusDB")

def createLangDB(text):
	print("createLangDB")

def createAPDB(text):
	print("createAPDB")

def createClubDB(text):
	print("createClubDB")

def createPBDB(text):
	print("createPBDB")

def createPGDB(text):
	print("createPGDB")

def createPercentDB(text):
	print("createPercentDB")

def createProgHiDB(text):
	print("createProgHiDB")

# Function to build "databases" by writing to csv files 
def buildDatabases(db):
	# db is a list of databases to build
	# dbFN are the default filenames
	dbFN = {
		"schools": "schoolDB.txt",
		"programs": "programsDB.txt",
		"subwayToSchool": "subwayDB.txt",
		"buses": "busDB.txt",
		"languages": "langDB.txt",
		"aps": "apDB.txt",
		"clubs": "clubDB.txt",
		"psal_boys": "pBoyDB.txt",
		"psal_girls": "pGirlDB.txt",
		"performance_percentages": "percentDB.txt",
		"program_highlights": "progHiDB.txt"
		}
	# dbIO is the mappings of open files to their strings, default None
	dbIO = {
		"schools": None,
		"programs": None,
		"subwayToSchool": None,
		"buses": None,
		"languages": None,
		"aps": None,
		"clubs": None,
		"psal_boys": None,
		"psal_girls": None,
		"performance_percentages": None,
		"program_highlights": None
	}
	# dbFuncs is the mapping to their respective functions
	dbFuncs = {
		"schools": createSchoolDB,
		"programs": createProgDB,
		"subwayToSchool": createSubDB,
		"buses": createBusDB,
		"languages": createLangDB,
		"aps": createAPDB,
		"clubs": createClubDB,
		"psal_boys": createPBDB,
		"psal_girls": createPGDB,
		"performance_percentages": createPercentDB,
		"program_highlights": createProgHiDB
	}
	# Create file io
	for x in db:
		dbIO[x] = open(dbFN[x],"w")

	#print(dbIO)

	# Separate all schools from each other to build db
	with open("schooldata.txt", "r") as doc:
		# chunk up text into schools by finding instances of ---- END SCHOOL -----\n
		schools = re.split(r"---- END SCHOOL -----", doc.read())
	for s in schools:
		pass



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
					break
			#print(extractedPages)
			# Calculate offset in pages from listed page number
			offset = (pages[p]+1) - extractedPages[0]
			# Set range of pages to convert
			r = []
			if p == (len(pages)-1):
				# 661 is hardcoded from book, will make more general later
				r = range(extractedPages[0]+offset,661)
			else:
				r = range(extractedPages[0]+offset,pages[p+1])
			#print(r)
			textToWrite = ""
			prevSchoolName = ""
			for i in r:
				sbuffer = convert_pdf_to_txt(path,pages=[i])
				sbuffer_raw = repr(sbuffer)
				# Search for school name by looking for "\xe2\x80\xa2 DBN"
				#print(sbuffer_raw)
				match = re.search(r"\\xe2\\x80\\xa2",sbuffer_raw)
				match2 = re.search(r"(\w)+",sbuffer_raw)
				if match == None:
					# No school name
					break
				else:
					#Find beginning of word ignoring new lines and spaces
					name = (sbuffer_raw[match2.start():match.start()]).replace('\n','')
					#Find first captial letter fo name and exclude everything else
					fcl = 0
					for n in name:
						if n.isupper():
							break
						fcl += 1
					name = name[fcl:]
					print(name + " vs " + prevSchoolName)
					if name == prevSchoolName:
						# Continue writing
						textToWrite += sbuffer
					else:
						# A different school
						textToWrite += "\n ----- END SCHOOL ----- \n"
						sd.writelines(textToWrite)
						textToWrite = sbuffer
					prevSchoolName = name

				#print("page "+str(i))
				#print(repr(sbuffer))



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
	elif sys.argv[1] == "buildDB":
		buildDatabases(["schools"])

		