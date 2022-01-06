import streamlit as st #web app 
import pandas as pd # data manipulation
import numpy as np # random gen
import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from pprint import pprint

st.title("SMOLVERSE - Dashboard")

st.subheader("NFT Floors 🚀 📈")

#st.markdown("### Key Metrics")

def getTickerPrice(ticker):
    url =f'https://api.covalenthq.com/v1/pricing/tickers/?quote-currency=USD&format=JSON&tickers={ticker}&key=ckey_78290656a6ca426fa748bdcd41b'
    response = requests.get(url)
    data = response.json()
    return(data['data']['items'][0]['quote_rate'])
def buildFloorQuery():
    query = gql(
        f"""
        {{
        collections {{
            id
            address
            name
            totalListings
            floorPrice
        }}
        }}
        """
        )
    return query

def getFloorPrice(collection):
    transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/wyze/treasure-marketplace")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    result = client.execute(buildFloorQuery())
    smolbrains = [obj for obj in result['collections'] if(obj['name'] == collection)]
    floor = int(smolbrains[0]['floorPrice'])/1000000000000000000
    #print(f"floor is {floor}")
    return floor
def getMagicPriceGraph(ticker):
    query = gql(
        f"""
        {{
        pairs(where:{{name:"{ticker}-USDT"}}){{
            name
            token1Price
            }}
        }}
        """
        )
    transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/sushiswap/arbitrum-exchange")
    client = Client(transport=transport, fetch_schema_from_transport=False)
    result = client.execute(query)
    return(round(float(result["pairs"][1]["token1Price"]),2))


kpi1, kpi2, kpi3,kpi4 = st.columns(4)

my_dynamic_value = 333.3335 

new_val = 222

final_val = my_dynamic_value / new_val


kpi1.metric(label = "Smol Brains",
            value = "$%.2f" %(getFloorPrice("Smol Brains")*getMagicPriceGraph("MAGIC")),
            )
kpi2.metric(label = "Smol Bodies",
            value = "$%.2f" %(getFloorPrice("Smol Bodies")*getMagicPriceGraph("MAGIC")))

kpi3.metric(label = "Smol Land",
            value = "$%.2f" %(getFloorPrice("Smol Brains Land")*getMagicPriceGraph("MAGIC")))
kpi4.metric(label = "Smol Cars",
            value = "$%.2f" %(getFloorPrice("Smol Cars")*getMagicPriceGraph("MAGIC")))

st.markdown("### Important Charts 📈")

chart1, chart2 = st.columns(2)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

chart1.bar_chart(chart_data)
chart2.line_chart(chart_data)

st.dataframe(chart_data)
