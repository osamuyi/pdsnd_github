import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS_DICT = {'JANUARY': '1', "FEBRUARY": "2", 'MARCH': '3', 'APRIL': '4', 'MAY': '5',
                    'JUNE': '6', 'ALL': 'ALL'}

INDEX_OF_MONTH = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                  6: 'June'}

DAY_DICT = {'MONDAY': 0, 'TUESDAY': 1, 'WEDNESDAY': 2, 'THURSDAY': 3, 'FRIDAY': 4, 'SATURDAY': 5,
                'SUNDAY': 6, 'ALL': "ALL"}

INDEX_OF_DAY = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("Press Ctrl + c if you want to exit at any moment!!!!")

    city_found, month_found, day_found = False, False, False

    while True:

        # Enter input from user for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        if not city_found:
            city = input("There are 3 cities for exploration : Chicago, Washington, New York City. Please choose "
                         "one : ")
            city = city.lower()
            if city not in CITY_DATA:
                print("Invalid city or data not available, please choose one of the 3 cities: Chicago, Washington, New York City")
                continue
            else:
                city_found = True

        print('\n')

        # Enter input from user for month (all, january, february, ... , june)
        if not month_found:
            month = input("Choose the month you want to explore : "
                          "JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, ALL : ")
            month = month.upper()
            if month not in MONTHS_DICT:
                print("Invalid month entered!!! Enter a valid month!!!")
                continue
            else:
                month_found = True

        print('\n')

        # Enter input from user for day of week (all, monday, tuesday, ... sunday)
        day = input("Choose the day you want to explore : MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY, ALL: ")
        day = day.upper()
        if day not in DAY_DICT:
            print("Invalid day entered!!! Enter a valid day!!!")
            continue
        else:
            break

    print('-' * 40)
    print('\n')
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()
    print("ANALYZING DATA!!!")

    df = pd.read_csv(CITY_DATA.get(city))

    # extract start month from the Start time column to create Start Month column
    df['Start Month'] = pd.DatetimeIndex(df['Start Time']).month

    # extract start day from the Start time column to create Start Day column
    df['Start Day'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S').dt.dayofweek

    # extract start hour from the Start Time column to create an Start Hour column
    df['Start Hour'] = pd.DatetimeIndex(df['Start Time']).hour

    # filter on month, if month is specified
    if month != MONTHS_DICT.get('ALL'):
        df = df[df['Start Month'] == int(MONTHS_DICT.get(month))]

    # filter on day, if day is specified
    if day != DAY_DICT.get('ALL'):
        df = df[df['Start Day'] == int(DAY_DICT.get(day))]

    print("\nThis took %s seconds." % (time.time() - start_time))
    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # show the most common month
    if month == MONTHS_DICT.get('ALL'):
        common_month = df['Start Month'].dropna()
        if common_month.empty:
            print("No common month found for the filter specified!! Please adjust your filter!!")
        else:
            common_month = common_month.mode()[0]
            print('Most common month for renting is : {}'.format(INDEX_OF_MONTH.get(common_month)))
    else:
        print('As you have chosen month : {} as filter, most common month for renting won\'t be calculated'.format(month))

    # show the most common day of week
    if day == DAY_DICT.get('ALL'):
        common_day = df['Start Day'].dropna()  #.mode()[0]
        if common_day.empty:
            print('No common day found for the filters chosen!! Please adjust your filter!!!')
        else:
            common_day = common_day.mode()[0]
            print('Most popular day for renting is : {}'.format(INDEX_OF_DAY.get(common_day)))
    else:
        print('As you have chosen "{}day" as filter, most common day for renting won\'t be calculated'.format(day.title()))

    # show the most common start hour
    common_start_hour = df['Start Hour'].dropna()
    if common_start_hour.empty:
        print('No common start hour found for the filter chosen!! Please adjust your filter !!!')
    else:
        common_start_hour = common_start_hour.mode()[0]
        print('Most common renting start hour is : {}:00 hrs'.format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # show most commonly used start station
    most_common_start_station = df['Start Station']
    if most_common_start_station.empty:
        print('No \'Start Station\' data found for the filter chosen!! Kindly adjust your filter')
    else:
        most_common_start_station = most_common_start_station.mode()[0]
        print('Most common start station for the filter chosen is : {}'.format(most_common_start_station))

    # show most commonly used end station
    most_common_end_station = df['End Station']
    if most_common_end_station.empty:
        print('No \'End Station\' data found for the filter chosen!! Kindly adjust your filter')
    else:
        most_common_end_station = most_common_end_station.mode()[0]
        print('Most common end station for the filter chosen is : {}'.format(most_common_end_station))

    # show most frequent combination of start station and end station trip
    most_common_start_and_end_station = df[['Start Station', 'End Station']].dropna()
    if most_common_start_and_end_station.empty:
        print('No data found for the filter chosen!! Kindly adjust your filter')
    else:
        most_common_start_and_end_station = most_common_start_and_end_station.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
        trip_count = most_common_start_and_end_station.iloc[0]
        stations = most_common_start_and_end_station[most_common_start_and_end_station == trip_count].index[0]

        start_station, end_station = stations
        print('Most common start station : {} and end station {} which was part of trips {} times'.format(start_station, end_station, trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # show total travel time
    valid_time = df['Trip Duration'].dropna()
    if valid_time.empty:
        print('No data found!! Please adjust your filter')
    else:
        total_time = valid_time.sum()
        print('Total travel time in seconds is : {}'.format(total_time))

        # show mean travel time
        mean_travel_time = valid_time.mean()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # show counts of user types
    user_type = df['User Type'].dropna()

    if user_type.empty:
        print('No data available for chosen filter, please adjust your filter!!')
    else:
        user_type = user_type.value_counts()
        print('User type details for the filter chosen : {}'.format(user_type))

    # show counts of gender
        if 'Gender' in df:
            user_gender = df['Gender'].dropna()
            if user_gender.empty:
                print('No data available for chosen filter, please adjust your filter!!')
            else:
                user_gender = user_gender.value_counts()
                print('User gender count : {}'.format(user_gender))

    # show earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_years = df['Birth Year'].dropna()
        if birth_years.empty:
            print('No data available for chosen filter, please adjust your filter!!')
        else:
            user_birth_year = df['Birth Year'].dropna()
            if user_birth_year.empty:
                print('No data available for your chosen filter, please adjust your filter!!!')
            else:
                oldest_user = user_birth_year.min()
                print('Earliest year of birth for the chosen filter : {}'.format(int(oldest_user)))

                youngest_user = user_birth_year.max()
                print('Most recent year of birth for the chosen filter : {}'.format(int(youngest_user)))

                most_common_year_of_birth = user_birth_year.mode()[0]
                print('Most popular year of birth for the chosen filter : {}'.format(int(most_common_year_of_birth)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def show_raw_data(df):
    '''method to print the selected data frame, 5 at a time '''
    choice = input("Would you like to see raw data? [y/n] : ")
    choice = choice.lower()

    count = 0
    if choice == 'Y':
        for row in df.iterrows():
            print(row)
            count += 1
            if count != 0 and count % 5 == 0:
                choice = input("Would you like to see raw data? [y/n] : ")
                if choice.lower() != 'y':
                    break

def main():
    while True:
        city, month, day = get_filters()
        print("Details of inputs: City : {}, Month : {}, Day : {}".format(city, month, day))

        df = load_data(city, month, day)

        if df.empty:
            print('No data found for specified filter, please adjust your filters!!!')
            continue

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
