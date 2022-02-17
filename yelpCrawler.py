import requests
import json
import pandas as pd

# Define my API Key, My Endpoint, and My Header
API_KEY = input("Enter API_KEY - ")
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# the first csv for request 
zoneIndex = input('Enter Zone Index - ')
inputFileName = "stockholmCounty_" + str(zoneIndex) +".csv"
outputFileNmae = "stockholmCounty_" + str(zoneIndex) + "_businesses" +".csv"
coordinate = pd.read_csv(inputFileName)

f = []
n = []
for x in range(0,241):
    # find the index of corresponding lat and lng in the imported csv
    lat = coordinate.iloc[x, 6]
    lng = coordinate.iloc[x, 5]
    
    for i in range (0,20):
        PARAMETERS = {#'term': 'food',
                'limit': 50,
                'offset': i * 50,
                'radius': 707,
                'latitude':lat,
                'longitude':lng,
                #'location': 'Stockholm'
                }

        response = requests.get(url = ENDPOINT,
                            params = PARAMETERS,
                            headers = HEADERS)

        business_data = response.json()

        # The key of 'businesses' may or may not valid
        if business_data.get('businesses') != None:
            for j in business_data["businesses"]:
                f.append(j)
        else:
            pass

    # a = business_data["total"]
    # n.append(a)

    # Covert Json to Dataframe"AllCoordinate_part1 - Copy.json" & Drop the duplicated row with same business_id
    df = pd.json_normalize(f)
    df.drop_duplicates(subset='id', keep="first")

    # Export to CSV
    df_ = df.drop_duplicates(subset='id', keep="first")
    df_.to_csv(outputFileNmae)