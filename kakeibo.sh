if [ $# != 2 ];then
	echo "usage: ./kakeibo.sh <year> <month>"
	exit 1
fi
year=$1
month=$2

./kakeibo.py data.evernote.$year$month

awk 'NR>=2{print}' log.txt | sort > sorted.txt
head -1 log.txt > detail.txt
cat sorted.txt >> detail.txt

./kakeibo_plot.py all 'ro-' < all.csv
./kakeibo_plot.py shokuhi 'bo-' < shokuhi.csv
./kakeibo_plot.py gaishokuhi 'yo-' < gaishokuhi.csv
perl -pe "s/\|yearstr\|/$year/" template.rst| perl -pe "s/\|monthstr\|/$month/" > kakeibo-$year$month.rst
#./kakeibo-data2rst.py data.evernote.$year$month >> kakeibo-$year$month.rst
./kakeibo-data2rst.py detail.txt >> kakeibo-$year$month.rst
rst2pdf kakeibo-$year$month.rst -s rst2pdf_ja.style -o kakeibo_$year-$month.pdf
echo "saved: kakeibo_$year-$month.pdf"

# clean up
rm all.csv shokuhi.csv gaishokuhi.csv kakeibo-$year$month.rst *.png
rm log.txt sorted.txt detail.txt

