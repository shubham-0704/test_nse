import streamlit as st
import math
import requests
import json
import time
import datetime as dt

#importnant urls
url_oc      = "https://www.nseindia.com/option-chain"
url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"


# functions for calculating at the money strike
def round_nearest(x,num=10): return int(math.floor(float(x+num/2)/num)*num)
def atm_bnf(x): return round_nearest(x,100)
def atm_nf(x): return round_nearest(x,50)

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


dic_nf ={"time":[], "PE":{},"CE":{},"exp_date":None,"start_price":None,"current_price":None,"first_run":True,"update_time":None}
dic_bnf ={"time":[], "PE":{},"CE":{},"exp_date":None,"start_price":None,"current_price":None,"first_run":True,"update_time":None}

first_run =True

def get_oi(url):
    global stike_p

    global start_strike
    global end_strike
    response_text = get_data(url)
    data = json.loads(response_text)

    dic_nf["current_price"]

    price =data["records"]["underlyingValue"]
    atm = atm_nf(price)
    atm_index = int((atm-data["filtered"]["data"][0]["strikePrice"])/50)

    atm_oi_change=data["filtered"]["data"][atm_index]["PE"]["changeinOpenInterest"]
    global first_run
    if first_run==True:
        currExpiryDate = data["records"]["expiryDates"][0]
        dic_nf["exp_date"]=currExpiryDate
        global strike_p
        strike_p=atm
        start_strike = data["filtered"]["data"][atm_index-29]["strikePrice"]
        end_strike=data["filtered"]["data"][atm_index+29]["strikePrice"]
        first_run=False
        for i in range(start_strike,end_strike+50,50):
          dic_nf["CE"][i]=[]
          dic_nf["PE"][i]=[]

    
    
    indx = int((strike_p - data["filtered"]["data"][0]["strikePrice"])/50)
    oi = data["filtered"]["data"][indx]["PE"]["changeinOpenInterest"]
    print(Oi_change,oi,indx)
    if  Oi_change!=oi:
        now = dt.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        dic_nf["time"].append(current_time)
        strike_p=atm
        start = int((start_strike - data["filtered"]["data"][0]["strikePrice"])/50)
        for i in range(start,start+59):
          sp=data["filtered"]["data"][i]["strikePrice"]
          dic_nf["PE"][sp].append(data["filtered"]["data"][i]["PE"]["openInterest"])
          dic_nf["CE"][sp].append(data["filtered"]["data"][i]["CE"]["openInterest"])

    time.sleep(2)

    return atm_oi_change





## page setup (webpage)

st.set_page_config(
    page_title = 'OI DATA',
    page_icon = '📊',
    layout = 'wide'
)

#headers
c1,c2,c3,c4=st.columns([2,1,1,1])
c1.title("📊 OI Data Tracker")
c2_placeholder = c2.empty()
c3_placeholder=c3.empty()
c4_placeholder=c4.empty()

def update_header():
    c2_placeholder.metric("Nifty",f'{dic_nf["current_price"]}',23)
    c3_placeholder.metric("Bank Nifty",f'{dic_bnf["current_price"]}',-234)
    c4_placeholder.text(f'''Last Update : {dic_nf["update_time"]}\nExpiry : {dic_nf["exp_date"]}''')


if __name__=="__main__":
    # Oi_change=get_oi(url_nf)
    update_header()