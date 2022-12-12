import time
import pandas as pd
import numpy as np

#---------------------------------------------------------------------------------------------------------------------

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#---------------------------------------------------------------------------------------------------------------------

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('Would you like to see data for which city? please enter your choice as: chicago, new york city or washington? ').lower()
        if city in ('chicago', 'new york city' , 'washington'):
            break
        else:
            print('Sorry, invalid input. Try again please')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to fillter by? please enter your choice as: january, february, march, april, may, june or type 'all' if you don't want a specific month ").lower()
        if month in ('january', 'february', 'march', 'april', 'may', 'june','all'):
            break
        else:
            print('Sorry, invalid input. Try again please')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day= input("Which day would you like to fillyer by? please enter your choice as: sunday, monday, tuesday, wednesday, thursday, friday, saturday or type 'all' if you don't want a specific day ").lower()
        if day in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            break
        else:
            print('Sorry, invalid input. Try again please')

    print('-'*40)
    return city, month, day

#---------------------------------------------------------------------------------------------------------------------

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day and hour of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


#---------------------------------------------------------------------------------------------------------------------

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month=df['month'].mode()[0]
    print('\nThe most common month is: {}'.format(months[common_month-1]))

    # display the most common day of week
    print('\nThe most common day is: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('\nThe most common hour is: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


#---------------------------------------------------------------------------------------------------------------------

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most commonly used start station is: {} '.format(df['Start Station'].value_counts().idxmax()))

    # display most commonly used end station
    print('The most commonly used end station is: {}'.format(df['End Station'].value_counts().idxmax()))

    # display most frequent combination of start station and end station trip
    df['combination stations']= df['Start Station'] +" AND "+ df['End Station']
    print('The most frequent combination of start station and end station trip are: {}'.format(df['combination stations'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#---------------------------------------------------------------------------------------------------------------------

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_seconds = df['Trip Duration'].sum()
    print('The total travel time is: {} days'.format(total_seconds/86400))


    # display mean travel time
    mean_seconds = df['Trip Duration'].mean()
    print('The avrage of travel time is: {} hours'.format(mean_seconds/60))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#---------------------------------------------------------------------------------------------------------------------

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The user types are:\n\n{} '.format(df['User Type'].value_counts()))

    # Display counts of gender
    print('The counts of gender are:\n\n')
    try:
        print(df['Gender'].value_counts())
    except KeyError:
        print("\nSorry, no data available for this month.")

    # Display earliest, most recent, and most common year of birth

    print('\nThe earlist year of birth is: ')
    try:
        earliset_birth = df['Birth Year'].min()
        print(earliset_birth)
    except KeyError:
       print("\nSorry, no data available for this month.")

    print('\nThe most recent year of birth is: ')
    try:
        recent_birth = df['Birth Year'].max()
        print(recent_birth)
    except KeyError:
        print("\nSorry, no data available for this month.")

    print('\nThe most common year of birth is: ')
    try:
        common_birth = df['Birth Year'].mode()[0]
        print(common_birth)
    except KeyError:
        print("\nSorry, no data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#---------------------------------------------------------------------------------------------------------------------

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_data= input("would you like to view individual trip data? Type 'yes' or 'no'").lower()

        if raw_data == 'yes':
            num = 0
            print("Type 'no' for stop")
            while (raw_data != 'no'):
                num= num+5
                print(df.head(num))

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

#---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	main()
