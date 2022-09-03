# Libraries
import requests
import json
import math
import  datetime as dt
import time
import display


# Method to get nearest strikes
# Method to get nearest strikes
def round_nearest(x,num=10): return int(math.floor(float(x+num/2)/num)*num)
def atm_bnf(x): return round_nearest(x,100)
def atm_nf(x): return round_nearest(x,50)

# Urls for fetching Data
url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

# Headers
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}

sess = requests.Session()
cookies = dict()

# Local methods
def set_cookie():
    request = sess.get(url_oc, headers=headers, timeout=1000)
    cookies = dict(request.cookies)

def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, cookies=cookies)
    if(response.status_code==401):
        set_cookie()
        response = sess.get(url_nf, headers=headers, timeout=5, cookies=cookies)
    if(response.status_code==200):
        return response.text
    return ""


stike_p = None
Oi_change =None
start_strike=None
end_strike=None


dic ={"time":[], "PE":{},"CE":{},"exp_date":None}

first_run =True

def get_oi(url):
    global stike_p

    global start_strike
    global end_strike
    response_text = get_data(url)
    data = json.loads(response_text)

    price =data["records"]["underlyingValue"]
    atm = atm_nf(price)
    atm_index = int((atm-data["filtered"]["data"][0]["strikePrice"])/50)

    atm_oi_change=data["filtered"]["data"][atm_index]["PE"]["changeinOpenInterest"]
    global first_run
    if first_run==True:
        currExpiryDate = data["records"]["expiryDates"][0]
        dic["exp_date"]=currExpiryDate
        global strike_p
        strike_p=atm
        start_strike = data["filtered"]["data"][atm_index-29]["strikePrice"]
        end_strike=data["filtered"]["data"][atm_index+29]["strikePrice"]
        first_run=False
        for i in range(start_strike,end_strike+50,50):
          dic["CE"][i]=[]
          dic["PE"][i]=[]

    
    
    indx = int((strike_p - data["filtered"]["data"][0]["strikePrice"])/50)
    oi = data["filtered"]["data"][indx]["PE"]["changeinOpenInterest"]
    print(Oi_change,oi,indx)
    if  Oi_change!=oi:
        now = dt.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        dic["time"].append(current_time)
        strike_p=atm
        start = int((start_strike - data["filtered"]["data"][0]["strikePrice"])/50)
        for i in range(start,start+59):
          sp=data["filtered"]["data"][i]["strikePrice"]
          dic["PE"][sp].append(data["filtered"]["data"][i]["PE"]["openInterest"])
          dic["CE"][sp].append(data["filtered"]["data"][i]["CE"]["openInterest"])

    time.sleep(2)

    return atm_oi_change


# while(1):
#   Oi_change=get_oi(url_nf)



if __name__ =="__main__":
    display(get_data(url_nf))


