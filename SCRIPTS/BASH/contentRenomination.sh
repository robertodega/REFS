cd /percorso/alla/cartella
i=1
for file in *.jpg; do
  mv "$file" $(printf "%03d.jpg" $i)
  ((i++))
done
