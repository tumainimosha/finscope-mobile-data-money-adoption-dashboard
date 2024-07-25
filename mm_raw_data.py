

def mm_raw_data(st, df, df_mapping):
    st.write('''
    ## Finscope Data
    ''')

    # Show data
    # if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

    st.write('''
    ## Summary
    ''')

    # Summary
    st.write(df.describe())

    st.write('''
        ## Data Mapping
        ''')
    st.subheader('Raw data')
    st.write(df_mapping)