import json
import numpy as np

import streamlit as st
import altair as alt
import pandas as pd
import sys
import json

def display(response):
  
  data=json.loads(response)
  print("Hello")
  columnsStrike = []
  rowsStrike=[]
  changePE = []
  midvalue=data['records']['underlyingValue']

  for strikeprice in data['filtered']['data']:
    if(midvalue < strikeprice['strikePrice'] + 50*8):
      columnsStrike.append(strikeprice['strikePrice'])
      rowsStrike.append(50*strikeprice['CE']['changeinOpenInterest'])
      changePE.append(50*strikeprice['PE']['changeinOpenInterest'])
    if(midvalue < strikeprice['strikePrice']-50*7 ):
      break

  alt.data_transformers.disable_max_rows()

  chart_data = pd.DataFrame({'StrikePrice' : columnsStrike,
                              'CE' : rowsStrike,
                              'PE': changePE})
  
  changeinvariables = pd.melt(chart_data, id_vars=['StrikePrice'], value_vars=['CE', 'PE'])



  chart = alt.Chart(changeinvariables, title='Change in Open Interest vs Strike Price').mark_bar(
    opacity=1,
    ).encode(
    column = alt.Column('StrikePrice:O', spacing = 5, header = alt.Header(labelOrient = "bottom")),
    x=alt.X('variable', sort = ["CE", "PE"], axis = None),
    y=alt.Y('value:Q'),
    color= alt.Color('variable'),
  ).configure_view(stroke='transparent')

 
  
  st.altair_chart(chart)
  


sys.modules[__name__] = display