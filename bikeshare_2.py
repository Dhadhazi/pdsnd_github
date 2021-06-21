import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def ask_for_data(question, dataset, all_data=False):
    """ Gets any question input for the user, and only returns if it's in the dataset """
    answer = ""
    while answer not in dataset:
        answer = input(question).lower()
        if all_data and answer == "all":
            break
        if answer not in dataset:
            print("That is not a valid answer, please try again!")

    return answer


def data_divider():
    print("\n")
    print('-_' * 20)
    print("\n")


def runtime_calculator(func, data):
    print('\nCalculating statistics...\n')
    start_time = time.time()
    func(data)
    print(f"\nThis took {time.time() - start_time} seconds.")


def stat_function_display(func, data):
    runtime_calculator(func, data)
    data_divider()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    city = ask_for_data('Which city get the data from? (Chicago, New York, or Washington) \n', CITY_DATA)
    month = ask_for_data('Which months you would like to have the data? (Enter a month from January to June, '
                         'or all for all the month s) \n', months, True)
    day = ask_for_data("Which dat of the week would you like data from? (Name a day or enter all for all days) \n",
                       days, True)
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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    month = df['Month'].mode()[0]
    day = df['Day of Week'].mode()[0]
    hour = df['Hour'].mode()[0]
    print(
        f'Most frequent month:  {month}.\n'
        f'Most frequent day: {day}.\n'
        f'Most frequent hour: {hour}.')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    start_station = df['Start Station'].mode()[0]
    end_station = df['End Station'].mode()[0]

    df['Start and End Stations'] = df['Start Station'] + '-' + df['End Station']
    start_end_station = df['Start and End Stations'].mode()[0]

    print(
        f'Most popular start station: {start_station}.\n'
        f'Most popular end station: {end_station}.\n'
        f'The most common trip was {start_end_station}.')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    total_time = df['Trip Duration'].sum()
    mean_time = df['Trip Duration'].mean()

    print(f'The total time for all trips was: {round(total_time / 3600, 2)} hours.\n'
          f'The average length of each trip was: {round(mean_time / 60, 2)} minutes.')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    gender_count = earliest_year = latest_year = common_year = 'is not available for this city\'s data.'

    if 'Gender' in df:
        gender_count = df['Gender'].value_counts().to_string()

    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        latest_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])

    print(
        f'The gender distribution of riders: \n {gender_count}\n'
        f'The earliest birth year is: {earliest_year}.\n'
        f'The latest birth year is: {latest_year}.\n'
        f'The most common birth year is {common_year}')


def data_reader(df):
    """Displays data if user does not type no"""
    row_counter = 0

    print(f"Would you like to view individual trip data? "
          f"(press enter to show data, type 'no' to stop displaying new data) ")
    x = 0
    while input().lower() != 'no':
        print(df.iloc[row_counter:row_counter+5].to_string())
        print("\n")
        row_counter += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        data_divider()

        stat_func_list = [time_stats, station_stats, trip_duration_stats, user_stats]

        for stat_func in stat_func_list:
            stat_function_display(stat_func, df)

        data_reader(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()