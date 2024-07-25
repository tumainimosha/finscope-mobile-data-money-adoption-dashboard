from matplotlib import pyplot as plt
import streamlit as st


def mm_adoption_visualization(data):
    # 1. Define indicator variable y1 into one variable `usesMobileMoney` of type boolean
    data.loc[:, 'usesMobileMoney'] = data['MM'].apply(lambda x: x == 'MM')

    # 2. Define indicator variable y2 into `lastMobileMoneyUsage` as an ordinal variable
    last_mobile_money_usage_map = {
        'Yesterday/today': 1,
        'In the past 7 days': 2,
        'In the past 30 days': 3,
        'In the past 90 days': 4,
        'In the past 6 months': 5,
        'Longer than 6 months ago': 6,
        ' ': 7, # No Use
    }
    data.loc[:, 'lastMobileMoneyUsage'] = data['mob9_2'].map(last_mobile_money_usage_map)

    # 1. Prepare pie chart of mobile money usage ration
    pie_chart_data = data['usesMobileMoney'].value_counts()
    pie_chart_data.index = ['Uses Mobile Money', 'Does not use Mobile Money']


    # 2. Prepare a bar chart of `lastMobileMoneyUsage` percentages
    last_mobile_money_usage_data = data['lastMobileMoneyUsage'].value_counts().sort_index()
    # Replace count with percentages
    last_mobile_money_usage_data = last_mobile_money_usage_data / last_mobile_money_usage_data.sum() * 100
    # Replace the numbers with their corresponding labels
    last_mobile_money_usage_data.index = ['1 day', '1 week', '1 month', '3 months', '6 months', '> 6 months', 'No use']

    # 3. Prepare a stacked bar chart of `rural/urban` mobile money usage
    # Order the bars by "Urban", "Rural", group by `usesMobileMoney`
    cluster_type_data = data.groupby(['RU', 'usesMobileMoney']).size().unstack()

    # Replace count with percentages
    cluster_type_data = cluster_type_data.div(cluster_type_data.sum(axis=1), axis=0) * 100

    # replace True and False with `Yes` and `No` labels
    cluster_type_data.columns = ['No', 'Yes']

    map_cluster_type = {
        'Dar es Salaam': 'Dar',
        'Other urban': 'Other Urban',
        'Rural': 'Rural',
        'Zanzibar': 'ZNZ',
    }

    cluster_type_data.index = cluster_type_data.index.map(lambda x: map_cluster_type[x])

    # Bar Chart displayed later below
    cluster_type_data.head()

    # 4. Prepare a stacked bar chart on mobile money usage by gender
    gender_mob_usage_data = data.groupby(['c9', 'usesMobileMoney']).size().unstack()

    # Replace count with percentages
    gender_mob_usage_data = gender_mob_usage_data.div(gender_mob_usage_data.sum(axis=1), axis=0) * 100

    # replace True and False with Yes and No
    gender_mob_usage_data.columns = ['No', 'Yes']

    # Bar Chart displayed later below
    gender_mob_usage_data.head()


    # 5. Prepare a stacked bar chart on mobile money usage by income type
    income_type_data = data.groupby(['IncomeMain', 'usesMobileMoney']).size().unstack()

    # Replace count with percentages
    income_type_data = income_type_data.div(income_type_data.sum(axis=1), axis=0) * 100

    # replace True and False with Yes and No
    income_type_data.columns = ['No', 'Yes']

    # Sort data by 'Yes' column
    income_type_data = income_type_data.sort_values('Yes', ascending=True)

    # Bar Chart displayed later below
    income_type_data.head()


    # 6. Prepare a stacked bar chart on reasons for not using mobile money `mob3`
    # filter out the rows where `usesMobileMoney` is False
    non_usage_reasons_data = data.loc[~data['usesMobileMoney'], 'mob3'].value_counts()

    # Replace count with percentages
    non_usage_reasons_data = non_usage_reasons_data.div(non_usage_reasons_data.sum(axis=0), axis=0) * 100

    # Sort data by 'Yes' column
    non_usage_reasons_data = non_usage_reasons_data.sort_values(ascending=False)[:7]

    map_non_usage_reasons = {
        'I do not have a smartphone': 'No Smartphone',
        'I do not need it, I do not make any transactions': 'No Transactions',
        'I do not have the required documents': 'No Documents',
        'Forgot the password/Sim Card is blocked/network problem': 'Forgot Password',
        'Fees for using this service are too high': 'High Fees',
        'There is no point-of-service/agent close to where I live': 'No Agents',
        'My spouse, family, in-laws do not approve of me having a mobile money account': 'Family Disapproval',
    }

    non_usage_reasons_data.index = non_usage_reasons_data.index.map(lambda x: map_non_usage_reasons[x])

    # Bar Chart displayed later below
    non_usage_reasons_data.head(10)



    # Perform feature engineering to prepare the data for modeling

    # define `phoneOwnership` as an indicator variable.
    #  Is `Simple Phone`, `Smart Phone` or `No Phone`, based on
    #    `c25__1` = 'Yes' => 'Smart Phone' and `c25__2` = 'Yes' => 'Simple Phone', else 'No Phone'
    data['phoneOwnership'] = data.apply(lambda row: 'Smart Phone' if row['c25__1'] == 'Yes' else ('Simple Phone' if row['c25__2'] == 'Yes' else 'No Phone'), axis=1)

    # Prepare bar chart data for phoneOwnership againt Mobile Money Usage
    phone_ownership_data = data.groupby(['phoneOwnership', 'usesMobileMoney']).size().unstack(fill_value=0)

    # Convert usage to percentage



    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Create a 2x3 grid of subplots
    fig = make_subplots(
        rows=3, 
        cols=2, 
        subplot_titles=[
            '(i) Mobile Money Usage', 
            '(ii) Mobile Money Usage Frequency', 
            '(iii) Mobile Money Usage by Cluster Type', 
            '(iv) Mobile Money Usage by Gender', 
            '(v) Income groups with least MM Usage', 
            '(vi) Reasons for not using Mobile Money'
        ],
        specs=[
            [{'type': 'domain'}, {'type': 'xy'}],
            [{'type': 'xy'}, {'type': 'xy'}],
            [{'type': 'xy'}, {'type': 'xy'}],
        ]
    )

    # Pie chart
    fig.add_trace(
        go.Pie(labels=pie_chart_data.index, values=pie_chart_data.values, 
            textinfo='percent', marker=dict(colors=['limegreen', 'lightcoral'])),
        row=1, col=1
    )

    # Bar chart for last mobile money usage
    fig.add_trace(
        go.Bar(x=last_mobile_money_usage_data.index, y=last_mobile_money_usage_data, 
            marker=dict(color=['limegreen', 'limegreen', 'limegreen', 'limegreen', 'limegreen', 'limegreen', 'lightcoral'])),
        row=1, col=2
    )
    # fig.update_xaxes(title_text='Days Since Last Use', row=1, col=2)
    # fig.update_yaxes(title_text='Percentage (%)', row=1, col=2)

    # Bar chart for mobile money usage by cluster type
    fig.add_trace(
        go.Bar(x=cluster_type_data.index, y=cluster_type_data['Yes'], 
            marker=dict(color='limegreen')),
        row=2, col=1
    )

    # Bar chart for mobile money usage by gender
    fig.add_trace(
        go.Bar(x=gender_mob_usage_data.index, y=gender_mob_usage_data['Yes'], 
            marker=dict(color='limegreen')),
        row=2, col=2
    )

    # Bar chart for mobile money usage by income type
    top_5_income_types = income_type_data.head(5)
    fig.add_trace(
        go.Bar(x=top_5_income_types.index, y=top_5_income_types['Yes'], 
            marker=dict(color='limegreen')),
        row=3, col=1
    )

    # Bar chart for reasons for not using mobile money
    fig.add_trace(
        go.Bar(x=non_usage_reasons_data.index, y=non_usage_reasons_data, 
            marker=dict(color='lightcoral')),
        row=3, col=2
    )

    # Update layout for better visibility
    fig.update_layout(
        height=800, width=1200, 
        title_text='Mobile Money Adoption Trend', 
        title_font_size=16, title_font=dict(color='black', family='Arial', size=20, weight='bold'),
        title_x=0.5,  # Center the title
        title_xanchor='center',  # Center the title
        # title_font=dict(size=20, family='Arial', color='black', bold=True),  # Bold the title
        showlegend=False
    )

    # Show the plot
    # fig.show()
    # plt.show()

    st.plotly_chart(fig)


    # Define `phoneOwnership` as an indicator variable.
    #  Is `Simple Phone`, `Smart Phone` or `No Phone`, based on
    #    `c25__1` = 'Yes' => 'Smart Phone' and `c25__2` = 'Yes' => 'Simple Phone', else 'No Phone'
    data['phoneOwnership'] = data.apply(lambda row: 'Smart Phone' if row['c25__1'] == 'Yes' else ('Simple Phone' if row['c25__2'] == 'Yes' else 'No Phone'), axis=1)

    # 1. Prepare bar chart data for phoneOwnership againt Mobile Money Usage
    phone_ownership_data = data.groupby(['phoneOwnership', 'usesMobileMoney']).size().unstack(fill_value=0)

    # Convert usage to percentage
    phone_ownership_data = phone_ownership_data.div(phone_ownership_data.sum(axis=1), axis=0) * 100

    # Replace True and False with 'Yes' and 'No'
    phone_ownership_data.columns = ['No', 'Yes']

    # 2. Prepare data of Trend of `lastMobileMoneyUsage` v/s `phoneOwnership`
    last_mobile_money_usage_phone_ownership_data = data.groupby(['lastMobileMoneyUsage', 'phoneOwnership']).size().unstack(fill_value=0)

    # Convert usage to percentage
    last_mobile_money_usage_phone_ownership_data = last_mobile_money_usage_phone_ownership_data.div(last_mobile_money_usage_phone_ownership_data.sum(axis=1), axis=0) * 100

    # Adjust the subplots to a 1x2 grid
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Plot the data
    last_mobile_money_usage_phone_ownership_data.plot(kind='bar', stacked=True, ax=axs[0], color=['lightcoral', 'skyblue', 'royalblue'])
    axs[0].set_title('Mobile Money Usage by Phone Ownership and Frequency')
    axs[0].set_xlabel('Days since last use')
    axs[0].set_ylabel('Percentage (%)')
    axs[0].legend(title='Phone Ownership', loc='upper left')
    axs[0].set_xticklabels(last_mobile_money_usage_data.index, rotation=0)

    # Plot the data
    phone_ownership_data.plot(kind='bar', stacked=True, color=['lightcoral', 'limegreen'], ax=axs[1])
    axs[1].set_title('Mobile Money Usage by Phone Ownership')
    axs[1].set_xlabel('Phone Ownership')
    axs[1].set_ylabel('Percentage (%)')
    axs[1].set_xticklabels(phone_ownership_data.index, rotation=0)

    # Add an overall title
    fig.suptitle('Mobile Money Adoption vs Phone Ownership', fontsize=16, fontweight='bold')

    plt.tight_layout()
    # plt.show()

    st.pyplot(fig)


    # Education level
    # Define the ordinal mapping of the education levels
    edu_level_ordinal_mapping = {
        'Don’t know': 0, # Treat 'Don’t know' as NaN
        'No formal education': 1,
        'Some primary': 2,
        'Primary completed': 3,
        'Post primary technical training': 4,
        'Some secondary': 5,
        'Secondary competed-O level': 6,
        'Secondary completed-A level': 7,
        'Some University or other higher education': 8,
        'University or higher education completed': 9,
    }

    # Apply the mapping to the 'c11' column
    data.loc[:, 'highestLevelOfEducation'] = data['c11'].map(edu_level_ordinal_mapping)
    edu_level_data = data.groupby(['highestLevelOfEducation', 'usesMobileMoney']).size().unstack()

    # Replace count with percentages
    edu_level_data = edu_level_data.div(edu_level_data.sum(axis=1), axis=0) * 100
    # replace True and False with `Yes` and `No` labels
    edu_level_data.columns = ['No', 'Yes']
    # Replace the numbers with their corresponding labels
    edu_level_data.index = edu_level_data.index.map({v: k for k, v in edu_level_ordinal_mapping.items()})

    # Adjust the subplots to a 1x1 grid
    fig, axs = plt.subplots(1, 1, figsize=(10, 6))
    edu_level_data['Yes'].plot(kind='bar', ax=axs, color=['limegreen'])
    axs.set_title('Highest Level of Education Completed vs Uses Mobile Money')
    axs.set_xlabel('Level of Education')
    axs.set_ylabel('Percentage (%)')
    axs.legend(title='Uses Mobile Money', loc='upper left')
    axs.set_xticklabels(edu_level_data.index, rotation=45)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    st.pyplot(fig)

    return None



