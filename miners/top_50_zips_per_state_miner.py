import requests
from bs4 import BeautifulSoup
import re

from main import get_schools_by_zip_code

cache = set()

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
          "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
          "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
          "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
          "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
          "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
          "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
          "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

with open('districts.csv', 'w') as districts_file:
    for state in states:
        print(state)
        r = requests.get('http://worldpopulationreview.com/zips/' + '-'.join(state.lower().split()))
        soup = BeautifulSoup(r.text, 'html.parser')
        zip_codes = soup.find_all('a', {'href': re.compile(r'/zips/\d{5}/')})
        for zip_code in zip_codes:
            districts = get_schools_by_zip_code(zip_code.text)
            for district in districts:
                district_hash = hash(district['PvueURL'])
                if district_hash not in cache:
                    print(district)
                    districts_file.write(','.join(district.values()))
                    districts_file.write('\n')
                    districts_file.flush()
                    cache.add(district_hash)
