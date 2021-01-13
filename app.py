import streamlit as st
st.set_page_config(layout="wide")
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

def main():
    df = pd.read_csv('table_records.csv')

    st.title('Reddit Stocks')
    ticker = st.selectbox('Example', ['All'] + df.Code.tolist())

    
    st.write("Here's our first attempt at using data to create a table:")
    table = df if ticker == 'All' else df[df.Code == ticker]
    # st.table(table)
    table

if __name__ == '__main__':
    main()