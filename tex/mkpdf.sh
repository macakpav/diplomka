#!/bin/bash

if [ "$#" -ne "1" ]; then
	echo "Error: Exactly one argument is required (main file name)."
	exit 1
fi

echo ":::: CLEAN BUILD OF $1 ::::"

cd "$(dirname "$0")" # go into directory of script

name="${1%%.tex}"
echo "Name is $name"
echo "Removing files..."
rm -f "${name}.toc"
rm -f "${name}.run.xml"
rm -f "${name}.out"
rm -f "${name}.nlo"
rm -f "${name}.log"
rm -f "${name}.bcf"
rm -f "${name}.aux"
rm -f "${name}.nls"
rm -f "${name}.ilg"
rm -f "${name}.idx"
rm -f "${name}.blg"
rm -f "${name}.bbl"

echo "First compilation..."
pdflatex "${name}.tex" > /dev/null
if [ -e "${name}.bcf" ]
then
	echo "Bibtex compilation..."
    bibtex -quiet "${name}"
fi

if [ -e "${name}.nlo" ]
then
	echo "Makeindex compilation..."
    makeindex -q "${name}.nlo" -s nomencl.ist -o "${name}.nls"
fi

echo "Last 3 compilations..."
pdflatex "${name}.tex" > /dev/null
pdflatex "${name}.tex" > /dev/null
# cf. https://tex.stackexchange.com/questions/27878
pdflatex -shell-escape -interaction=nonstopmode -file-line-error "${name}.tex" | grep -i ".*:[0-9]*:.*\|warning" 
echo "Done."
# xdg-open "${name}.pdf"
