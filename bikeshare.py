import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def is_month(month):
    """判断输入是否是月份"""
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    while True:
        if month not in months: # 如果输入的月份不在months列表中，一直循环
            month = input('Please type out the correct month:\n').lower()
        else:
            break

    return month


def is_day(day):
    """判断输入是否是星期"""
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    while True:
        if day not in days: # 如果输入的星期不在days列表中，一直循环
            day = input('Please type out the correct day:\n').lower()
        else:
            break

    return day


def is_filter_condition(filter_condition):
    """判断输入是否是筛选条件"""
    conditions = ('month', 'day', 'both', 'none')

    while True:
        if filter_condition in conditions:
            break
        else:
            filter_condition = user_input('filter_condition')

    return filter_condition


def get_month_and_day(filter_condition):
    """
    根据filter_condition筛选月份和星期

    Returns:
        (str) month - 输入的月份
        (str) day - 输入的星期
    """

    month = ''
    day = ''

    if filter_condition in ['month', 'both']: # month，将用户输入的月份值赋给month
        # 获取用户输入的月份
        month = user_input('month')
        month = is_month(month)
    if filter_condition in ['day', 'both']: # day，将用户输入的星期几值赋给day
        # 获取用户输入的星期几
        day = user_input('day')
        day = is_day(day)

    return month, day


def user_input(input_type):
    """根据输入类型返回filter_condition、month、day"""
    if input_type == 'filter_condition':
        return input('Would you like to filter the date by month, day, both, or not at all? Type "none" for no time filter.\n').lower()
    elif input_type == 'month':
        return input('Which month? January, February, March, April, May or June?\n').lower()
    elif input_type == 'day':
        return input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n').lower()


def clean_data(df):
    """
    清洗数据
    washington.csv没有'Birth Year'和'Gender'这两列数据
    washington.csv中的'Trip Duration'列的数据类型是float64，
    将其替换成和其他两个城市相同的int64类型
    """
    # 替换NaN
    df['User Type'] = df['User Type'].fillna(method = 'ffill', axis = 0)
    # washington没有'Birth Year'和'Gender'列
    if 'Birth Year' and 'Gender' in df:
        # 用'Birth Year'的平均值替换NaN
        df['Birth Year'] = df['Birth Year'].fillna(df['Birth Year'].mean())
        # 将原本'Birth Year'float64的类型替换int64
        df['Birth Year'] = df['Birth Year'].astype(np.int64)
        # 利用向前填充替换'Birth Year'的NaN
        df['Gender'] = df['Gender'].fillna(method = 'ffill', axis = 0)
    else:
        # 将washington的'Trip Duration'列的float64替换成int64
        df['Trip Duration'] = df['Trip Duration'].astype(np.int64)

    return df


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        # 获取用户输入的city
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        # 判断是否是这三个城市
        # 不是的话返回循环
        if city not in CITY_DATA.keys():
            continue

        # 获取筛选数据条件
        filter_condition = is_filter_condition(user_input('filter_condition'))

        # 获取月份和星期
        month, day = get_month_and_day(filter_condition)
        # 获取到正确的月份和星期后，直接退出while循环
        break

    print('-'*40)
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
    # 加载city数据
    df = pd.read_csv(CITY_DATA[city])

    # 将Start Time列转换成datetime数据类型
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # 添加月份列
    df['Month'] = df['Start Time'].dt.month_name()
    # 添加星期几列
    df['DayOfWeek'] = df['Start Time'].dt.day_name()

    # 筛选月数据
    if month:
        df = df[df['Month'] == month.title()]
    # 筛选日数据
    if day:
        df = df[df['DayOfWeek'] == day.title()]

    # 清洗数据
    df = clean_data(df)

    return df


def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (str) month - 如果用户根据月份查询数据，则不需要返回the most popular month
        (str) day - 如果用户根据星期查询数据，则不需要返回the most popular day
        df - 筛选后的city数据
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if not month: # month有值，说明用户是以month作为筛选条件
        top_month = df['Month'].mode()[0]
        print('What was the most popular month for traveling?\n', top_month)

    if not day: # day有值，说明用户是以day作为筛选条件
        top_day = df['DayOfWeek'].mode()[0]
        print('What was the most popular day for traveling?\n', top_day)

    top_hour = df['Start Time'].dt.hour.mode()[0]
    print('What was the most popular time for taveling?\n', top_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    top_start = df['Start Station'].mode()[0]
    print('What was the most popular start station?\n', top_start)
    print('Total: %d times' % df['Start Station'].value_counts().max())

    top_end = df['End Station'].mode()[0]
    print('What was the most popular end station?\n', top_end)
    print('Total: %d times' % df['End Station'].value_counts().max())

    # 根据'Start Station'和'End Station'
    # 筛选最热门的骑行行程
    top_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    start_station = top_trip[0]
    end_station = top_trip[1]
    print('What was the most popular trip from start to end?')
    print('Start Station: {}\nEnd Station: {}'.format(top_trip[0], top_trip[1]))
    print('Total: %d times' % df.groupby(['Start Station', 'End Station']).size().max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # 将得到的秒转换成年年时分秒
    total_trip = pd.Timedelta(seconds = df['Trip Duration'].sum())
    print('What was the total traveling time?\n', total_trip)

    # display mean travel time
    # 将得到的秒转换成年时分秒
    mean_trip = pd.Timedelta(seconds = df['Trip Duration'].mean())
    print('What was the average traveling time?\n', mean_trip)

    # 最短行程
    shortest_trip = pd.Timedelta(seconds = df['Trip Duration'].min())
    print('What was the shortest traveling time?\n', shortest_trip)
    # 最长行程
    longest_trip = pd.Timedelta(seconds = df['Trip Duration'].max())
    print('What was the longest traveling time?\n', longest_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('What is the breakdown of users?')
    user_type_count = df['User Type'].value_counts()
    print(user_type_count)

    # Display counts of gender
    # 判断'Gender'在不在df中
    print('What is the breakdown of gender?')
    if 'Gender' in df:
        print(df['Gender'].value_counts())
    else:
        print('Washington has no gender data to share.')

    # Display earliest, most recent, and most common year of birth
    # 判断'Birth Year'在不在df中
    print('What is the breakdown of year of birth?')
    if 'Birth Year' in df:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        popular = df['Birth Year'].mode()[0]
        print('Youngest: ', youngest)
        print('Oldest: ', oldest)
        print('Popular: ', popular)
    else:
        print('Washington has no year of birth data to share.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nType any key to exit or type "y" to restart\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
