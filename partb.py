# import relevant libraries

import csv
import time
import calendar
from exceptions import MyException as MyException

# Function to convert epoch time to date timestamp

def epoch_to_date(timestamp):
    dt = time.gmtime(timestamp)
    date_string = time.strftime('%d/%m/%Y', dt)
    return date_string


# from date to epoch
def date_to_epoch(epoch):
    timestamp = calendar.timegm(time.strptime(epoch, "%d/%m/%Y"))
    return timestamp


# Function that checks if the date given is matching the expected date format
def check_date_format(date):
    try:
        # Try to convert it, if the string is in incorrect format it will raise an exception
        timestamp = calendar.timegm(time.strptime(str(date), "%d/%m/%Y"))
    except Exception as ex:
        # If exception was raised, raise MyException with the corresponding value
        raise MyException("Error: invalid date value")


# Define start and end date for the data
min_start_date = date_to_epoch('28/04/2015')
max_end_date = date_to_epoch('18/10/2020')


# Function that checks if the provided start and end dates are in correct format, within the given ranges and that if
# end date is after start date
def check_validity(start_date, end_date):
    try:
        # Check if both start and end date were given in the right format
        check_date_format(start_date)
        check_date_format(end_date)
    except Exception as ex:
        # If any of the check_date_format function calls raised an exception, raise another exception with the message
        # from the original exception
        raise MyException(ex.args[0])
    else:
        # If no exceptions were raised check if the given dates are within the range and if end date is after start date
        try:
            # Convert both dates into timestamp
            start_d = date_to_epoch(start_date)
            end_d = date_to_epoch(end_date)

            # Check if the start date is on or after min_start_date AND if the end date is on or before the max_end_date
            if start_d <= min_start_date or end_d >= max_end_date:
                # If it's not raise exception
                raise MyException("Error: date value is out of range")
            # Check if the end date comes after start date
            elif end_d < start_d:
                # If it's not raise exception
                raise MyException("Error: end date must be larger than start date")
        except Exception as ex:
            # Raise exception if any exception was raised
            raise MyException(ex.args[0])


"""
    Part A
    Please provide definitions for the following functions
"""


# highest_price(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def highest_price(data, start_date, end_date):
    try:
        # Check whether provided start and end date are meeting given criteria
        check_validity(start_date, end_date)
    except Exception as ex:
        # If they are not, an exception was raised - print error to the user
        print(ex)
    else:
        # If no exception were raised, perform calculations
        high_list = []
        start_d = date_to_epoch(start_date)
        end_d = date_to_epoch(end_date)
        try:
            for row in data:
                if start_d <= int(row['time']) <= end_d:
                    high_list.append(float(row['high']))
        except KeyError:
            print("Error: requested column is missing from dataset")
        else:
            return max(high_list)


# lowest_price(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def lowest_price(data, start_date, end_date):
    try:
        # Check whether provided start and end date are meeting given criteria
        check_validity(start_date, end_date)
    except Exception as ex:
        # If they are not, an exception was raised - print error to the user
        print(ex)
    else:
        # If no exception were raised, perform calculations
        low_list = []

        start_d = date_to_epoch(start_date)
        end_d = date_to_epoch(end_date)

        try:
            for row in data:
                if start_d <= int(row['time']) <= end_d:
                    low_list.append(float(row['low']))
        except KeyError:
            print("Error: requested column is missing from dataset")
        # result=("highest price between {} and {} is {}".format(start_date,end_date,float(max(high_list))))
        else:
            # replace None with an appropriate return value
            # return print("highest price between {} and {} is {}".format(start_date, end_date, float(max(high_list))))
            return min(low_list)


# max_volume(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def max_volume(data, start_date, end_date):
    try:
        # Check whether provided start and end date are meeting given criteria
        check_validity(start_date, end_date)
    except Exception as ex:
        # If they are not, an exception was raised - print error to the user
        print(ex)
    else:
        # If no exception were raised, perform calculations
        volume_list = []
        start_d = date_to_epoch(start_date)
        end_d = date_to_epoch(end_date)

        try:
            for row in data:
                if start_d <= int(row['time']) <= end_d:
                    volume_list.append(float(row['volumefrom']))
        except KeyError:
            print("Error: requested column is missing from dataset")
        else:
            return max(volume_list)


# best_avg_value(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def best_avg_value(data, start_date, end_date):
    try:
        # Check whether provided start and end date are meeting given criteria
        check_validity(start_date, end_date)
    except Exception as ex:
        # If they are not, an exception was raised - print error to the user
        print(ex)
    else:
        # If no exception were raised, perform calculations
        avg_list = []
        start_d = date_to_epoch(start_date)
        end_d = date_to_epoch(end_date)
        try:
            if start_d == end_d:
                items = list(filter(lambda i: int(i['time']) == start_d, data))

                if len(items) == 1:
                    item = items[0]
                    return float(item['volumeto']) / float(item['volumefrom'])

            for row in data:
                if start_d <= int(row['time']) <= end_d:
                    avg_list.append(float(row['volumeto']) / float(row['volumefrom']))
        except KeyError:
            print("Error: requested column is missing from dataset")
        else:
            # replace None with an appropriate return value
            return max(avg_list)


# 0. Create two variables, number_of_entries and sum and assign both of them to 0.
# 1. Iterate through all data between start_date and end_date
# 2. Take each value that satisfies date condition, and call the best_avg_value function for that date
# 3. Add return value of best_avg_value function call to the sum and increment number_of_entries by 1
# 4. Once loop has finished return sum / number_of_entries


# moving_average(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def moving_average(data, start_date, end_date):
    try:
        # Check whether provided start and end date are meeting given criteria
        check_validity(start_date, end_date)
    except Exception as ex:
        # If they are not, an exception was raised - print error to the user
        print(ex)
    else:
        # If no exception were raised, perform calculations
        start_d = date_to_epoch(start_date)
        end_d = date_to_epoch(end_date)
        result = 0
        number_of_entries = 0

        for row in data:
            if start_d <= int(row['time']) <= end_d:
                result += best_avg_value(data, epoch_to_date(int(row['time'])), epoch_to_date(int(row['time'])))
                number_of_entries += 1
        # replace None with an appropriate return value
        return round(result / number_of_entries, 2)


# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program

    # Example variable initialization
    # data is always the cryptocompare_btc.csv read in using a DictReader

    data = []
#this is an extra exception for cases when the user meses with the dataset columns instead of just the functions
    try:
        f = open("cryptocompare_btc.csv", "r")
        headings = ['time', 'high', 'low', 'open', 'close', 'volumefrom', 'volumeto']
        sorted(headings)
        first_line_of_file = f.readline().replace('\n', '').split(',')
        sorted(first_line_of_file)
        f.seek(0)

        if not ",".join(headings) == ",".join(first_line_of_file):
            raise MyException("Error: requested column is missing from dataset")

    # first_line_of_file = take the firtst line from CSV
    # headings_file = first_line_of_file.replace('\n', '').split(',')
    except Exception as ex:
        if ex.args[0] == 2:
            print("Error: dataset not found")
        else:
            print(ex)
    else:
        reader = csv.DictReader(f)
        data = [r for r in reader]

        # access individual rows from data using list indices
        first_row = data[0]
        # to access row values, use relevant column heading in csv
        print(f"timestamp = {first_row['time']}")
        print(f"daily high = {first_row['high']}")
        print(f"volume in BTC = {first_row['volumefrom']}")


        # check results
        print("highest price between {} and {} is\n{}".format('01/01/2016', '31/01/2016',
                                                              highest_price(data, '01/01/2016', '31/01/2016')))
        print(str(highest_price(data, '01/02/2016', '28/02/2016')))
        print(highest_price(data, '01/01/2016', '31/12/2015'))

        print(lowest_price(data, '01/01/2016', '31/01/2016'))
        print(lowest_price(data, '01/02/2016', '28/02/2016'))
        print(lowest_price(data, '01/12/2016', '31/12/2016'))

        print(max_volume(data, '01/01/2016', '31/01/2016'))
        print(max_volume(data, '01/02/2016', '28/02/2016'))
        print(max_volume(data, '01/12/2016', '31/12/2016'))

        print(best_avg_value(data, '01/01/2016', '31/01/2016'))
        print(best_avg_value(data, '01/02/2016', '28/02/2016'))
        print(best_avg_value(data, '01/12/2016', '31/12/2016'))

        print(moving_average(data, '01/01/2016', '31/01/2016'))
        print(moving_average(data, '01/02/2017', '28/02/2016'))
        print(moving_average(data, '01/01/2015', '01/05/2015'))

    pass
