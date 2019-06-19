"""
This script provides descriptive statistics about data related to bike share systems for Chicago, New York City, and Washington, in an 
interactive way with the user.
The data provided by Motivate has been wrangled by Udacity team.
"""
import numpy as np
import pandas as pd
import time

city_data = {'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv'}

def get_filters():
	"""
	Asks user to specify a city, month, and day to analyse.
	Returns:
		(str) city - name of the city to analyse
		(str) month - name of the month to filter by, or "all" to apply no month filter	
		(str) day - name of the day of week to filter by, or "all" to apply no day filter
	"""	
	while True:
		try:
			city = input("Hello! Let´s explore some US bikeshare data!\nWould you like to see data for Chicago, New York, or Washington? ").lower()
			while city != 'chicago' and city != 'new york' and city != 'washington':
				city = input("That's not a valid option. You must choose among Chicago, New York, and Washington. Please try again. ").lower()
			print("You have chosen to see the data for: {}.\n".format(city.title()))
			filt = input('Would you like to filter the data by month, day, or not at all? Type "none" for no time filter. ').lower()	
			while filt != 'month' and filt != 'day' and filt != 'none':
				filt = input("That´s not a valid option. You must choose among month, day, or 'none'. Please try again. ").lower()			
			if filt == 'month':
				day = 'all'
				month = input('Which month? January, February, March, April, May, or June? ').title()
				while month != 'January' and month != 'February' and month != 'March' and month != 'April' and month != 'May' and month != 'June':
					month = input('It looks like you have not chosen the month correctly. Please type the month again. ').title()
				print("You have chosen to filter the data by: {}. Let's see the statistics!\n".format(month))
			elif filt == 'day':
				month = 'all'
				day = input('Which day? Mon, Tue, Wed, Thu, Fri, Sat, or Sun? ').title()
				while day != 'Mon' and day != 'Tue' and day != 'Wed' and day != 'Thu' and day != 'Fri' and day != 'Sat' and day != 'Sun':
					day = input('It looks like you have not chosen the day correctly. Please type the day again using three letters. ').title()
				print("You have chosen to filter the data by: {}. Let's see the statistics!\n".format(day))
			else:
				day = 'all'
				month = 'all'
				print("You have chosen no filter. Let´s see the statistics!\n")
			break		
		except KeyboardInterrupt:
			print('\nNo input taken\n')
			break
		except Exception as e:
			print("Unexpected error: {}\n".format(e))
		finally:
			print('-'*40)	
	return city, month, day

def load_data(city, month, day):
	"""
	Loads data for the specified city and filters by month and day if applicable.
	Args:
		(str) city - name of the city to analyse
		(str) month - name of the month to filter by, or "all" to apply no month filter
		(str) day - name of the day of week to filter by, or "all" to apply no day filter
	Returns:
		df - Pandas DataFrame containing city data filtered by month and day
	"""
	df = pd.read_csv(city_data[city])
	df['Start Time'] = pd.to_datetime(df['Start Time'])
	df['month'] = df['Start Time'].dt.month
	df['day_of_week'] = df['Start Time'].dt.weekday_name
	
	# filter by month if applicable
	if month != 'all':
		months = ['January', 'February', 'March', 'April', 'May', 'June']
		month = months.index(month)+1
		df = df[df['month'] == month]
	
	# filter by day of week if applicable
	if day != 'all':
		days = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
		day = days.get('day')
		df = df[df['day_of_week'] == day]
	
	return df
	
def time_stats(df):
	"""Displays statistics on the most frequent times of travel."""
	try:
		print('\nCalculating the most frequent times of travel...\n') 
		start_time = time.time()
		
		print('Most frequent month: ', df['month'].mode()[0])
		print('Most frequent day of week: ', df['day_of_week'].mode()[0])
		df['hour'] = df['Start Time'].dt.hour
		print('Most frequent start hour: ', df['hour'].mode()[0])
		
		print("\nThis took %s seconds." % (time.time() - start_time))
		print('\n')
	except Exception as e:
		print("Unexpected error: {}\n".format(e))
	finally:
		print('-'*40)

def trip_duration_stats(df):
	"""Displays statistics on the total, average and maximum trip duration."""
	try:
		print('\nCalculating trip duration...\n')
		start_time = time.time()
		
		print('Total travel time: {} seconds'.format(np.sum(df['Trip Duration'])))
		print('Mean travel time: {} seconds'.format(np.mean(df['Trip Duration'])))
		print('Maximum travel time: {} seconds'.format(np.max(df['Trip Duration'])))
		
		print("\nThis took %s seconds." % (time.time() - start_time))
		print('\n')
	except Exception as e:
		print("Unexpected error: {}\n".format(e))
	finally:
		print('-'*40)

def station_stats(df):
	"""Displays statistics on the most popular stations and trip."""
	try:
		print('\nCalculating the most popular stations and trip...\n')
		start_time = time.time()
		
		print('Most frequent start station:\n    ', df['Start Station'].mode()[0])
		print('Most frequent end station:\n    ', df['End Station'].mode()[0])
		df['combined_station'] = df['Start Station'] + ' - ' + df['End Station']
		print('Most frequent combination of start station and end station trip:\n    ', df['combined_station'].mode()[0])
		
		print("\nThis took %s seconds." % (time.time() - start_time))
		print('\n')
	except Exception as e:
		print("Unexpected error: {}\n".format(e))
	finally:
		print('-'*40)

def user_stats(df):
	"""Displays statistics on bikshare users."""
	try:
		print('\nCalculating user statistics...\n')
		start_time = time.time()
		
		print('Counts of user types:\n{}'.format(df['User Type'].value_counts()))
		if 'Gender' in df:
			print('\nCounts of user gender:\n{}'.format(df['Gender'].value_counts()))
			print('\nEarliest year of birth: {}'.format(np.min(df['Birth Year'])))
		else:
			print('Gender data not present in bike dataset!')
		if 'Birth Year' in df:
			print('Most recent year of birth: {}'.format(np.max(df['Birth Year'])))
			print('Most frequent year of birth: {}'.format(df['Birth Year'].mode()[0]))
		else:
			print('Birth Year data not present in bike dataset!')
		
		print("\nThis took %s seconds." % (time.time() - start_time))
		print('\n')
	except Exception as e:
		print("Unexpected error: {}\n".format(e))
	finally:
		print('-'*40)

def raw_data():
	record_counter = 0
	while True:
		choice = input('\nWould you like to see 5 consecutive data records? Please type yes or no.\n').lower()
		if choice == 'yes':
			print(df.iloc[record_counter:record_counter+5])
			record_counter += 5
			continue
		else:
			break
		restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
		if restart != 'yes':
			break
		
def main():
	while True:
		city, month, day = get_filters()
		df = load_data(city, month, day)
		
		time_stats(df)
		trip_duration_stats(df)
		station_stats(df)
		user_stats(df)
		
		raw_data()


if __name__ == "__main__":
	main()
	