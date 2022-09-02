import json
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import streamlit as st
import pandas as pd
import sys
import json

def display(response):
  
  data=json.loads(response)
  # print(data);
  columnsStrike = []
  rowsStrike=[]
  midvalue=data['records']['underlyingValue']
  for strikeprice in data['filtered']['data']:
    if(midvalue < strikeprice['strikePrice'] + 50*8):
      columnsStrike.append(strikeprice['strikePrice'])
    if(midvalue < strikeprice['strikePrice']-50*7 ):
      break
  chart_data = pd.Series(columnsStrike)
  b = (
    Bar()
    .add_xaxis(columnsStrike)
    .add_yaxis(
        "Red Bar shows StrikPrice",columnsStrike
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="StrikePrice vs Nothing", subtitle=f"Underlying Value = {midvalue}"
        ),
        toolbox_opts=opts.ToolboxOpts(),
    )
  )
  st_pyecharts(b)


sys.modules[__name__] = display