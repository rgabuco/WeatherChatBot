import json
import requests
import os
from datetime import datetime
import string

def get_country_code(country_name):
    """Convert country names to ISO country codes"""
    # Official countries that include "The" in their name
    official_the_countries = {
        'bahamas': ('BS', 'The Bahamas'),
        'gambia': ('GM', 'The Gambia'),
        'netherlands': ('NL', 'The Netherlands'),
        'philippines': ('PH', 'The Philippines'),
        'united arab emirates': ('AE', 'The United Arab Emirates'),
        'united kingdom': ('GB', 'The United Kingdom'),
        'united states': ('US', 'The United States')
    }
    
    country_codes = {
        # North America
        'united states': 'US', 'usa': 'US', 'america': 'US', 'us': 'US',
        'united states of america': 'US',
        'canada': 'CA',
        'mexico': 'MX',
        'greenland': 'GL',

        # Central America
        'belize': 'BZ',
        'costa rica': 'CR',
        'el salvador': 'SV',
        'guatemala': 'GT',
        'honduras': 'HN',
        'nicaragua': 'NI',
        'panama': 'PA',

        # Southeast Asia
        'brunei': 'BN',
        'cambodia': 'KH',
        'indonesia': 'ID',
        'laos': 'LA',
        'malaysia': 'MY', 'burma': 'MM',
        'singapore': 'SG',
        'thailand': 'TH',
        'timor-leste': 'TL', 'east timor': 'TL',
        'vietnam': 'VN',

        # Central America
        'cuba': 'CU',
        'dominica': 'DM',
        'dominican republic': 'DO',
        'grenada': 'GD',
        'haiti': 'HT',
        'jamaica': 'JM',
        'saint kitts and nevis': 'KN',
        'saint lucia': 'LC',
        'saint vincent and the grenadines': 'VC',
        'trinidad and tobago': 'TT',

        # South America
        'argentina': 'AR',
        'bolivia': 'BO',
        'brazil': 'BR',
        'chile': 'CL',
        'colombia': 'CO',
        'ecuador': 'EC',
        'guyana': 'GY',
        'paraguay': 'PY',
        'peru': 'PE',
        'suriname': 'SR',
        'uruguay': 'UY',
        'venezuela': 'VE',

        # Western Europe
        'france': 'FR',
        'germany': 'DE',
        'belgium': 'BE',
        'luxembourg': 'LU',
        'ireland': 'IE',
        'switzerland': 'CH',
        'liechtenstein': 'LI',
        'monaco': 'MC',
        'andorra': 'AD',
        'san marino': 'SM',
        'vatican city': 'VA',

        # Northern Europe
        'denmark': 'DK',
        'finland': 'FI',
        'iceland': 'IS',
        'norway': 'NO',
        'sweden': 'SE',
        'faroe islands': 'FO',

        # Southern Europe
        'albania': 'AL',
        'bosnia and herzegovina': 'BA',
        'croatia': 'HR',
        'greece': 'GR',
        'italy': 'IT',
        'malta': 'MT',
        'montenegro': 'ME',
        'north macedonia': 'MK', 'macedonia': 'MK',
        'portugal': 'PT',
        'serbia': 'RS',
        'slovenia': 'SI',
        'spain': 'ES',

        # Eastern Europe
        'belarus': 'BY',
        'bulgaria': 'BG',
        'czech republic': 'CZ', 'czechia': 'CZ',
        'estonia': 'EE',
        'hungary': 'HU',
        'latvia': 'LV',
        'lithuania': 'LT',
        'moldova': 'MD',
        'poland': 'PL',
        'romania': 'RO',
        'slovakia': 'SK',
        'ukraine': 'UA',

        # Northern Asia (Siberia)
        'russia': 'RU',

        # Central Asia
        'kazakhstan': 'KZ',
        'kyrgyzstan': 'KG',
        'tajikistan': 'TJ',
        'turkmenistan': 'TM',
        'uzbekistan': 'UZ',

        # East Asia
        'china': 'CN',
        'japan': 'JP',
        'mongolia': 'MN',
        'north korea': 'KP',
        'south korea': 'KR',
        'taiwan': 'TW',
        'hong kong': 'HK',
        'macau': 'MO',

        # South Asia
        'afghanistan': 'AF',
        'bangladesh': 'BD',
        'bhutan': 'BT',
        'india': 'IN',
        'maldives': 'MV',
        'nepal': 'NP',
        'pakistan': 'PK',
        'sri lanka': 'LK',

        # Middle East
        'bahrain': 'BH',
        'cyprus': 'CY',
        'israel': 'IL',
        'iraq': 'IQ',
        'iran': 'IR',
        'jordan': 'JO',
        'kuwait': 'KW',
        'lebanon': 'LB',
        'oman': 'OM',
        'palestine': 'PS',
        'qatar': 'QA',
        'saudi arabia': 'SA',
        'turkey': 'TR', 'turkiye': 'TR',
        'yemen': 'YE',

        # Central Africa
        'cameroon': 'CM',
        'central african republic': 'CF',
        'chad': 'TD',
        'congo': 'CG',
        'democratic republic of the congo': 'CD', 'dr congo': 'CD',
        'equatorial guinea': 'GQ',
        'gabon': 'GA',
        'sao tome and principe': 'ST',

        # East Africa
        'burundi': 'BI',
        'comoros': 'KM',
        'djibouti': 'DJ',
        'eritrea': 'ER',
        'ethiopia': 'ET',
        'kenya': 'KE',
        'madagascar': 'MG',
        'malawi': 'MW',
        'mauritius': 'MU',
        'mozambique': 'MZ',
        'rwanda': 'RW',
        'seychelles': 'SC',
        'somalia': 'SO',
        'south sudan': 'SS',
        'tanzania': 'TZ',
        'uganda': 'UG',
        'zambia': 'ZM',
        'zimbabwe': 'ZW',

        # North Africa
        'algeria': 'DZ',
        'egypt': 'EG',
        'libya': 'LY',
        'morocco': 'MA',
        'sudan': 'SD',
        'tunisia': 'TN',
        'western sahara': 'EH',

        # Southern Africa
        'angola': 'AO',
        'botswana': 'BW',
        'eswatini': 'SZ', 'swaziland': 'SZ',
        'lesotho': 'LS',
        'namibia': 'NA',
        'south africa': 'ZA',

        # West Africa
        'benin': 'BJ',
        'burkina faso': 'BF',
        'cape verde': 'CV',
        'ivory coast': 'CI', 'cote d\'ivoire': 'CI',
        'mali': 'ML',
        'mauritania': 'MR',
        'niger': 'NE',
        'nigeria': 'NG',
        'senegal': 'SN',
        'sierra leone': 'SL',
        'togo': 'TG',

        # Oceania
        'australia': 'AU',
        'fiji': 'FJ',
        'kiribati': 'KI',
        'marshall islands': 'MH',
        'micronesia': 'FM',
        'nauru': 'NR',
        'new zealand': 'NZ',
        'palau': 'PW',
        'papua new guinea': 'PG',
        'samoa': 'WS',
        'solomon islands': 'SB',
        'tonga': 'TO',
        'tuvalu': 'TV',
        'vanuatu': 'VU',
    }
    
    # Convert input to lowercase for case-insensitive matching
    if not country_name:
        return None
    
    # Clean and normalize input
    normalized = country_name.lower().strip()
    
    # Remove 'the ' prefix if present
    if normalized.startswith('the '):
        normalized = normalized[4:].strip()
    
    # First check if it's one of the official "The" countries
    for official_name, (code, display_name) in official_the_countries.items():
        if normalized == official_name or normalized == official_name.replace('the ', ''):
            return code
    
    # Then check regular country codes
    return country_codes.get(normalized)

def get_display_country_name(country_name):
    """Get the proper display name for a country, including 'The' where official"""
    # Official countries that include "The" in their name
    official_the_countries = {
        'bahamas': 'The Bahamas',
        'gambia': 'The Gambia',
        'netherlands': 'The Netherlands',
        'philippines': 'The Philippines',
        'united arab emirates': 'The United Arab Emirates',
        'united kingdom': 'The United Kingdom',
        'united states': 'The United States'
    }
    
    if not country_name:
        return country_name
    
    # Clean and normalize input
    normalized = country_name.lower().strip()
    
    # Remove 'the ' prefix if present
    if normalized.startswith('the '):
        normalized = normalized[4:].strip()
    
    # Check if it's one of the official "The" countries
    for official_name, display_name in official_the_countries.items():
        if normalized == official_name or normalized == official_name.replace('the ', ''):
            return display_name
    
    # For other countries, just capitalize each word
    return country_name.title()

def get_major_cities(country):
    """Return major cities for common countries with context"""
    major_cities = {
        # North America
        'us': [
            ('New York', 'largest city'),
            ('Los Angeles', 'west coast hub'),
            ('Chicago', 'third largest city'),
            ('Houston', 'largest city in Texas'),
            ('Phoenix', 'desert metropolis'),
            ('Philadelphia', 'historic city'),
            ('San Antonio', 'texas landmark'),
            ('San Diego', 'coastal city'),
            ('Dallas', 'major business hub'),
            ('San Jose', 'silicon valley'),
            ('Miami', 'southern hub'),
            ('Atlanta', 'southern metropolis'),
            ('Boston', 'historic capital'),
            ('San Francisco', 'bay area hub'),
            ('Seattle', 'pacific northwest'),
            ('Denver', 'mile high city'),
            ('Washington', 'capital city'),
            ('Las Vegas', 'entertainment capital'),
            ('Portland', 'oregon hub'),
            ('Detroit', 'motor city')
        ],
        'ca': [
            ('Toronto', 'largest city'),
            ('Montreal', 'french metropolis'),
            ('Vancouver', 'west coast hub'),
            ('Calgary', 'prairie metropolis'),
            ('Edmonton', 'northern hub'),
            ('Ottawa', 'capital city'),
            ('Quebec', 'historic capital'),
            ('Winnipeg', 'central hub'),
            ('Hamilton', 'industrial center'),
            ('Halifax', 'atlantic gateway')
        ],
        'mx': [
            ('Mexico City', 'capital and largest'),
            ('Guadalajara', 'second largest'),
            ('Monterrey', 'business hub'),
            ('Tijuana', 'border city'),
            ('Cancun', 'tourist destination'),
            ('Merida', 'yucatan capital'),
            ('Acapulco', 'pacific resort')
        ],

        # South America
        'br': [
            ('Sao Paulo', 'largest city'),
            ('Rio de Janeiro', 'tourist capital'),
            ('Brasilia', 'capital city'),
            ('Salvador', 'cultural center'),
            ('Manaus', 'amazon gateway')
        ],
        'ar': [
            ('Buenos Aires', 'capital city'),
            ('Cordoba', 'second city'),
            ('Rosario', 'port city'),
            ('Mendoza', 'wine country')
        ],

        # Europe
        'gb': [
            ('London', 'capital city'),
            ('Manchester', 'northern hub'),
            ('Birmingham', 'second city'),
            ('Liverpool', 'historic port'),
            ('Glasgow', 'scottish metropolis'),
            ('Edinburgh', 'scottish capital'),
            ('Leeds', 'yorkshire hub'),
            ('Bristol', 'western gateway'),
            ('Cardiff', 'welsh capital')
        ],
        'fr': [
            ('Paris', 'capital city'),
            ('Lyon', 'second city'),
            ('Marseille', 'mediterranean port'),
            ('Toulouse', 'aerospace center'),
            ('Bordeaux', 'wine capital'),
            ('Strasbourg', 'european hub')
        ],
        'de': [
            ('Berlin', 'capital city'),
            ('Hamburg', 'major port'),
            ('Munich', 'southern capital'),
            ('Frankfurt', 'financial hub'),
            ('Stuttgart', 'auto city'),
            ('Dusseldorf', 'fashion capital')
        ],
        'it': [
            ('Rome', 'eternal city'),
            ('Milan', 'fashion capital'),
            ('Naples', 'southern hub'),
            ('Turin', 'northern center'),
            ('Florence', 'art capital'),
            ('Venice', 'canal city')
        ],
        'es': [
            ('Madrid', 'capital city'),
            ('Barcelona', 'catalan capital'),
            ('Valencia', 'mediterranean hub'),
            ('Seville', 'southern center'),
            ('Bilbao', 'basque city')
        ],

        # Asia
        'jp': [
            ('Tokyo', 'capital city'),
            ('Osaka', 'commerce hub'),
            ('Kyoto', 'cultural capital'),
            ('Yokohama', 'port city'),
            ('Sapporo', 'northern capital'),
            ('Nagoya', 'industrial center'),
            ('Fukuoka', 'southern gateway')
        ],
        'kr': [
            ('Seoul', 'capital city'),
            ('Busan', 'port city'),
            ('Incheon', 'gateway city'),
            ('Daegu', 'southern hub'),
            ('Daejeon', 'tech center')
        ],
        'cn': [
            ('Beijing', 'capital city'),
            ('Shanghai', 'financial hub'),
            ('Guangzhou', 'southern center'),
            ('Shenzhen', 'tech hub'),
            ('Chengdu', 'western capital'),
            ('Tianjin', 'northern port'),
            ('Xian', 'ancient capital')
        ],
        'in': [
            ('Mumbai', 'financial capital'),
            ('Delhi', 'capital region'),
            ('Bangalore', 'tech hub'),
            ('Chennai', 'southern gateway'),
            ('Kolkata', 'cultural capital'),
            ('Hyderabad', 'tech center'),
            ('Pune', 'education hub')
        ],
        'sg': [
            ('Singapore', 'city-state')
        ],
        'ph': [
            ('Manila', 'capital city'),
            ('Cebu', 'second city'),
            ('Davao', 'mindanao hub')
        ],
        'th': [
            ('Bangkok', 'capital city'),
            ('Phuket', 'island hub'),
            ('Chiang Mai', 'northern capital')
        ],

        # Australia & New Zealand
        'au': [
            ('Sydney', 'largest city'),
            ('Melbourne', 'cultural capital'),
            ('Brisbane', 'queensland capital'),
            ('Perth', 'western capital'),
            ('Adelaide', 'southern hub'),
            ('Canberra', 'capital city'),
            ('Gold Coast', 'tourist hub')
        ],
        'nz': [
            ('Auckland', 'largest city'),
            ('Wellington', 'capital city'),
            ('Christchurch', 'garden city'),
            ('Hamilton', 'waikato hub')
        ],

        # Middle East
        'ae': [
            ('Dubai', 'largest city'),
            ('Abu Dhabi', 'capital city'),
            ('Sharjah', 'cultural hub')
        ],
        'sa': [
            ('Riyadh', 'capital city'),
            ('Jeddah', 'port city'),
            ('Mecca', 'holy city'),
            ('Medina', 'holy city')
        ],

        # Africa
        'za': [
            ('Johannesburg', 'largest city'),
            ('Cape Town', 'mother city'),
            ('Durban', 'port city'),
            ('Pretoria', 'capital city')
        ],
        'eg': [
            ('Cairo', 'capital city'),
            ('Alexandria', 'mediterranean hub'),
            ('Luxor', 'ancient capital')
        ],

        # Central America
        'cr': [
            ('San Jose', 'capital city'),
            ('Liberia', 'tourist gateway')
        ],
        'pa': [
            ('Panama City', 'capital')
        ]
    }
    
    # Convert input to lowercase and get country code if needed
    if not country:
        return [('Please specify a city name', 'for accurate weather information')]
        
    country_lower = country.lower().strip()
    
    # If input is a full country name, get its code
    if len(country_lower) > 2:
        country_code = get_country_code(country_lower)
        if country_code:
            country_lower = country_code.lower()
    
    # If the country code isn't in our dictionary, return a generic message
    if country_lower not in major_cities:
        return [('Please specify a major city name in this country', 'for accurate weather information')]
    
    return major_cities.get(country_lower, [])

def is_gibberish(text):
    """Check if input looks like gibberish/random characters"""
    if not text:
        return False
        
    # Check for repeated characters
    if any(c * 3 in text.lower() for c in 'abcdefghijklmnopqrstuvwxyz'):
        return True
        
    # Check for keyboard mashing patterns
    keyboard_patterns = ['asdf', 'qwer', 'zxcv', 'hjkl', 'jkl', 'dfg', 'xcv']
    if any(pattern in text.lower() for pattern in keyboard_patterns):
        return True
    
    # Check consonant to vowel ratio
    consonants = sum(1 for c in text.lower() if c in 'bcdfghjklmnpqrstvwxyz')
    vowels = sum(1 for c in text.lower() if c in 'aeiou')
    if vowels == 0 and consonants > 3:  # No vowels and multiple consonants
        return True
        
    return False

def suggest_cities():
    """Suggest popular cities to check weather for"""
    suggestions = [
        ('New York', 'US', 'major global city'),
        ('London', 'GB', 'popular destination'),
        ('Tokyo', 'JP', 'largest city in Japan'),
        ('Paris', 'FR', 'capital of France'),
        ('Sydney', 'AU', 'major Australian city'),
        ('Dubai', 'AE', 'middle eastern hub'),
        ('Singapore', 'SG', 'asian technology hub'),
        ('Toronto', 'CA', 'Canadian metropolis')
    ]
    return suggestions[:]

def clean_location_name(location):
    """Clean location name by removing punctuation and extra whitespace"""
    if not location:
        return location
    # Remove punctuation except hyphens and apostrophes
    punctuation_to_remove = string.punctuation.replace("-", "").replace("'", "")
    # First clean the ends of the string from all punctuation including ? . ! etc
    location = location.strip(string.punctuation + ' ')
    # Then only remove specific punctuation from within the string, keeping hyphens and apostrophes
    location = ''.join(char for char in location if char not in punctuation_to_remove)
    # Clean up any extra whitespace
    location = ' '.join(location.split())
    return location

def parse_location(input_text):
    """Smart location parser"""
    if not input_text:
        return None, None
        
    # Debug print
    print(f"Original input before cleaning: '{input_text}'")
    
    # Clean input and convert to lowercase for better matching
    input_lower = input_text.lower().strip()
    
    # Comprehensive list of prefixes to remove
    prefixes_to_remove = [
        # Temperature specific patterns
        "what's the temperature in", "what is the temperature in",
        "how's the temperature in", "how is the temperature in",
        "temperature in", "temperature at", "temperature of",
        "what's the temp in", "what is the temp in",
        "how's the temp in", "how is the temp in",
        "temp in", "temp at", "temp of",
        "current temperature in", "current temp in",
        
        # Question forms with "the weather"
        "how's the weather in", "how is the weather in",
        "what's the weather in", "what is the weather in",
        "what's the weather like in", "what is the weather like in",
        "how's the weather like in", "how is the weather like in",
        
        # Question forms without "the"
        "how's weather in", "how is weather in",
        "what's weather in", "what is weather in",
        "what's weather like in", "what is weather like in",
        "how's weather like in", "how is weather like in",
        
        # Show/Tell/Get forms with "the weather"
        "show me the weather in", "show the weather in",
        "tell me the weather in", "tell the weather in",
        "get me the weather in", "get the weather in",
        "give me the weather in", "give the weather in",
        "check the weather in",
        
        # Show/Tell/Get forms without "the"
        "show me weather in", "show weather in",
        "tell me weather in", "tell weather in",
        "get me weather in", "get weather in",
        "give me weather in", "give weather in",
        "check weather in",
        
        # Direct weather queries with "the"
        "the weather in", "the temperature in",
        "the forecast in", "the conditions in",
        
        # Direct weather queries without "the"
        "weather in", "weather for", "weather at", "weather of",
        "temperature in", "temperature at", "temperature for",
        "forecast in", "forecast for",
        "conditions in", "conditions at", "conditions for",
        
        # Current/Now variations with "the"
        "current the weather in", "the current weather in",
        "the weather right now in", "the weather now in",
        
        # Current/Now variations without "the"
        "current weather in", "weather right now in", "weather now in",
        
        # Can you/Could you variations
        "can you tell me the weather in", "could you tell me the weather in",
        "can you show me the weather in", "could you show me the weather in",
        "can you check the weather in", "could you check the weather in",
        
        # Temperature variations with can/could
        "can you tell me the temperature in", "could you tell me the temperature in",
        "can you show me the temperature in", "could you show me the temperature in",
        "can you check the temperature in", "could you check the temperature in",
        
        # Can you/Could you variations without "the"
        "can you tell me weather in", "could you tell me weather in",
        "can you show me weather in", "could you show me weather in",
        "can you check weather in", "could you check weather in",
        
        # I want/I'd like variations
        "i want to know the weather in", "i'd like to know the weather in",
        "i want to see the weather in", "i'd like to see the weather in",
        "i want to check the weather in", "i'd like to check the weather in",
        
        # Temperature I want/I'd like variations
        "i want to know the temperature in", "i'd like to know the temperature in",
        "i want to see the temperature in", "i'd like to see the temperature in",
        "i want to check the temperature in", "i'd like to check the temperature in",
        
        # I want/I'd like variations without "the"
        "i want to know weather in", "i'd like to know weather in",
        "i want to see weather in", "i'd like to see weather in",
        "i want to check weather in", "i'd like to check weather in",
        
        # Simple forms
        "weather", "temperature", "temp", "forecast", "conditions",
        
        # Common typos/variations
        "wheather in", "wether in", "weather n",
        "weather @", "weather @in", "weather @for",
        
        # Voice input variations
        "what is it like in", "how is it in",
        "what's it like in", "how's it in",
        
        # Additional variations
        "climate in", "climate of", "climate for",
        "conditions in", "conditions at", "conditions for",
        
        # Temperature specific typos/variations
        "whats the temp in", "hows the temp in",
        "temp of", "temperature of",
        "degrees in", "how many degrees in"
    ]
    
    # Sort prefixes by length (longest first) to ensure we remove the most specific matches first
    prefixes_to_remove.sort(key=len, reverse=True)
    
    # Remove prefixes
    original_input = input_lower
    for prefix in prefixes_to_remove:
        if input_lower.startswith(prefix):
            input_lower = input_lower[len(prefix):].strip()
            print(f"Removed prefix '{prefix}', new input: '{input_lower}'")
            break
    
    # Now clean the remaining location name
    input_text = clean_location_name(input_lower)
    print(f"Final cleaned input: '{input_text}'")
    
    # First check if the cleaned input exactly matches a country
    country_code = get_country_code(input_text)
    if country_code:
        print(f"Found country code '{country_code}' for cleaned input '{input_text}'")
        return None, input_text
    
    # Handle comma-separated locations with flexible spacing
    if ',' in input_text:
        # Split and clean each part, handling multiple spaces and empty parts
        parts = [part.strip() for part in input_text.split(',')]
        # Filter out empty parts
        parts = [part for part in parts if part]
        if len(parts) >= 2:
            # If first part starts with 'the', remove it for city
            city = parts[0]
            if city.startswith('the '):
                city = city[4:].strip()
            # Join remaining parts for potential multi-word country names
            country = ','.join(parts[1:]).strip()
            return city, country
        elif len(parts) == 1:
            # If single part starts with 'the', remove it
            part = parts[0]
            if part.startswith('the '):
                part = part[4:].strip()
            return part, None
    
    # Handle "in" keyword
    if ' in ' in input_text:
        parts = input_text.split(' in ')
        if len(parts) == 2:
            city = parts[0].strip()
            country = parts[1].strip()
            # If city part starts with 'the', remove it
            if city.startswith('the '):
                city = city[4:].strip()
            # If the first part is empty after removing prefixes, treat it as a country-only query
            if not city:
                # Check for multi-word country
                country_code = get_country_code(country)
                if country_code:
                    print(f"Found country code '{country_code}' for 'in' split country '{country}'")
                    return None, country
            return city, country
    
    # Try to match the entire input as a multi-word country
    words = input_text.split()
    for i in range(len(words), 0, -1):
        potential_country = ' '.join(words[:i])
        country_code = get_country_code(potential_country)
        if country_code:
            print(f"Found multi-word country: '{potential_country}' with code '{country_code}'")
            return None, potential_country
    
    # Handle special cases and common abbreviations
    special_cases = {
        'nyc': 'New York,US',
        'la': 'Los Angeles,US',
        'sf': 'San Francisco,US',
        'dc': 'Washington,US',
        'tokyo': 'Tokyo,JP',
        'paris': 'Paris,FR',
        'london': 'London,GB',
        'hk': 'Hong Kong,HK',
        'mel': 'Melbourne,AU',
        'syd': 'Sydney,AU',
        'tor': 'Toronto,CA',
        'van': 'Vancouver,CA',
        'kl': 'Kuala Lumpur,MY',
        'sg': 'Singapore,SG',
        'bkk': 'Bangkok,TH',
        'jkt': 'Jakarta,ID',
        'mnl': 'Manila,PH',
        'dxb': 'Dubai,AE',
        'cdg': 'Paris,FR',
        'fra': 'Frankfurt,DE',
        'ams': 'Amsterdam,NL',
        'bcn': 'Barcelona,ES',
        'ist': 'Istanbul,TR',
        'mxp': 'Milan,IT',
        'mad': 'Madrid,ES',
        'cph': 'Copenhagen,DK',
        'arn': 'Stockholm,SE',
        'vie': 'Vienna,AT',
        'zrh': 'Zurich,CH',
        'tlv': 'Tel Aviv,IL',
        'mow': 'Moscow,RU',
        'led': 'Saint Petersburg,RU',
        
        # Costa Rica cities - ensuring all variations are covered
        'cartago': 'Cartago,CR',
        'cartago costa rica': 'Cartago,CR',
        'san jose': 'San José,CR',
        'san josé': 'San José,CR',
        'san jose costa rica': 'San José,CR',
        'san josé costa rica': 'San José,CR',
        'alajuela': 'Alajuela,CR',
        'alajuela costa rica': 'Alajuela,CR',
        'heredia': 'Heredia,CR',
        'heredia costa rica': 'Heredia,CR',
        'liberia': 'Liberia,CR',
        'liberia costa rica': 'Liberia,CR',
        'puntarenas': 'Puntarenas,CR',
        'puntarenas costa rica': 'Puntarenas,CR',
        'limon': 'Limón,CR',
        'limón': 'Limón,CR',
        'limon costa rica': 'Limón,CR',
        'limón costa rica': 'Limón,CR'
    }
    
    if input_text in special_cases:
        return parse_location(special_cases[input_text])
    
    # If no country is found, return the whole input as city
    # If input starts with 'the', remove it for city name
    if input_text.startswith('the '):
        input_text = input_text[4:].strip()
    print(f"No country found, treating '{input_text}' as city")
    return input_text, None

def get_weather_description(temp, feels_like, humidity, condition, wind_speed=None):
    """Generate a smart weather description"""
    description = []
    
    # Temperature assessment
    if temp > 35:
        description.append("It's extremely hot")
    elif temp > 30:
        description.append("It's very hot")
    elif temp > 25:
        description.append("It's quite warm")
    elif temp > 20:
        description.append("It's pleasantly warm")
    elif temp > 15:
        description.append("It's mild")
    elif temp > 10:
        description.append("It's cool")
    elif temp > 0:
        description.append("It's cold")
    elif temp > -10:
        description.append("It's very cold")
    else:
        description.append("It's extremely cold")

    # Temperature difference assessment
    temp_diff = feels_like - temp
    if abs(temp_diff) > 5:
        if temp_diff > 0:
            description.append(f"but feels much warmer at {feels_like}°C")
        else:
            description.append(f"but feels much colder at {feels_like}°C")
    
    # Humidity assessment
    if humidity > 80:
        description.append("and very humid")
    elif humidity < 30:
        description.append("and very dry")
    
    # Wind assessment
    if wind_speed:
        if wind_speed > 20:
            description.append("with strong winds")
        elif wind_speed > 10:
            description.append("with moderate winds")
    
    return " ".join(description)

def handle_invalid_city(input_text):
    """Handle invalid city inputs more intelligently"""
    
    # Check if input is gibberish
    if is_gibberish(input_text):
        suggestions = suggest_cities()
        cities_list = ", ".join(f"{city[0]}" for city in suggestions[:3])
        return (
            "That doesn't look like a valid city name. "
            f"Try checking the weather in real cities like {cities_list}. "
            "Or you can ask me about any major city in the world!"
        )
    
    # Check if input is too short
    if len(input_text) < 2:
        return (
            "Please enter a complete city name. "
            "For example: 'Tokyo', 'New York', or 'Paris'"
        )
    
    # Check if input might be a country
    common_countries = ['usa', 'uk', 'japan', 'china', 'india', 'france', 'germany', 'italy', 'spain', 'canada']
    if input_text.lower() in common_countries:
        country = input_text.upper()
        cities = get_major_cities(input_text.lower())
        if cities:
            city_examples = ", ".join(city[0] for city in cities[:3])
            return (
                f"'{input_text}' is a country. Please specify a city instead.\n"
                f"Popular cities in {country} include: {city_examples}\n"
                "Which city would you like to know about?"
            )
    
    return None  # Return None if no special handling needed

def handle_fallback_intent(input_text):
    """Handle unknown inputs with more helpful responses"""
    if not input_text:
        return "I'm your weather assistant. How can I help you today? Try asking about the weather in any city!"
        
    input_lower = input_text.lower().strip()
    
    # Rant and frustration phrases
    rant_phrases = {
        # Negative feedback
        'this is stupid': "I understand your frustration. Let me help you get the weather information you need. Just tell me which city you're interested in.",
        'this is useless': "I want to help you get the weather information you need. Could you tell me which city you'd like to know about?",
        'you are stupid': "I'm here to help you check the weather. Let's start fresh - which city would you like to know about?",
        'you dont understand': "I apologize if I misunderstood. Let me try again - which city's weather would you like to know?",
        'you don\'t understand': "I apologize if I misunderstood. Let me try again - which city's weather would you like to know?",
        
        # Expressions of frustration
        'ugh': "Let's try again. Just tell me which city you'd like to check the weather for.",
        'argh': "I understand this might be frustrating. Let me help you - which city's weather would you like to know?",
        'this is not working': "I'm sorry you're having trouble. Let's try a simple weather check - just tell me which city.",
        'this doesnt work': "Let's make this work together. Simply tell me which city you'd like to check the weather for.",
        'this doesn\'t work': "Let's make this work together. Simply tell me which city you'd like to check the weather for.",
        
        # Confusion expressions
        'what': "I might not have been clear. I'm a weather bot - I can tell you the weather for any city. Which city interests you?",
        'i dont get it': "Let me explain simply: I can check the weather for any city. Just tell me which city you want to know about.",
        'i don\'t get it': "Let me explain simply: I can check the weather for any city. Just tell me which city you want to know about.",
        'im confused': "No problem, let me clarify: I'm here to check the weather for you. Just name any city!",
        'i\'m confused': "No problem, let me clarify: I'm here to check the weather for you. Just name any city!",
        
        # General complaints
        'bad bot': "I'm trying my best to help. Let me prove it - just tell me which city's weather you'd like to know.",
        'useless bot': "I can be quite helpful with weather information. Give me a chance - which city interests you?",
        'not helpful': "I want to be helpful. Let me show you - just tell me which city's weather you'd like to check.",
        
        # Profanity/Strong Language (keeping it clean)
        'stupid': "I understand you might be frustrated. Let's start fresh - which city's weather would you like to know?",
        'dumb': "I want to help you. Let's try again - just tell me which city you're interested in.",
        'terrible': "I'm sorry you're not satisfied. Let me try to help - which city's weather would you like to know?"
    }
    
    # Check for rant phrases with flexible matching
    for phrase, response in rant_phrases.items():
        if phrase in input_lower:
            return response
    
    # Thank you variations
    thank_you_phrases = ['thank you', 'thanks', 'thx', 'thank u', 'thankyou', 'tysm', 'ty']
    if any(phrase == input_lower for phrase in thank_you_phrases):
        return "You're welcome! Let me know if you need any more weather updates."
    
    # Goodbye variations
    goodbye_phrases = ['bye', 'goodbye', 'bye bye', 'see you', 'cya', 'good night', 'goodnight']
    if any(phrase == input_lower for phrase in goodbye_phrases):
        return "Goodbye! Feel free to ask about the weather anytime!"
    
    # Common greetings
    greetings = {
        'hi': "Hi there! I can help you check the weather anywhere in the world. Try asking 'What's the weather in Tokyo?' or 'Weather in Paris'!",
        'hello': "Hello! I'm your weather assistant. Ask me about the weather in any city!",
        'hey': "Hey! Need a weather update? Just name any city!",
        'good morning': "Good morning! Would you like to check today's weather? Just tell me which city!",
        'good afternoon': "Good afternoon! Ready to check the weather for you - which city would you like to know about?",
        'good evening': "Good evening! I can help you check the weather in any city. Where would you like to know about?"
    }
    
    for greeting, response in greetings.items():
        if input_lower.startswith(greeting):
            return response
    
    # How are you variations
    how_are_you = ['how are you', 'how r u', 'how you doing', "what's up", 'whats up', 'sup']
    if any(phrase in input_lower for phrase in how_are_you):
        return "I'm doing well, thanks for asking! I'm ready to help you check the weather. Which city would you like to know about?"
    
    # Identity/help questions
    identity_questions = [
        'who are you', 'what are you', 'what can you do', 'help', 'can you help',
        'what do you do', 'your name', 'who created you', 'what is your purpose'
    ]
    if any(q in input_lower for q in identity_questions):
        return (
            "I'm your friendly weather bot! I can help you check the weather anywhere in the world. "
            "Here's what I can do:\n"
            "1. Get current weather for any city\n"
            "2. Show temperature, humidity, and conditions\n"
            "3. Suggest major cities in countries\n\n"
            "Try asking: 'What's the weather in London?' or 'Weather in Tokyo, Japan'"
        )
    
    # Weather-related but incomplete queries
    weather_related = ['weather', 'temperature', 'forecast', 'rain', 'snow', 'sunny', 'cloudy', 'hot', 'cold']
    if any(w in input_lower for w in weather_related):
        suggestions = suggest_cities()
        cities_list = ", ".join(f"{city[0]}" for city in suggestions[:3])
        return (
            "I can check the weather for you, but I need to know which city. "
            f"Try asking about cities like {cities_list}, or any other city in the world!"
        )
    
    # Handle gibberish or invalid input
    if is_gibberish(input_text):
        return (
            "I didn't quite catch that. I'm a weather bot - I can tell you the weather "
            "for any city in the world. Try asking something like:\n"
            "- 'Weather in Paris'\n"
            "- 'How's the weather in Tokyo?'\n"
            "- 'What's the temperature in New York?'"
        )
    
    # Default response for other unknown inputs
    return (
        "I'm your weather assistant, so I can help you check the weather in any city. "
        "Try asking me things like:\n"
        "- 'Weather in Paris'\n"
        "- 'How's the weather in Tokyo?'\n"
        "- 'What's the temperature in New York?'\n"
        "Which city would you like to know about?"
    )

def handle_weather_intent(slots, original_input, api_key):
    """Handle the GetWeather intent"""
    try:
        # Debug logging
        print(f"Original input: {original_input}")
        print(f"Slots received: {slots}")
        
        # Clean input text
        if original_input:
            original_input = original_input.strip()
            # Remove common prefixes - aligned with Lex utterance patterns
            prefixes = [
                # Temperature patterns
                "what's the temperature in", "what is the temperature in",
                "how's the temperature in", "how is the temperature in",
                "what's the temp in", "what is the temp in",
                "how's the temp in", "how is the temp in",
                "temperature in", "temperature at", "temperature of",
                "temp in", "temp at", "temp of",
                "current temperature in", "current temp in",
                "degrees in", "how many degrees in",
                
                # Weather patterns
                "what's the weather in", "what is the weather in",
                "how's the weather in", "how is the weather in",
                "what's the weather like in", "what is the weather like in",
                "how's the weather like in", "how is the weather like in",
                "weather in", "weather for", "weather at",
                
                # Show/Tell patterns
                "show me the weather in", "tell me the weather in",
                "show me the temperature in", "tell me the temperature in",
                
                # Simple patterns
                "weather", "temperature", "temp"
            ]
            
            # Convert input to lowercase for matching
            input_lower = original_input.lower()
            
            # Sort prefixes by length (longest first) to ensure we remove the most specific matches first
            prefixes.sort(key=len, reverse=True)
            
            # Clean the input by removing prefixes
            for prefix in prefixes:
                if input_lower.startswith(prefix):
                    original_input = original_input[len(prefix):].strip()
                    print(f"Removed prefix '{prefix}', new input: '{original_input}'")
                    break
        
        print(f"Cleaned input: {original_input}")
        
        # Extract from slots if present
        city_input = None
        country_input = None
        
        if slots.get('City') and slots['City'].get('value', {}).get('interpretedValue'):
            city_input = slots['City']['value']['interpretedValue']
            
        if slots.get('Country') and slots['Country'].get('value', {}).get('interpretedValue'):
            country_input = slots['Country']['value']['interpretedValue']
            print(f"Found country context: {country_input}")
        
        # If we have slots, use them directly
        if city_input or country_input:
            # If we have only country input, suggest cities
            if country_input and not city_input:
                country_code = get_country_code(country_input)
                if country_code:
                    cities = get_major_cities(country_code)
                    if cities:
                        city_list = ", ".join([f"{city[0]} ({city[1]})" for city in cities[:5]])
                        return {
                            "sessionState": {
                                "dialogAction": {
                                    "type": "ElicitSlot",
                                    "slotToElicit": "City"
                                },
                                "intent": {
                                    "name": "GetWeather",
                                    "slots": {
                                        'Country': slots['Country'],  # Preserve country context
                                        'City': None  # Clear city slot to get new input
                                    },
                                    "state": "InProgress"
                                }
                            },
                            "messages": [{
                                "contentType": "PlainText",
                                "content": f"Which city in {get_display_country_name(country_input)} would you like to know about? Popular cities include: {city_list}"
                            }]
                        }
            # If we have both city and country, make the API call
            elif city_input and country_input:
                country_code = get_country_code(country_input)
                if country_code:
                    location = f"{city_input},{country_code}"
                    print(f"Making API call with city and country: {location}")
                    return make_api_call(location, api_key, slots)
        
        # If no slots or slot parsing failed, parse from original input
        if original_input:
            input_text = original_input.strip()
            
            # Check if we have a previous country context
            if slots.get('Country') and slots['Country'].get('value', {}).get('interpretedValue'):
                country_input = slots['Country']['value']['interpretedValue']
                print(f"Processing city input with country context: {input_text}")
                # Return a delegate response to let Lex handle the city slot
                return {
                    "sessionState": {
                        "dialogAction": {
                            "type": "Delegate"
                        },
                        "intent": {
                            "name": "GetWeather",
                            "slots": {
                                'Country': slots['Country'],  # Preserve country context
                                'City': {
                                    'value': {
                                        'originalValue': input_text,
                                        'interpretedValue': input_text
                                    }
                                }
                            }
                        }
                    }
                }
            
            # Check if input contains comma (city-country format)
            if ',' in input_text:
                parts = [part.strip() for part in input_text.split(',')]
                if len(parts) == 2:
                    city, country = parts
                    country_code = get_country_code(country)
                    if country_code:
                        location = f"{city},{country_code}"
                        print(f"Parsed city-country format: {location}")
                        return make_api_call(location, api_key, slots)
            
            # No comma, check if input is a country
            country_code = get_country_code(input_text)
            if country_code:
                # It's a country, suggest cities
                cities = get_major_cities(country_code)
                if cities:
                    city_list = ", ".join([f"{city[0]} ({city[1]})" for city in cities[:5]])
                    return {
                        "sessionState": {
                            "dialogAction": {
                                "type": "ElicitSlot",
                                "slotToElicit": "City"
                            },
                            "intent": {
                                "name": "GetWeather",
                                "slots": {
                                    'Country': {
                                        'value': {
                                            'originalValue': input_text,
                                            'interpretedValue': input_text,
                                            'resolvedValues': [input_text]
                                        }
                                    },
                                    'City': None
                                },
                                "state": "InProgress"
                            }
                        },
                        "messages": [{
                            "contentType": "PlainText",
                            "content": f"Which city in {get_display_country_name(input_text)} would you like to know about? Popular cities include: {city_list}"
                        }]
                    }
            
            # Not a country, must be a city
            print(f"Treating input as city: {input_text}")
            return make_api_call(input_text, api_key, slots)
        
        # If we get here, we couldn't parse the input
        suggestions = suggest_cities()
        cities_list = ", ".join(f"{city[0]} ({city[1]})" for city in suggestions[:3])
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": "GetWeather",
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [{
                "contentType": "PlainText",
                "content": f"I need a city name to check the weather. Try asking about {cities_list}, or any other major city!"
            }]
        }

    except Exception as e:
        print(f"Error in handle_weather_intent: {str(e)}")
        suggestions = suggest_cities()
        cities_list = ", ".join(f"{city[0]} ({city[1]})" for city in suggestions[:3])
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": "GetWeather",
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [{
                "contentType": "PlainText",
                "content": f"I'm having trouble getting that weather information. Try popular cities like {cities_list}, or try adding the country name for better accuracy."
            }]
        }

def make_api_call(location, api_key, slots):
    """Make the weather API call and format response"""
    # Handle city,country format properly
    if ',' in location:
        city, country = location.split(',')
        # Clean city and country separately
        city = clean_location_name(city)
        country = clean_location_name(country)
        location = f"{city},{country}"
    else:
        # Clean single location name
        location = clean_location_name(location)
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    print(f"Making API call to: {url}")
    
    response = requests.get(url)
    print(f"API response status: {response.status_code}")
    print(f"API response content: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"API response data: {data}")
        temp = data['main']['temp']
        condition = data['weather'][0]['description']
        feels_like = data['main'].get('feels_like', temp)
        humidity = data['main'].get('humidity', 0)
        wind_speed = data['wind'].get('speed', 0)
        actual_city = data['name']
        actual_country = data['sys']['country']
        
        # Get local time
        sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.fromtimestamp(data['sys']['sunset'])
        current_time = datetime.now()
        time_of_day = "night" if current_time.hour < sunrise.hour or current_time.hour > sunset.hour else "day"
        
        # Build smart weather description
        weather_desc = get_weather_description(temp, feels_like, humidity, condition, wind_speed)
        
        message = (
            f"Weather report for {actual_city}, {actual_country}:\n"
            f"{weather_desc}. "
            f"Current temperature is {temp}°C with {condition}. "
            f"Humidity is {humidity}%. "
            f"Wind speed is {wind_speed} m/s."
        )
        
        # Add time-specific details
        if time_of_day == "night":
            message += f"\nSunrise will be at {sunrise.strftime('%H:%M')}."
        else:
            message += f"\nSunset will be at {sunset.strftime('%H:%M')}."
        
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": "GetWeather",
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [{"contentType": "PlainText", "content": message}]
        }
    
    # Handle API errors with more specific messages
    if response.status_code == 404:
        # Get country name if available
        country_name = None
        if slots.get('Country') and slots['Country'].get('value', {}).get('interpretedValue'):
            country_name = get_display_country_name(slots['Country']['value']['interpretedValue'])
        
        # Get city name if available
        city_name = None
        if slots.get('City') and slots['City'].get('value', {}).get('interpretedValue'):
            city_name = slots['City']['value']['interpretedValue']
        
        if country_name and city_name:
            message = f"I'm sorry, but I couldn't find weather information for {city_name} in {country_name}. This city might not be supported by our weather service. Try asking about a major city instead."
        elif city_name:
            message = f"I'm sorry, but I couldn't find weather information for {city_name}. This city might not be supported by our weather service. Try asking about a major city instead."
        else:
            message = "I'm sorry, but I couldn't find weather information for that location. Try asking about a major city instead."
        
        # Get some suggestions
        suggestions = suggest_cities()
        cities_list = ", ".join(f"{city[0]}" for city in suggestions[:3])
        message += f"\nPopular cities you can try: {cities_list}"
    else:
        message = "I'm having trouble getting the weather information right now. Please try again with a different city."
    
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                "name": "GetWeather",
                "slots": slots,
                "state": "Fulfilled"
            }
        },
        "messages": [{
            "contentType": "PlainText",
            "content": message
        }]
    }

def lambda_handler(event, context):
    try:
        # Get intent name safely with a default value
        intent_name = event.get('sessionState', {}).get('intent', {}).get('name', 'FallbackIntent')
        original_input = event.get('inputTranscript', '').strip()

        # Handle FallbackIntent
        if intent_name == 'FallbackIntent':
            message = handle_fallback_intent(original_input)
            return {
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {"name": "FallbackIntent", "state": "Fulfilled"}
                },
                "messages": [{"contentType": "PlainText", "content": message}]
            }

        # Handle GetWeather intent
        if intent_name == 'GetWeather':
            slots = event.get('sessionState', {}).get('intent', {}).get('slots', {})
            api_key = os.environ.get('OPENWEATHER_API_KEY')
            if not api_key:
                raise Exception("OpenWeather API key not configured")
            return handle_weather_intent(slots, original_input, api_key)

        # Handle unknown intents
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": intent_name, "state": "Fulfilled"}
            },
            "messages": [{
                "contentType": "PlainText",
                "content": "I'm not sure how to handle that request. I'm best at checking weather for cities!"
            }]
        }

    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": "FallbackIntent", "state": "Fulfilled"}
            },
            "messages": [{
                "contentType": "PlainText",
                "content": "I'm having trouble understanding that. Try asking about the weather in a city!"
            }]
        }