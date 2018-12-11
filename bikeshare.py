import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def input_city():
    #To begin the interactivity with the user. It will ask for the user's choice as input city.
    print('Hello! Let\'s explore some US bikeshare data together!')
    print(' ')
    #To get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    print('We have the following cities and their corresponding numbers.')
    print('1 - Chicago')
    print('2 - New York City')
    print('3 - Washington')
    print(' ')
    city = input('Please choose a city: ')
    city = city.lower()
    while True: #To handle unexpected city input by user.
            if city == '1' or city == 'chicago':
                print("\nChicago, the Windy City! Cool.")
                return 'chicago'
            elif city == '2' or city == 'new york city':
                print("\nNew York City, the Big Apple! Cool.")
                return 'new york city'
            elif city == '3' or city == 'washington':
                print("\nWashington, the Nation's Capital! Cool.")
                return 'washington'
            #The below will be displayed to ask for user input again.
            else:
                print('\nInvalid Input. Please enter 1, 2, or 3, or the name of the city.\n')
                city = input('Please choose a city again: ')
                city = city.lower()
    return city

def input_time(): #To get the user to choose between month & day of the month, day of the week only, or no filters at all.
    print('You can choose to filter by month & day of the month, day of the week, or no filters at all.')
    print('month - Month & Day of the Month')
    print('day - Day of the Week')
    print('no - No Filters')
    period = input('\nEnter your choice: ')
    period = period.lower()

    while True:
        if period == "month":
            while True:
                day_month = input("Do you want to filter the data by day of the month as well? Type 'yes' or 'no': ").lower()
                if day_month == "no":
                    print('Alright, the data will be filtered by month only.\n')
                    return 'month'
                elif day_month == "yes":
                    print ('\nAlright, the data will be filtered by month and day of the month.')
                    return 'day_of_month'

        elif period == "day":
            print('Alright, the data will be filtered by the day of the week.\n')
            return 'day_of_week'
        elif period == "no":
            print('Alright, no time filter will be applied.\n')
            return "none"
        period = input("\nSorry. Please choose a time filter by inputting 'month', 'day', or 'no': ").lower()

def month_choice(m): #To get user input for name of month.
    if m == 'month':
        month = input('We have data for January, February, March, April, May, and June. Choose your month: ')
        while month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nSorry, please input one of January, February, March, April, May, or June. Type again: ')
        return month.lower()
    else:
        return 'none'

def month_day_choice(df, day_m): #To ask the user for the month plus the day of the week.
    month_day = []
    if day_m == "day_of_month":
        month = month_choice("month")
        month_day.append(month)
        maximum_day_month = max_day_month(df, month)

        while (True):
            ask = "Now which day of that month would you like? Please enter an integer between 1 and "
            ask  = ask + str(maximum_day_month) + ": "
            day_m = input(ask)

            try:
                day_m = int(day_m)
                if 1 <= day_m <= maximum_day_month:
                    month_day.append(day_m)
                    return month_day
            except ValueError:
                print("That is not a valid number for day of month input.")
    else:
        return 'none'

def day_info(d): #To ask the user for day of week input.
    if d == 'day_of_week':
        print('Which day of the week?')
        print('Mon - Monday\nTue - Tuesday\nWed - Wednesday\nThu - Thursday\nFri - Friday\nSat - Saturday\nSun - Sunday')
        day = input('\nEnter your choice: ')
        while day.lower() not in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
            day = input('\nInvalid input. Please input Mon, Tue, Wed, Thu, Fri, Sat, or Sun: ')
        return day.lower()
    else:
        return 'none'

def load_data(city):
    #To load csv for the chosen city.
    print('\nNext... \n')
    df = pd.read_csv(CITY_DATA[city])

    #To convert to and extract from Start Time.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df["day_of_month"] = df["Start Time"].dt.day
    return df

def time_stats(df, time, month, week_day, md): #To filter data and product new df according to all the criteria given by the user.
    print('\nGotcha! Now calculating stats for you!\n')
    #To filter by month.
    if time == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #To filter by day of week.
    if time == 'day_of_week':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days:
            if week_day.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]
    #To convert month and day section.
    if time == "day_of_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = md[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = md[1]
        df = df[df['day_of_month'] == day]
    return df

def max_day_month(df, month):
    #To get the max day of the month.
    months = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6}
    df = df[df["month"] == months[month]]
    max_day = max(df["day_of_month"])
    return max_day

def month_freq(df):
    #To get the most common month as Start Time.
    #To get the dataframes returned from time_stats.
    print('\nWHAT WAS THE MOST COMMON MONTH FOR BIKE USAGE?\n')
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m - 1].capitalize()
    return popular_month

def day_freq(df):
    #To get the most common day of week as Start Time.
    #To get the dataframes returned from time_stats.
    print('\nWHAT WAS THE MOST COMMON DAY OF THE WEEK FOR BIKE USAGE?\n')
    return df['day_of_week'].value_counts().reset_index()['index'][0]

def hour_freq(df):
    #To get the most common hour of day as Start Time.
    #To get the dataframes returned from time_stats.
    print('\nWHAT WAS THE MOST COMMON HOUR OF THE DAY FOR BIKE USAGE?\n')
    df['hour'] = df['Start Time'].dt.hour
    print("The most common hour was {}:00".format(df.hour.mode()[0]))
    #return df.hour.mode()[0]

def stations_freq(df):
    #To get the most common start station and most popular end station.
    #To get the dataframes returned from time_stats.
    print("\nWHAT WAS THE MOST COMMON START STATION?\n")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)
    print("\nWHAT WAS THE MOST COMMON END STATION?\n")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station

def common_trip(df):
    #To get the most common trip from start point to end point.
    #To get the dataframes returned from time_stats.
    com_trip = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nWHAT WAS THE MOST COMMON TRIP FROM START TO END?\n')
    return com_trip

def ride_duration(df):
    #To get the total ride duration and average ride duration.
    #To get the dataframes returned from time_stats.
    print('\nWHAT WAS THE TOTAL TRAVEL TIME AND THE AVERAGE TRAVEL TIME IN THIS QUERY?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']

    #To get sum for total trip time, and mean for avg trip time.
    total_ride_time = np.sum(df['Travel Time'])
    print("\nBased on your query, the total travel time was: {}".format(total_ride_time))

    avg_ride_time = np.mean(df['Travel Time'])
    print("Based on your query, the average travel time was: {}".format(avg_ride_time))

    return total_ride_time, avg_ride_time

def bike_users(df):
    #To get the counts of each user type.
    #To get the dataframes returned from time_stats.
    print('\nHOW MANY WERE THERE OF EACH TYPE OF USER?\n')
    return df['User Type'].value_counts()

def gender_data(df):
    #To get What are the counts of each gender.
    #To get the dataframes returned from time_stats.
    try:
        print('\nHOW MANY USERS WERE THERE OF EACH GENDER?\n')
        return df['Gender'].value_counts()
    except:
        print('Sorry, there was no gender data for this city.')

def birth_years(df):
    #To get the earliest, most recent, and most common year of birth.
    #To get the dataframes returned from time_stats.
    try:
        print('\nWHAT WAS THE EARLIEST, THE MOST RECENT, AND THE MOST COMMON YEAR OF BIRTH?')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest))
        latest = np.max(df['Birth Year'])
        print ("The most recent year of birth is " + str(latest))
        most_frequent= df['Birth Year'].mode()[0]
        print ("The most common year of birth is " + str(most_frequent))
        return earliest, latest, most_frequent
    except:
        print('Sorry, there was no birth year data for this city.')

def compute_time(f, df):
    #To calculate the time it takes to process each stat.
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("This took %s seconds." % (time.time() - start_time))

def disp_raw_data(df): #To display all raw data according to criteria inputted by the user.
    df = df.drop(['month', 'day_of_month'], axis = 1)
    row_index = 0

    see_data = input("We have some raw data to show you. Would you like to see? Type 'yes' or 'no': \n").lower()
    while True:
        if see_data == 'no':
            return
        if see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input("\nWould you like to see five more rows of raw data? Type 'yes' or 'no': \n").lower()

def main(): #To process and print all data as dictated by the user's input.
    #To call all functions at once.
    city = input_city()
    df = load_data(city)
    period = input_time()
    month = month_choice(period)
    day = day_info(period)
    month_day = month_day_choice(df, period)

    df = time_stats(df, period, month, day, month_day)
    disp_raw_data(df)

    print("\nAlright! And here are some other fascinating facts related to your query:")

    #To list up all items to be printed out according to user criteria.
    stats_funcs_list = [month_freq, day_freq, hour_freq,
                        stations_freq, common_trip,
                        ride_duration,
                        bike_users, gender_data, birth_years]

    for x in stats_funcs_list: #To call function that prints out all data related to user criteria.
        compute_time(x, df)

    #To ask the user for another city input.
    restart = input("\nNow you have a good idea. Would you like analyze another city? Type 'yes' or 'no': \n")
    if restart.lower() == 'yes' or restart.lower() == "y":
        main()

if __name__ == '__main__':
    main()
