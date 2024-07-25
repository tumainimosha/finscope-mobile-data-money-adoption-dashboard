import pandas as pd

def mm_model(sf, model, preprocessor):

    sf.title('Mobile Money Adoption Model')

    sf.write('''
    ## What-if Analysis
    ''')

    # Create three columns
    col1, col2, col3 = sf.columns(3)

    # Organize inputs into the three columns
    with col1:
        phone_network_quality_at_home = sf.checkbox('Phone Network Quality at Home', value=False)
        has_access_to_internet = 1 if phone_network_quality_at_home else 0

        comfortable_to_use_financial_services = sf.checkbox('Comfortable to Use Financial Services', value=False)

    with col2:
        has_received_some_financial_education = sf.checkbox('Has Received Some Financial Education', value=False)
        has_national_id = sf.checkbox('Has National ID', value=False)

    with col3:
        trust_issues = sf.checkbox('Has Trust Issues on MM', value=True)
        


    # Define the options for the select box
    phone_type_options = {
        'Simple Phone': 1,
        'Smart Phone': 2,
        'No Phone': 0
    }

    # Create two columns
    col1, col2 = sf.columns(2)

    # Column 1
    with col1:
        gender_label = sf.selectbox("Gender:", ['Female', 'Male'])
        gender = 0 if gender_label == 'Male' else 1

        phone_type_label = sf.selectbox("Phone Type:", list(phone_type_options.keys()))
        phone_type = phone_type_options[phone_type_label]

        has_access_to_mobile_phone = 1 if phone_type > 0 else 0
        owns_a_mobile_phone = 1 if phone_type > 0 else 0
        owns_a_sim_card = 1 if phone_type > 0 else 0

        age = sf.slider('Age', 0, 100, 50)

        

    # Column 2
    with col2:
        rural_urban_label = sf.selectbox("Location:", ['Rural', 'Urban'])
        rural_urban = 0 if rural_urban_label == 'Rural' else 1

        income_main = sf.selectbox("Income Main:", ['Other', 'Farmer', 'Casual Labourer', 'Dependant'])
        is_a_dependant = 1 if income_main == 'Dependant' else 0
        is_casual_labourer = 1 if income_main == 'Casual Labourer' else 0
        is_farmer = 1 if income_main == 'Farmer' else 0

        highest_level_of_education = sf.slider('Highest Level of Education (0=None, 9=University)', 0, 9, 3)

    # Preprocess the data
    data = [[
        comfortable_to_use_financial_services, 
        has_received_some_financial_education, 
        highest_level_of_education, 
        has_access_to_mobile_phone, 
        has_access_to_internet, 
        owns_a_mobile_phone, 
        owns_a_sim_card, 
        phone_network_quality_at_home, 
        rural_urban, 
        trust_issues, 
        phone_type, 
        age, 
        gender,
        is_farmer, 
        is_casual_labourer, 
        is_a_dependant, 
        has_national_id
    ]]

    # convert data to dataframe
    df = pd.DataFrame(data, columns=[
        'comfortableToUseFinancialServices',
        'hasReceivedSomeFinancialEducation',
        'highestLevelOfEducation',
        'hasAccessToMobilePhone',
        'hasAccessToInternet',
        'ownsAMobilePhone',
        'ownsASimCard',
        'phoneNetworkQualityAtHome',
        'ruralUrban',
        'trustIssues',
        'phoneType',
        'age',
        'gender', # Gender
        'isFarmer', # Income type
        'isCasualLabourer', # Income type
        'isADependant', # Income type
        'hasNationalId', # Possess national id
    ])
        
    transformed_data = preprocessor.transform(df)

    # Predict
    prediction = model.predict(transformed_data)
    prediction_probability = model.predict_proba(transformed_data)

    # Output prediction whether the individual will adopt mobile money or not
    sf.write(f'''
    ## Prediction
    Uses Mobile Money: **{'Yes' if prediction[0] else 'No'}**

    Probability: **{prediction_probability[0][1] *  100:.2f}%**
    ''')
   


    

    
