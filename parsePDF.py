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
def extractSchoolName(sbuffer_raw):
	#match = re.search(r"\\xe2\\x80\\xa2",sbuffer_raw)
	#match2 = re.search(r"(\w)+",sbuffer_raw)
	#match3 = re.search(r"((\\n\\n)|^)[\w\s\\\(\)\.\-&:'\"\d]*?(\\xe2\\x80\\x99)?[\w\\\(\)\.\-&:'\"\d]*?(\\xe2\\x80\\xa2)",sbuffer_raw)
	match3 = re.search(r"^.+?DBN\s+?[\d\w]{6}",sbuffer_raw,re.MULTILINE)
	if match3 == None:
		# No school name
		print("No name found")
		print(sbuffer_raw)
		return None
	else:
		#Find beginning of word ignoring new lines and spaces
		name = (sbuffer_raw[match3.start():match3.end()]).replace('\n','')
		#print(name)
		#Find first captial letter fo name and exclude everything else
		#print(sbuffer_raw)
		fcl = 0
		for n in name:
			if n.isupper():
				break
			fcl += 1
		return name[fcl:-14]

# Functions to scan school to form DB
def createSchoolDB(text,f):
	# Find each category in the text and write to f
	#Name, ID, Address, phone, fax, email, website, sharedspace, totalStudents, gradeSpan, siteAccessibility, SpecialEducation, overview
	#print(extractSchoolName(raw_text))
	Name = extractSchoolName(text)
	print(Name)
	if Name == None:
		return None
	#ID
	matchObj = re.search(r"DBN\s[\d\w]{6}",text,re.MULTILINE)
	ID = text[matchObj.start()+4:matchObj.end()]
	print("ID ="+ID)
	#Address
	matchObj = re.search(r"^Address:.*?,.*?$",text,re.MULTILINE|re.DOTALL)
	if matchObj==None:
		print("No address found")
	else:
		Address = (((text[matchObj.start()+8:matchObj.end()]).strip()).replace("\n\n",", ")).replace("\n",", ")
		print("Address: "+Address)

	#Phone
	matchObj = re.search(r"^Phone.*",text,re.MULTILINE)
	if matchObj==None:
		print("No Phone # found")
	else:
		Phone= text[matchObj.start()+7:matchObj.end()]
		print("Phone #: "+Phone)
	#fax
	matchObj = re.search(r"^Fax.*",text,re.MULTILINE)
	if matchObj==None:
		print("No Fax # found")
	else:
		Fax= text[matchObj.start()+4:matchObj.end()]
		print("Fax #: "+Fax)
	#website
	matchObj = re.search(r"^Website.*",text,re.MULTILINE)
	if matchObj==None:
		print("No Phone # found")
	else:
		WS= text[matchObj.start()+8:matchObj.end()]
		print("Website: "+WS)
	#sharedspace
	matchObj = re.search(r"^Shared\sSpace:.*",text,re.MULTILINE)
	if matchObj==None:
		print("No SHaredSpace found")
	else:
		SS= text[matchObj.start()+13:matchObj.end()]
		print("Shared Space: "+SS)
	#totalStudents
	matchObj = re.search(r"^Total\sStudents\sin\sSchool:.*",text,re.MULTILINE)
	if matchObj==None:
		print("No numStudents found")
	else:
		numStudents= text[matchObj.start()+26:matchObj.end()]
		print("numStudents: "+numStudents)
	#Gradespan
	matchObj = re.search(r"^Grade\sSpan\sof\sSchool.*",text,re.MULTILINE)
	if matchObj==None:
		print("No Grade Span found")
	else:
		GS= text[matchObj.start()+34:matchObj.end()]
		print("Grade Span: "+GS)
	#Site accessibility
	matchObj = re.search(r"^Site\sAccessibility:.*",text,re.MULTILINE)
	if matchObj==None:
		print("No Site Accessibility found")
	else:
		SA= (text[matchObj.start()+19:matchObj.end()]).strip()
		print("Site Accessibility: "+SA)
	#specialEdu
	matchObj = re.search(r"^Special\s*Education\s*Services.*",text,re.MULTILINE)
	if matchObj==None:
		print("No SE found")
	else:
		SE= text[matchObj.start()+31:matchObj.end()]
		print("Special Education Services: "+SE)
	#overview
	matchObj = re.search(r"^Overview.*?\.\s*$",text,re.MULTILINE|re.DOTALL)
	if matchObj==None:
		print("No Overview # found")
	else:
		OV= text[matchObj.start()+10:matchObj.end()]
		print("Overview : "+OV)
	stringToWrite =Name+","+ID+","+Address+","+Phone+","+Fax+","+WS+","+SS+","+numStudents+","+GS+","+SA+","+SE+","+OV+"\n"
	f.write(stringToWrite)

def createProgDB(text,f):
	print("createProgDB")

def createSubDB(text,f):
	print("createSubDB")

def createBusDB(text,f):
	print("createBusDB")

def createLangDB(text,f):
	print("createLangDB")

def createAPDB(text,f):
	print("createAPDB")

def createClubDB(text,f):
	print("createClubDB")

def createPBDB(text,f):
	print("createPBDB")

def createPGDB(text,f):
	print("createPGDB")

def createPercentDB(text,f):
	print("createPercentDB")

def createProgHiDB(text,f):
	print("createProgHiDB")

# Function to build "databases" by writing to csv files 
def buildDatabases(db):
	# db is a list of databases to build
	dbCategories = {
		"schools": "name, id, address, phone, fax, email, website, sharedSpace, totalStudents, gradeSpan, siteAccessibility, specialEducation, overview\n",
		"programs": "name, code, schoolID, grade, interest, admission method, seats, applicants, applicantsPerSeat, description\n",
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
		dbIO[x].write(dbCategories[x])

	#print(dbIO)

	# Separate all schools from each other to build db
	with open("schooldata.txt", "r") as doc:
		# chunk up text into schools by finding instances of ---- END SCHOOL -----\n
		schools = re.split(r"---- END SCHOOL -----", doc.read())
	#print("Number of schools : " + str(len(schools)))
	for s in schools:
		for x in db:
			val = dbFuncs[x](s,dbIO[x])
			if val == None:
				next

	# close all the IOs
	for key, val in dbIO.iteritems():
		if not val == None:
			val.close()



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
				#sbuffer_raw = repr(sbuffer)
				# Search for school name by looking for "\xe2\x80\xa2 DBN"
				#print(sbuffer_raw)
				name = extractSchoolName(sbuffer)
				if name == None:
					#print(sbuffer_raw + '\n\n\n')
					next
				else:
					print(name + " vs " + prevSchoolName)
					#print(sbuffer_raw + '\n\n\n')
					if name == prevSchoolName:
						# Continue writing
						textToWrite += sbuffer
					else:
						# A different school
						textToWrite += "\n ----- END SCHOOL ----- \n"
						sd.writelines(textToWrite)
						textToWrite = sbuffer
					prevSchoolName = name


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

		