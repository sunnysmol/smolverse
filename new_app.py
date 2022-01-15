import streamlit as st #web app 
import pandas as pd # data manipulation
import numpy as np # random gen
import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from pprint import pprint
from streamlit_autorefresh import st_autorefresh

count = st_autorefresh(interval=3000000, key="fizzbuzzcounter")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("SMOLVERSE - Dashboard")

st.subheader("Free Mints 🚀 📈")

#st.markdown("### Key Metrics")
@st.cache
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
@st.cache
def getFloorPrice(collection):
    transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/wyze/treasure-marketplace")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    result = client.execute(buildFloorQuery())
    pprint(result)
    smolbrains = [obj for obj in result['collections'] if(obj['name'] == collection)]
    floor = int(smolbrains[0]['floorPrice'])/1000000000000000000
    #print(f"floor is {floor}")
    return floor
@st.cache
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
    client = Client(transport=transport, fetch_schema_from_transport=True)
    result = client.execute(query)
    pprint(result)
    return(round(float(result["pairs"][1]["token1Price"]),2))


def getFloor():
    totalFloor = st.columns(3)
    st.markdown("***")
    st.subheader("NFT Floor 🚀 📈")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi4 = st.columns(3)

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
    kpi4[1].metric(label = "Smol Cars",
            value = "$%.2f" %(getFloorPrice("Smol Cars")*getMagicPriceGraph("MAGIC")))

    smolbrains_value = int(getFloorPrice("Smol Brains")*getMagicPriceGraph("MAGIC"))*2
    smolboadies_value = int(getFloorPrice("Smol Bodies")*getMagicPriceGraph("MAGIC"))*2
    smolCars_value = int(getFloorPrice("Smol Cars")*getMagicPriceGraph("MAGIC"))*2
    smol_land = int(getFloorPrice("Smol Brains Land")*getMagicPriceGraph("MAGIC"))

    total = smol_land+smolCars_value+smolboadies_value+smolbrains_value

    totalFloor[2].metric(label = "Total Free Mint",
            value = "$%.2f" %int(total),
            )

    totalFloor[0].image('https://www.smolverse.lol/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FGrow.725fafa2.gif&w=256&q=75',width=70)
    st.markdown("***")

    st.write("follow on twitter [@smolmintfloor](https://twitter.com/smolmintfloor)")
getFloor()



# st.markdown("### Important Charts 📈")

# chart1, chart2 = st.columns(2stat

# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])

# chart1.bar_chart(chart_data)
# chart2.line_chart(chart_data)

    #st.dataframe(chart_data)

