import requests
import pandas as pd
from datetime import datetime, timedelta
import os

def initialize():

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    url = "https://api.nbp.pl/api/exchangerates/rates/a/"   # API url for retrieving exchange rates
    currencies = ['eur','usd','chf']                        # currencies to retrieve

    exh_rates_dictionary = {**{'date': []}, **{f'{currency}/pln': [] for currency in currencies}}

    for currency in currencies:
        try:    # retrieve data for currency for the last 30 days
            data = requests.get(f'{url}/{currency}/{start_date}/{end_date}')
        except Exception as e:      # if something fails, inform user and abort program
            print(f'Failed to fetch data: {e}')
            return None
        
        data = data.json()  # decode

        for i in data['rates']:
            rate = i['mid'] # average daily rate
            exh_rates_dictionary[f'{currency}/pln'].append(rate) # filling the dictionary

            if currency == currencies[0]:   # fill dictionary with dates only during 1st iteration
                date = i['effectiveDate']
                exh_rates_dictionary['date'].append(date)

    exh_rates_df = pd.DataFrame.from_dict(exh_rates_dictionary) # create pandas DataFrame
    exh_rates_df['eur/usd'] = (exh_rates_df['eur/pln']/exh_rates_df['usd/pln']).round(4)   # calculate eur/usd
    exh_rates_df['chf/usd'] = (exh_rates_df['chf/pln']/exh_rates_df['usd/pln']).round(4)   # and       chf/usd
    exh_rates_df.to_csv('all_currency_data.csv',index=False)    # save into a CSV file
    os.system('cls||clear')
    print('Initialized successfully!')
    print('All currency data has been saved!\n')

    return exh_rates_df

def main_menu(exh_rates_df):
    columns_names = exh_rates_df.columns.tolist()
    selected = []   # exchange rates selected by user

    while True: # main loop
        choice = display_menu(selected)

        if choice == '1':
            selected = rates_selection(columns_names, selected)

        elif choice == '2':
            selected = save_selected(selected, exh_rates_df)

        elif choice == '3': 
            data_analysis(exh_rates_df, selected)

        elif choice == '4': # quit program
            break

        else:
            os.system('cls||clear')

def display_menu(selected):

    print('Menu:')
    print('1. Select rates')
    print('2. Save selected rates (currently selected: ',', '.join(selected),')')
    print('3. Analyze selected currency pair')
    print('4. Quit')
    user_choice = input('\nChoose an option: ')

    return user_choice

def rates_selection(columns_names, selected):

    os.system('cls||clear')
    print('Available options:\n')               ###############

    for i in range(1,len(columns_names)):       #             #
        print(f'{i}. {columns_names[i]}')       #   submenu   #
                                                #             #
    print(f'{len(columns_names)}. Clear all')
    print(f'[any other number]. Back')          ###############

    while True:
        try:
            pair_choice = int(input('\nChoose an option: '))    # type casting
            break
        except ValueError:
            print('Please enter an integer.')   # if user passed wrong input

    if pair_choice in range(1,len(columns_names)):      # exchange rates options
        if columns_names[pair_choice] not in selected:  # if pair is not already selected...
            selected.append(columns_names[pair_choice]) # ...select it
            os.system('cls||clear')

        else:                                           # if pair is already selected - inform user
            os.system('cls||clear')
            print('Already selected!')

    elif pair_choice == (len(columns_names)):           # if user wanted to clear selected pairs...
        selected = []                                   # ... do it
        os.system('cls||clear')

    else:                                               # any other number will exit the submenu
        os.system('cls||clear')
        pass

    return selected                                     # return selected currency pairs

def save_selected(selected, exh_rates_df):

    os.system('cls||clear')
    if len(selected) == 0:  # if no pair was selected inform user                                                  
        print('No currency pair was selected.')
    else:
        selected.insert(0,'date')
        selected_data = exh_rates_df[selected]  # create new dataframe with selected pairs and 'date' column
        selected_data.to_csv('selected_currency_data.csv',index=False)
        print('Data for ',', '.join(selected[1:]),' has been saved!\n')
        selected = []   # clear selected after saving

    return selected

def data_analysis(exh_rates_df, selected_currencies):

    os.system('cls||clear')
    for pair in selected_currencies:    # for each selected pair
        average = exh_rates_df[f'{pair}'].mean()    # get metrics using
        median = exh_rates_df[f'{pair}'].median()   # inbuilt functions
        minimum = exh_rates_df[f'{pair}'].min()
        maximum = exh_rates_df[f'{pair}'].max()

        # display info for user
        print(f'\nStatistical metrics for {pair} for last 30 days are:')
        print(f'Average: {average:.4f}')
        print(f'Median: {median:.4f}')
        print(f'Maximum: {maximum:.4f}')
        print(f'Minimum: {minimum:.4f}')
    print('\n')

    return


if __name__ == "__main__":
    currency_data = initialize()    # start

    if currency_data is not None:   # if initialized successfully, move on
        main_menu(currency_data)
