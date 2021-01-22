import streamlit as st
st.set_page_config(layout="wide")
from streamlit.components.v1 import iframe
import streamlit.components.v1 as components

# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import SessionState
from AutoDD import getHistory
from get_data import refresh_data
import numpy as np
import pandas as pd
import dominate
from dominate.tags import div, p, h1,h2, h4, ul, a, li, label
import altair as alt

session_state = SessionState.get(clicked=False)

def local_css(file_name):
    '''
    Read in and apply user defined css.

    Args:
        file_name (str): path to the css file.

    Return:
        Nothing

    '''
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# apply user css
local_css('user.css')
# apply dark theme
local_css('dark.css')

# enable dark theme for altair charts
alt.themes.enable("dark")

            
@st.cache
def init():
    '''
    Initialize data.

    Return:
        df (dataframe): tickers extracted from posts with ticker stats
        ticker (list): list of ticker codes
        interval (int): time range to scrape for posts
        subs (dataframe): reddit posts
        history (dataframe): price history for stocks
    '''
    df = pd.read_csv('table_records.csv').sort_values(by='Total', ascending = False)
    tickers = ['All'] + df.Code.tolist()
    interval = 24
    # subs = [{'title': ' Buying otc in Canada ', 'title_extracted': [], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhr80/buying_otc_in_canada/'}, {'title': ' Maganese Corp MNXXF ', 'title_extracted': ['MNXXF'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhncj/maganese_corp_mnxxf/'}, {'title': ' UAMY Looking Good 🙌🏼 ', 'title_extracted': ['UAMY'], 'url': 'https://www.reddit.com/gallery/kxhkss'}, {'title': ' Asking for a DD &amp; Catalyst BEFORE the run... $VNUE is still .01 and is ready to pop (some DD included) ', 'title_extracted': ['VNUE', 'BEFOR'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhik0/asking_for_a_dd_catalyst_before_the_run_vnue_is/'}, {'title': ' Actual Due Diligence for TANH - (Not Moon Hype for once) Tantech Holdings Ltd ', 'title_extracted': ['TANH'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhh25/actual_due_diligence_for_tanh_not_moon_hype_for/'}, {'title': ' $PHUN Blockchain play ', 'title_extracted': ['PHUN'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhe3z/phun_blockchain_play/'}, {'title': ' Resort Savers (RSSV) starting to move... ', 'title_extracted': ['RSSV'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhde6/resort_savers_rssv_starting_to_move/'}, {'title': ' Anomalous Stocks, January 14, 2021 ', 'title_extracted': [], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh99k/anomalous_stocks_january_14_2021/'}, {'title': ' GGBXF doubling in price? Why? ', 'title_extracted': ['GGBXF'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh8yi/ggbxf_doubling_in_price_why/'}, {'title': ' WANT A STOCK WITH A SOLID TICKER NAME? Buy $EVUS 🚀🚀🚀🚀🚀 ', 'title_extracted': ['SOLID', 'WITH', 'TICKE', 'EVUS', 'STOCK', 'NAME', 'WANT'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh8tb/want_a_stock_with_a_solid_ticker_name_buy_evus/'}, {'title': ' $VGLS ready to TAKE OFF ', 'title_extracted': ['VGLS', 'OFF', 'TAKE'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh7ng/vgls_ready_to_take_off/'}, {'title': ' What is a good price target for BNGO? ', 'title_extracted': ['BNGO'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh57r/what_is_a_good_price_target_for_bngo/'}, {'title': ' $SENS IS MOON BOUND 🚀🚀🌕🌕 ', 'title_extracted': ['MOON', 'BOUND', 'SENS'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh4mj/sens_is_moon_bound/'}, {'title': ' ASTI &amp; OMEG to the moon?! 🚀🚀🚀 ', 'title_extracted': ['OMEG', 'ASTI'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxgxup/asti_omeg_to_the_moon/'}]
    subs = pd.read_json('submissions.json')
    history = pd.read_csv('history.csv')
    return df, tickers, interval, subs, history


def pull_data(interval):
    df, subs, history = refresh_data(int(interval))
    tickers = ['All'] + df.sort_values(by='Total', ascending = False).Code.tolist()

    return df, tickers, subs, history

def get_reddit_list(data):
    '''
    Create html list of posts using dominate.

    Args:
        data (dataframe): dataframe of reddit posts
    '''
    # data = [{'title': ' Buying otc in Canada ', 'title_extracted': [], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhr80/buying_otc_in_canada/'}, {'title': ' Maganese Corp MNXXF ', 'title_extracted': ['MNXXF'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhncj/maganese_corp_mnxxf/'}, {'title': ' UAMY Looking Good 🙌🏼 ', 'title_extracted': ['UAMY'], 'url': 'https://www.reddit.com/gallery/kxhkss'}, {'title': ' Asking for a DD &amp; Catalyst BEFORE the run... $VNUE is still .01 and is ready to pop (some DD included) ', 'title_extracted': ['VNUE', 'BEFOR'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhik0/asking_for_a_dd_catalyst_before_the_run_vnue_is/'}, {'title': ' Actual Due Diligence for TANH - (Not Moon Hype for once) Tantech Holdings Ltd ', 'title_extracted': ['TANH'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhh25/actual_due_diligence_for_tanh_not_moon_hype_for/'}, {'title': ' $PHUN Blockchain play ', 'title_extracted': ['PHUN'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhe3z/phun_blockchain_play/'}, {'title': ' Resort Savers (RSSV) starting to move... ', 'title_extracted': ['RSSV'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxhde6/resort_savers_rssv_starting_to_move/'}, {'title': ' Anomalous Stocks, January 14, 2021 ', 'title_extracted': [], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh99k/anomalous_stocks_january_14_2021/'}, {'title': ' GGBXF doubling in price? Why? ', 'title_extracted': ['GGBXF'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh8yi/ggbxf_doubling_in_price_why/'}, {'title': ' WANT A STOCK WITH A SOLID TICKER NAME? Buy $EVUS 🚀🚀🚀🚀🚀 ', 'title_extracted': ['SOLID', 'WITH', 'TICKE', 'EVUS', 'STOCK', 'NAME', 'WANT'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh8tb/want_a_stock_with_a_solid_ticker_name_buy_evus/'}, {'title': ' $VGLS ready to TAKE OFF ', 'title_extracted': ['VGLS', 'OFF', 'TAKE'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh7ng/vgls_ready_to_take_off/'}, {'title': ' What is a good price target for BNGO? ', 'title_extracted': ['BNGO'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh57r/what_is_a_good_price_target_for_bngo/'}, {'title': ' $SENS IS MOON BOUND 🚀🚀🌕🌕 ', 'title_extracted': ['MOON', 'BOUND', 'SENS'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxh4mj/sens_is_moon_bound/'}, {'title': ' ASTI &amp; OMEG to the moon?! 🚀🚀🚀 ', 'title_extracted': ['OMEG', 'ASTI'], 'url': 'https://www.reddit.com/r/pennystocks/comments/kxgxup/asti_omeg_to_the_moon/'}]
    reddit_subs_list = div(id='reddit-submission', style = 'max_height: 500px') \
            .add(div(style = 'overflow:hidden;')) \
            .add(ul(style = 'overflow-y:scroll; height: 500px;'))
    with reddit_subs_list:
            for d in data:
                li(a(h4(d['title']), target = '_blank', href='{}'.format(d['url']))) \
                    .add(label(' score: {}'.format(d['score'])))

    return st.markdown(reddit_subs_list, unsafe_allow_html=True)

def get_urls(tick):
    url_dict = {}
    url_dict['Robin Hood']  = [f'https://robinhood.com/stocks/{tick}','https://robinhood.com/favicon.ico']
    url_dict['CNN Money'] = [f'https://money.cnn.com/quote/forecast/forecast.html?symb={tick}','']
    url_dict['Yahoo Finance'] = [f'https://finance.yahoo.com/quote/{tick}','']

    m_list = ''
    favicon = '''<link rel="icon" 
      type="image/png" 
      href="{}" />'''
    for u in url_dict.keys():
        fav = favicon.format(url_dict[u][1]) if url_dict[u][1] != '' else ''
        m_list += f'  - [{u} ({tick})]({url_dict[u][0]})\n'
    st.markdown(m_list, unsafe_allow_html=True)

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

    st.write((chart + text + chart.transform_regression(x,y).mark_line()).configure(background='#000000'))

def line_plot(data, x = 'date:T',y = 'close:Q', color = 'symbol:N', verticals = None, title = None, legend = None):
    chart = (
        alt.Chart(data.reset_index())
        .mark_line()
        .encode(y = alt.Y(y, scale=alt.Scale(zero=False), axis = alt.Axis(orient = 'right', title = '', format='$,r')), 
                x=alt.X(x, scale=alt.Scale(zero=False), axis = alt.Axis(title = '')), 
                color=alt.Color(color, legend=None) if legend is None else alt.Color(color),
                tooltip = [color,alt.Tooltip(y, format='$.2f'),x])
        .properties(
            #  width='container'
        )
    )

    if verticals:
        chart += verticals

    if title:
        chart += chart.properties(title = title)

    chart = chart.configure(background='#000000').configure_axis(
        grid=False
    ).configure_view(strokeOpacity=0)

    chart

def tradingview(ticker, components, height = 300, width = 400):
    embed = '''
     <!-- TradingView Widget BEGIN -->
 <div class="tradingview-widget-container">
    <div id="tradingview_5032c"></div>
    <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Chart</span></a> by TradingView</div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget(
    {{
    "autosize": false,
    "width": {0},
    "height": {1},
    "symbol": "{2}",
    "interval": "D",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "3",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_5032c"
  }}
    );
    </script>
  </div>
  <!-- TradingView Widget END -->
    '''
    # HtmlFile = open(embed, 'r', encoding='utf-8')
    # source_code = HtmlFile.read() 
    source_code = embed
    # st.write(source_code.format(ticker))

    components.html(source_code.format(width, height, ticker), height = height)

def refresh_data_button():
    my_expander = st.beta_expander('Refresh Data')
    with my_expander:
        interval = st.number_input("Last N hours", min_value = 1, max_value = 48, value = 24)
        clicked = st.button('Submit')
    return interval,clicked
    


if session_state.clicked:
    df, tickers, subs, history = session_state.df, session_state.tickers, session_state.subs, session_state.history 
else:
    df, tickers, interval, subs, history  = init()

st.title('🚀🚀🚀 Reddit Stocks 🚀🚀🚀')
col21,buffer,col22,col23 = st.beta_columns((2,1,2,3))

with col21:
    ticker_select = st.empty()
    interval, clicked = refresh_data_button()
    tick = ticker_select.selectbox('Select Ticker to see additional info', tickers)
    
    if clicked:
        session_state.clicked = True
        session_state.df, session_state.tickers, session_state.subs, session_state.history = pull_data(interval)
        st.balloons()
        tick = ticker_select.selectbox('Select Ticker to see additional info', session_state.tickers)


table = df if tick == 'All' else df[df.Code == tick]

with col22:
    if tick != 'All':
        st.markdown('## ${}'.format(tick))
        st.markdown('### Links')
        get_urls(tick)
    else:
        st.empty()
with col23:
    if tick != 'All':
        tradingview(tick,components, width=500)
    else:
        with col23:
            line_plot(history[history.symbol.isin(table.sort_values(by='Total',ascending = False)[:10].Code)], 
            title = 'Price of Top 10 Most Mentioned Stocks')
    
# with col24:
#     query_params = st.experimental_get_query_params()
#     st.write(query_params)
#     # iframe(src=f'https://www.tradingview.com/chart/?symbol={tick}')
#     # <img src="https://chart.finance.yahoo.com/z?s=AAPL&t=6m&q=l&l=on&z=s&p=m50,m200"/>
#     # https://finance.yahoo.com/quote/TANH


tableStyler = table.style.set_table_styles([ dict(selector='div', props=[('text-align', 'center')] ) ]).set_properties(**{'text-align': 'center'}).hide_index()
data_table_expander = st.beta_expander('Show Data Table', expanded=False)
with data_table_expander:
    st.dataframe(tableStyler, height=300)

subs = subs[subs.tickers_extracted.astype(str).str.contains(tick, na = False)] if tick != 'All' else subs[subs.tickers_extracted.astype(str)!='[]']
subs = subs.sort_values(by = ['score'], ascending = False)


    
plots_expander = st.beta_expander('Plots and Analysis', expanded=True)
with plots_expander:
    col31,col32,col33,col34 = st.beta_columns(4)
    with col31:
        scatter_plot(table,'%Change','Change')
    with col32: 
        chart = alt.Chart(subs, title = "Posts by hour").transform_aggregate(
            count = 'count(title):Q',
            groupby=['created_date','flair']
        ).mark_bar().encode(
            x = alt.X('hours(created_date):O', title = 'datetime'),
            y = alt.Y('sum(count):Q', title = 'count'),
            color=alt.Color('flair'),
            tooltip=['flair',alt.Tooltip('created_date:T', format='%Y-%m-%d %H:%M')]
        ).configure(background='#000000'
        ).configure_axis(grid=False
        ).configure_view(strokeOpacity=0)

        chart



# data = getHistoryCache(table.Code,'3mo','1d')
# data

st.markdown(f'## Posts ({len(subs)})')
get_reddit_list(subs.to_dict(orient = 'records'))
# table



