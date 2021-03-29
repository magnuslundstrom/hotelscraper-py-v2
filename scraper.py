import requests
import threading
import bs4
import json

open('writeHotels.json', 'w').close()
hotelsJSON = open('hotels.json')
data = json.load(hotelsJSON)
updatedHotels = []

def getPrice(startIdx, endIdx):
    for url in range(startIdx, endIdx):
        try:
            if 'hotels.com' in data[url]['link']:
                res = requests.get(data[url]['link'])
                res.raise_for_status() # maybe delete later
                soup = bs4.BeautifulSoup(res.text, 'html.parser')
                priceElem = soup.select_one('.current-price')
    
                if not priceElem:
                    print("Could not get price for: %s" % data[url]['name'])
                    updatedHotels.append(data[url])
                else:
                    price = priceElem.getText().replace(' DKK', '')
                    print(f'Found a new price for {data[url]["name"]} - it is: {price}')
                    data[url]['price'] = price
                    updatedHotels.append(data[url])
            else:
                print("Failed completely to get price for: %s" % data[url]['name'])
                updatedHotels.append(data[url])
        except:
            print("Couldn't fetch price for %s - Probably not provided a Hotels.com link" % data[url]['name'])
            updatedHotels.append(data[url])

length = len(data)
scrapeThreads = []

for i in range(0, length, 10):
    start = i
    end = length - start
    if end > 10:
        end = i + 10
    else:
        end += i
    
    scrapeThread = threading.Thread(target=getPrice, args=(start,end))
    scrapeThread.start()
    scrapeThreads.append(scrapeThread)

    if len(scrapeThreads) >= 4: # Cap the threading to 4 threads... We don't really need more atm.
        for thread in scrapeThreads:
            thread.join()
            scrapeThreads = [] # Reset so we can fill it up again

for thread in scrapeThreads:
    thread.join()

hotelsJSON.close()

writeHotelsFile = open('writeHotels.json', 'w', encoding='utf8')
json.dump(updatedHotels, writeHotelsFile, ensure_ascii=False)
writeHotelsFile.close()

print("Done With Scraping and file has been saved!")

