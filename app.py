import streamlit as st
st.set_page_config(layout="wide")
from streamlit.components.v1 import iframe
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import SessionState
from get_data import refresh_data
import numpy as np
import pandas as pd
import dominate
from dominate.tags import div, p, h1,h2, h4, ul, a, li, label
import altair as alt

session_state = SessionState.get(clicked=False)

def get_title(gen):
    titles = []
    for i in gen:
        if hasattr(i, 'title'):
            title = ' ' + i.title + ' '
            titles.append(title)
    return titles
            
@st.cache
def init():
    df = pd.read_csv('table_records.csv').sort_values(by='Total', ascending = False)
    tickers = ['All'] + df.Code.tolist()
    interval = 24
    # subs = [{'title': ' Buying otc in Canada ', 'title_extracted': [], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhr80/buying_otc_in_canada/'}, {'title': ' Maganese Corp MNXXF ', 'title_extracted': ['MNXXF'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhncj/maganese_corp_mnxxf/'}, {'title': ' UAMY Looking Good 🙌🏼 ', 'title_extracted': ['UAMY'], 'url': 'https://www.reddit.com/gallery/kxhkss'}, {'title': ' Asking for a DD &amp; Catalyst BEFORE the run... $VNUE is still .01 and is ready to pop (some DD included) ', 'title_extracted': ['VNUE', 'BEFOR'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhik0/asking_for_a_dd_catalyst_before_the_run_vnue_is/'}, {'title': ' Actual Due Diligence for TANH - (Not Moon Hype for once) Tantech Holdings Ltd ', 'title_extracted': ['TANH'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhh25/actual_due_diligence_for_tanh_not_moon_hype_for/'}, {'title': ' $PHUN Blockchain play ', 'title_extracted': ['PHUN'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhe3z/phun_blockchain_play/'}, {'title': ' Resort Savers (RSSV) starting to move... ', 'title_extracted': ['RSSV'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhde6/resort_savers_rssv_starting_to_move/'}, {'title': ' Anomalous Stocks, January 14, 2021 ', 'title_extracted': [], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh99k/anomalous_stocks_january_14_2021/'}, {'title': ' GGBXF doubling in price? Why? ', 'title_extracted': ['GGBXF'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh8yi/ggbxf_doubling_in_price_why/'}, {'title': ' WANT A STOCK WITH A SOLID TICKER NAME? Buy $EVUS 🚀🚀🚀🚀🚀 ', 'title_extracted': ['SOLID', 'WITH', 'TICKE', 'EVUS', 'STOCK', 'NAME', 'WANT'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh8tb/want_a_stock_with_a_solid_ticker_name_buy_evus/'}, {'title': ' $VGLS ready to TAKE OFF ', 'title_extracted': ['VGLS', 'OFF', 'TAKE'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh7ng/vgls_ready_to_take_off/'}, {'title': ' What is a good price target for BNGO? ', 'title_extracted': ['BNGO'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh57r/what_is_a_good_price_target_for_bngo/'}, {'title': ' $SENS IS MOON BOUND 🚀🚀🌕🌕 ', 'title_extracted': ['MOON', 'BOUND', 'SENS'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh4mj/sens_is_moon_bound/'}, {'title': ' ASTI &amp; OMEG to the moon?! 🚀🚀🚀 ', 'title_extracted': ['OMEG', 'ASTI'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxgxup/asti_omeg_to_the_moon/'}]
    subs = pd.read_json('submissions.json')
    return df, tickers, interval, subs

@st.cache
def pull_data(interval):
    df, subs = refresh_data(int(interval))
    tickers = ['All'] + df.sort_values(by='Total', ascending = False).Code.tolist()

    return df, tickers, pd.DataFrame(subs)

def get_reddit_list(data):
    # data = [{'title': ' Buying otc in Canada ', 'title_extracted': [], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhr80/buying_otc_in_canada/'}, {'title': ' Maganese Corp MNXXF ', 'title_extracted': ['MNXXF'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhncj/maganese_corp_mnxxf/'}, {'title': ' UAMY Looking Good 🙌🏼 ', 'title_extracted': ['UAMY'], 'url': 'https://www.reddit.com/gallery/kxhkss'}, {'title': ' Asking for a DD &amp; Catalyst BEFORE the run... $VNUE is still .01 and is ready to pop (some DD included) ', 'title_extracted': ['VNUE', 'BEFOR'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhik0/asking_for_a_dd_catalyst_before_the_run_vnue_is/'}, {'title': ' Actual Due Diligence for TANH - (Not Moon Hype for once) Tantech Holdings Ltd ', 'title_extracted': ['TANH'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhh25/actual_due_diligence_for_tanh_not_moon_hype_for/'}, {'title': ' $PHUN Blockchain play ', 'title_extracted': ['PHUN'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhe3z/phun_blockchain_play/'}, {'title': ' Resort Savers (RSSV) starting to move... ', 'title_extracted': ['RSSV'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhde6/resort_savers_rssv_starting_to_move/'}, {'title': ' Anomalous Stocks, January 14, 2021 ', 'title_extracted': [], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh99k/anomalous_stocks_january_14_2021/'}, {'title': ' GGBXF doubling in price? Why? ', 'title_extracted': ['GGBXF'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh8yi/ggbxf_doubling_in_price_why/'}, {'title': ' WANT A STOCK WITH A SOLID TICKER NAME? Buy $EVUS 🚀🚀🚀🚀🚀 ', 'title_extracted': ['SOLID', 'WITH', 'TICKE', 'EVUS', 'STOCK', 'NAME', 'WANT'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh8tb/want_a_stock_with_a_solid_ticker_name_buy_evus/'}, {'title': ' $VGLS ready to TAKE OFF ', 'title_extracted': ['VGLS', 'OFF', 'TAKE'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh7ng/vgls_ready_to_take_off/'}, {'title': ' What is a good price target for BNGO? ', 'title_extracted': ['BNGO'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh57r/what_is_a_good_price_target_for_bngo/'}, {'title': ' $SENS IS MOON BOUND 🚀🚀🌕🌕 ', 'title_extracted': ['MOON', 'BOUND', 'SENS'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh4mj/sens_is_moon_bound/'}, {'title': ' ASTI &amp; OMEG to the moon?! 🚀🚀🚀 ', 'title_extracted': ['OMEG', 'ASTI'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxgxup/asti_omeg_to_the_moon/'}]
    reddit_subs_list = div(id='reddit-submission', style = 'max_height: 500px').add(div(style = 'overflow:hidden;')).add(ul(style = 'overflow-y:scroll; height: 500px;'))
    with reddit_subs_list:
            for d in data:
                li(a(h4(d['title']), target = '_blank', href='{}'.format(d['url']))) \
                    .add(label(' score: {}'.format(d['score'])))

    return st.markdown(reddit_subs_list, unsafe_allow_html=True)

def get_urls(tick):
    url_dict = {}
    url_dict['Robin Hood']  = f'https://robinhood.com/stocks/{tick}'
    url_dict['CNN Money'] = f'https://money.cnn.com/quote/forecast/forecast.html?symb={tick}'
    url_dict['Yahoo Finance'] = f'https://finance.yahoo.com/quote/{tick}'

    m_list = ''
    for u in url_dict.keys():
        m_list += f'  - [{u} ({tick})]({url_dict[u]})\n'
    st.markdown(m_list)


st.title('Reddit Stocks')
col21,col22,col23,col24 = st.beta_columns(4)
with col21:
    ticker = st.empty()
    my_expander = st.beta_expander('Refresh Data')
    with my_expander:
        interval = st.number_input("Last N hours", min_value = 1, max_value = 48, value = 24)
        clicked = st.button('Submit')

if clicked:
    session_state.clicked = True
    session_state.df, session_state.tickers, session_state.subs = pull_data(interval)
    st.balloons()

if session_state.clicked:
    df, tickers, subs = session_state.df, session_state.tickers, session_state.subs
else:
    df, tickers, interval, subs = init()
    
with col21:
    tick = ticker.selectbox('Select Ticker to see additional info', tickers)
with col22:
    if tick != 'All':
        st.markdown('### Links')
        get_urls(tick)
# with col23:
    # iframe(src=f'https://www.tradingview.com/chart/?symbol={tick}')
    # <img src="https://chart.finance.yahoo.com/z?s=AAPL&t=6m&q=l&l=on&z=s&p=m50,m200"/>
    # https://finance.yahoo.com/quote/TANH


table = df 
    
def scatter_plot(df,x,y, x_title = '', y_title = ''):
    x_title = x if not x_title else x_title
    y_title = y if not y_title else y_title
    chart = alt.Chart(df).mark_point().encode(
        # The notation below is shorthand for:
        # x = alt.X("Acceleration", type="quantitative", title="Acceleration"),
        x=alt.X(x, type="quantitative", title=x_title),

        y=alt.Y(y, type="quantitative", title=y_title),
    )
    text = alt.Chart({'values':[{}]}).mark_text(
        align="left", baseline="top"
    ).encode(
        x=alt.value(5),  # pixels from left
        y=alt.value(5),  # pixels from top
        text=alt.value(f"r: {df[x].astype(float).corr(df[y].astype(float)) :.3f}"),
    )

    st.write(chart + text + chart.transform_regression(x,y).mark_line())

st.dataframe(table, height = 500)

plots_expander = st.beta_expander('Plots and Analysis')
with plots_expander:
    col31,col32,col33,col34 = st.beta_columns(4)
    with col31:
        scatter_plot(table,'%Change','Change')
    with col32:
        scatter_plot(table,'%Change','Total')


subs = subs[subs.tickers_extracted.astype(str).str.contains(tick, na = False)] if tick != 'All' else subs[subs.tickers_extracted.astype(str)!='[]']
subs = subs.sort_values(by = ['score'], ascending = False)

st.markdown(f'## Posts ({len(subs)})')
get_reddit_list(subs.to_dict(orient = 'records'))
# table

