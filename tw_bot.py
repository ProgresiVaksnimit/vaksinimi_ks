import requests, re, configparser, tweepy, datetime
from bs4 import BeautifulSoup

# Population as of 2020 - ASK - Agjensisë së Statistikave të Kosovës (https://ask.rks-gov.net)
POPULATION = 1798188 

# Official Website of Ministry of Health - COVID-19 statistics
URL = 'https://msh.rks-gov.net/sq/statistikat-covid-19'

# Declare first and second dose global variables  
COVID_DASHBOARD_LINK, FIRST_DOSE, SECOND_DOSE = None, None, None

# Link to Twitter API config file
TWITTER_API_CONFIG_FILE = 'twitter.config'

# Switch it to False for production
DRY_RUN = True

# Get Twitter API configuration data
def getTwitterConfig():
    """
    Read Twitter API config file given on TWITTER_API_CONFIG_FILE global variable
    """
    config = configparser.ConfigParser()
    config.read(TWITTER_API_CONFIG_FILE)
    return config


# Authenticate Twitter based on given Twitter API configuration file
def authTwitter(config):
    """
    Auth to Twitter and return auth object
    """
    auth = tweepy.OAuthHandler(config.get('TWITTER', 'API_KEY'), config.get('TWITTER', 'API_SECRET_KEY'))
    auth.set_access_token(config.get('TWITTER', 'ACCESS_TOKEN'), config.get('TWITTER', 'ACCESS_TOKEN_SECRET'))
    return auth


# Find COVID statistics dashboard link from given URL
def findDashboardLink(url):
    """
    Get source page of given url and find covid dashboard link
    """
    global COVID_DASHBOARD_LINK
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        COVID_DASHBOARD_LINK = soup.find(src=re.compile("coviddashboard")).attrs['src']
    except requests.exceptions.RequestException as e:
        print(f'Error getting source page from URL: {url}.\nError: {e}')
        raise
    except Exception as e:
        print(f'Error parsing/finding dashboard link\nError: {e}')
        raise


# Find first and second dose from COVID statistics dashboard
def findFirstAndSecondDoseStats(dashboard_link):
    """
    Find first and second dose numbers by extracting them from COVID statistics dashboard
    """
    global FIRST_DOSE, SECOND_DOSE
    try:
        page = requests.get(dashboard_link)
        soup = BeautifulSoup(page.content, "html.parser")
        numbers = soup.find_all('div', class_="numbers")
        for number in numbers:
            if number.find(string=re.compile("dozën e parë")):
                FIRST_DOSE = int(number.find('h4').string)
                print(f'First dose: \n{FIRST_DOSE}')
            if number.find(string=re.compile("dy dozat")):
                SECOND_DOSE = int(number.find('h4').string)
                print(f'Second dose: \n{SECOND_DOSE}')
    except requests.exceptions.RequestException as e:
        print(f'Error getting source page from COVID statistics dashboard: {dashboard_link}.\nError: {e}')
        raise
    except Exception as e:
        print(f'Error parsing/finding first and second dose stats\nError: {e}')
        raise


# Will generate a progress bar based on percentage
def generateProgressBar(percentage):
	num_chars = 15
	num_filled = round(percentage * num_chars)
	num_empty = num_chars - num_filled
	display_percentage = str(round(percentage * 100, 1)).replace('.', ',')
	msg = '{}{} {}%'.format('▓' * num_filled, '░' * num_empty, display_percentage)
	return msg


# Generate Tweet message
def generateTweet():
    """
    Generate Tweet content including progress bar and text
    """
    f_dose = generateProgressBar(float((FIRST_DOSE + SECOND_DOSE) / POPULATION))
    s_dose = generateProgressBar(float(SECOND_DOSE / POPULATION))
    tweet_message = f'{f_dose} - të vaksinuar me dozën e parë\n{s_dose} - të vaksinuar me dy doza\nData: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
    return tweet_message


# Send Tweet with progress bar and percentage
def sendTweet(tweet, auth):
    """
    Authenticate Twitter API and send tweet
    """
    tw_api = tweepy.API(auth)
    if DRY_RUN:
        print(f'DRY RUN - ON\nTweet: \n{tweet}, by Twitter User: {tw_api.me().screen_name}')
        return
    try:
        print(f'Tweet: \n{tweet}')
        tw_api.update_status(tweet)
    except Exception as e:
        print(f'Error sending Tweet - {e}')

# The main function that calls all functions
def main():
    tw_conf = getTwitterConfig()
    tw_auth = authTwitter(tw_conf)
    findDashboardLink(URL)
    findFirstAndSecondDoseStats(COVID_DASHBOARD_LINK)
    tweet = generateTweet()
    sendTweet(tweet, tw_auth)

def lambda_handler(event, context):
    main()