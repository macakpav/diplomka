#/bin/sh

./clean.sh
cp data/*.csv .
python3 processData.py

cd plots
plotnames="Uy UyA Fy FyA"
for plot in $plotnames; do
    echo Creating figure \'$plot.pdf\'...
    pdflatex -synctex=0 -interaction=batchmode $plot.tex > /dev/null
done
echo Done.
