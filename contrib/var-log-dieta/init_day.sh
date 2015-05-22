#! /bin/bash
set -u

cd $(dirname 0)

DATE=${1:-$(date +%F)}

echo "Initting $DATE"

mkdir -p data/{juli,log}/$DATE/{01-desayuno,02-media-manana,03-almuerzo,04-postre,05-merienda,06-cena,07-postre}
touch data/{juli,log}/$DATE/{01-desayuno,02-media-manana,03-almuerzo,04-postre,05-merienda,06-cena,07-postre}/__init__
touch data/{juli,log}/$DATE/__init__
