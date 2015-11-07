#!/bin/sh
# This script will run parsePDF.py to build databases and also copy db with postgres
python parsePDF.py buildDB



dbname="nychsproj"
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.4/bin

psql $dbname <<- EOS
	delete from school; 
	copy "school" from '/Users/RaymondTse/Desktop/nychsproj/schoolDB.csv' with csv header;
EOS
