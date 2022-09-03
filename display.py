import json
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
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

  # print(changeinvariables)

  chart = alt.Chart(changeinvariables, title='Change in Open Interest vs Strike Price').mark_bar(
    opacity=1,
    ).encode(
    column = alt.Column('StrikePrice:O', spacing = 5, header = alt.Header(labelOrient = "bottom")),
    x=alt.X('variable', sort = ["CE", "PE"], axis = None),
    y=alt.Y('value:Q'),
    color= alt.Color('variable'),
  ).configure_view(stroke='transparent')

  # alt.data_transformers.disable_max_rows()

  # np.random.seed(0)
  # data = pd.DataFrame({
  #     'date': pd.date_range('1990-01-01', freq='Y', periods=10),
  #     'FAO_yied': np.random.randn(10).cumsum(),
  #     'Simulation': np.random.randn(10).cumsum(),
  #     'Predicted': np.random.randn(10).cumsum(),
  # })

  # print(pd.date_range('1990-01-01', freq='Y', periods=10))

  # prediction_table = pd.melt(data, id_vars=['date'], value_vars=['FAO_yied', 'Predicted', 'Simulation'])
  # print(prediction_table)

  # chart = alt.Chart(prediction_table, title='Simulated (attainable) and predicted yield ').mark_bar(
  #   opacity=1,
  #   ).encode(
  #   column = alt.Column('date:O', spacing = 5, header = alt.Header(labelOrient = "bottom")),
  #   x =alt.X('variable', sort = ["Actual_FAO", "Predicted", "Simulated"],  axis=None),
  #   y =alt.Y('value:Q'),
  #   color= alt.Color('variable')
  # ).configure_view(stroke='transparent')
  
  st.altair_chart(chart)
  
  # b = (
  #   Bar()
  #   .add_xaxis(columnsStrike)
  #   .add_yaxis(
  #       "Red Bar shows StrikPrice",rowsStrike
  #   )
  #   .set_global_opts(
  #       title_opts=opts.TitleOpts(
  #           title="StrikePrice vs Change in Open Interest", subtitle=f"Underlying Value = {midvalue}"
  #       ),
  #       toolbox_opts=opts.ToolboxOpts(),
  #   )
  # )
  # st_pyecharts(b, height=700)


sys.modules[__name__] = display