#!/bin/bash
SCRAPERSCRIPT=~/documents/github/hotelscraper-py/scraper.py
source ./py-env/bin/activate

python3 ${SCRAPERSCRIPT}
if [ $? -ne 0 ]
then
    echo "Something went wrong in the Python script -- Cancelled execution"
    exit 1
fi

WRITE_HOTELS_JSON_FILE=~/documents/github/hotelscraper-py/writeHotels.json
DESTINATION_JSON_FILE=~/documents/github/ophold/src/data/hotels/hotels.json
echo "Writing to file"
echo $(<$WRITE_HOTELS_JSON_FILE) > $DESTINATION_JSON_FILE

echo "Commiting"
cd ~/documents/github/ophold
git add src/data/hotels/hotels.json
git commit -m "Updated prices: $(date +%m-%d-%Y)"
git push -u origin master
echo "Done!"
