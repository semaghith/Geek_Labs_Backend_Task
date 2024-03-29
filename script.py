from playwright.sync_api import sync_playwright
from datetime import datetime , timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def login():
        login_link = page.query_selector("a[href*=login]")
        login_link.click()
        
        page.get_by_role("textbox").fill(os.getenv("EMAIL"))
        page.get_by_role("button", name="Next").click()
        
        page.get_by_role("textbox",  name="Phone or username").fill(os.getenv("USERNAME"))
        page.get_by_role("button", name="Next").click()
        
        page.get_by_role("textbox").fill(os.getenv("PASS"))
        page.get_by_role("button", name="log in").click()

cnt = 0
result = []
setResult = set()
scrolling = True


#inputs
inputTicker = "$TSLA"
timeInput = 999999
twitterAccounts = [
   "https://twitter.com/Mr_Derivatives",
   "https://twitter.com/warrior_0719",
   "https://twitter.com/ChartingProdigy",
   "https://twitter.com/allstarcharts",
   "https://twitter.com/yuriymatso",
   "https://twitter.com/TriggerTrades",
   "https://twitter.com/AdamMancini4",
   "https://twitter.com/CordovaTrades",
   "https://twitter.com/Barchart",
   "https://twitter.com/RoyLMattox",
   ]

#Get inerval time based on input minutes
currentTime = datetime.now()
intervalTime = currentTime - timedelta(minutes=timeInput)

#selectors used
tweetSelector = '[data-testid="tweet"]'
hrefSelector = '[href$="/search?q=%24{}&src=cashtag_click"]'.format(inputTicker[1:])


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page(bypass_csp=True)

    #loop on 10 input accounts
    for twitterAccount in twitterAccounts:
 
        page.goto(twitterAccount)
        
        #login()
        
        while True:
            
            page.wait_for_load_state("networkidle")
            
            #get all tweets
            tweets = page.query_selector_all(tweetSelector) 
            
            for tweet in tweets:
                
                #get time of each tweet
                tweetTime = tweet.query_selector("time")
                timeValue = tweetTime.get_attribute("datetime")
                
                parsedTime = datetime.strptime(timeValue, '%Y-%m-%dT%H:%M:%S.000Z')
                
                #add tweet if the time is in range
                if parsedTime >= intervalTime:
                    result.append(tweet)
                    
                    #add tweets with the same tricker of the ticker input
                    setResult.add(tweet.query_selector(hrefSelector)) 
            
                else:
                    #set scrolling bool to stop scrolling for new tweets if time is out of range
                    scrolling = False
                    break
                
                
            if scrolling:                
                # Scroll to the last tweet in result
                result[-1].scroll_into_view_if_needed()

            else:
                break
            
    #calc numb of tricker found
    cnt = len(setResult)
        
    print(f'""{inputTicker}" was mentioned "{cnt}" in the last "{timeInput}" minutes."')
    
    browser.close()
