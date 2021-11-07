import csv
import time
import calendar
from exceptions import MyException as MyException

"""
    Part C
    Please provide definitions for the following functions
"""


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
            if start_d < min_start_date or end_d > max_end_date:
                # If it's not raise exception
                raise MyException("Error: date value is out of range")
            # Check if the end date comes after start date
            elif end_d < start_d:
                # If it's not raise exception
                raise MyException("Error: end date must be larger than start date")
        except Exception as ex:
            # Raise exception if any exception was raised
            raise MyException(ex.args[0])


# moving_avg_short(data, start_date, end_date) -> dict
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def moving_avg_short(data, start_date, end_date):
    try:
        check_validity(start_date, end_date)
    except Exception as ex:
        print(ex)
    else:
        start_d = date_to_epoch(start_date)
        end_d = date_to_epoch(end_date)
        results = dict()
#make an indexing system with enumerate function and account for the special cases of the first 2 days. If its the first day take that day
        #if it is the second day take day 1 twice and if its from the third day and after just take (n-2)+(n-1)+n/3

        for row in enumerate(data):
            if start_d <= int(row[1]['time']) <= end_d:
                if row[0] == 0:
                    results[epoch_to_date(int(row[1]['time']))] = float(row[1]['volumeto']) / float(row[1]['volumefrom'])
                elif row[0] == 1:
                    avg_1 = float(data[0]['volumeto']) / float(data[0]['volumefrom'])
                    avg_2 = float(data[1]['volumeto']) / float(data[1]['volumefrom'])
                    results[epoch_to_date(int(row[1]['time']))] = (avg_1 + avg_1 + avg_2) / 3
                else:
                    avg_1 = float(data[row[0] - 2]['volumeto']) / float(data[row[0] - 2]['volumefrom'])
                    avg_2 = float(data[row[0] - 1]['volumeto']) / float(data[row[0] - 1]['volumefrom'])
                    avg_3 = float(data[row[0]]['volumeto']) / float(data[row[0]]['volumefrom'])

                    results[epoch_to_date(int(row[1]['time']))] = (avg_1 + avg_2 + avg_3) / 3

        return results


# moving_avg_long(data, start_date, end_date) -> dict
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def moving_avg_long(data, start_date, end_date):
    try:
        check_validity(start_date, end_date)
    except Exception as ex:
        print(ex)
    else:
        start_d = date_to_epoch(start_date)
        end_d = date_to_epoch(end_date)
        results = dict()
#same logic as above but now we have 10 days so special cases cover 9 days
        for row in enumerate(data):
            if start_d <= int(row[1]['time']) <= end_d:
                if row[0] < 9:
                    total_sum = 0

                    for x in range(10 - (row[0] + 1)):
                        total_sum += (float(data[0]['volumeto']) / float(data[0]['volumefrom']))

                    total_sum += (float(data[row[0]]['volumeto']) / float(data[row[0]]['volumefrom']))

                    results[epoch_to_date(int(row[1]['time']))] = total_sum / 10
                else:
                    total_sum = 0

                    for x in range(10):
                        total_sum += (float(data[row[0] - x]['volumeto']) / float(data[row[0] - x]['volumefrom']))

                    results[epoch_to_date(int(row[1]['time']))] = total_sum / 10

        return results


# find_buy_list(short_avg_dict, long_avg_dict) -> dict
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def find_buy_list(short_avg_dict, long_avg_dict):
    #initialize empty variables in order to define the condition for our buy signal
    previous_short = None
    previous_long = None
    current_short = None
    current_long = None

#empty result list
    results = []

    for x in short_avg_dict:
        if previous_short is None and previous_long is None and current_short is None and current_long is None:
            previous_short = short_avg_dict[x]
            previous_long = long_avg_dict[x]
            current_short = short_avg_dict[x]
            current_long = long_avg_dict[x]
            continue
        else:
            current_short = short_avg_dict[x]
            current_long = long_avg_dict[x]
#condition for buy signal
            if current_short > current_long and previous_short <= previous_long:
                results.append(x)

        previous_short = short_avg_dict[x]
        previous_long = long_avg_dict[x]

    return results


# find_sell_list(short_avg_dict, long_avg_dict) -> dict
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def find_sell_list(short_avg_dict, long_avg_dict):
    previous_short = None
    previous_long = None
    current_short = None
    current_long = None

    results = []

    for x in short_avg_dict:
        if previous_short is None and previous_long is None and current_short is None and current_long is None:
            previous_short = short_avg_dict[x]
            previous_long = long_avg_dict[x]
            current_short = short_avg_dict[x]
            current_long = long_avg_dict[x]
            continue
        else:
            current_short = short_avg_dict[x]
            current_long = long_avg_dict[x]
#condition of sell signal if previous day short MA>= previous day long MA and current short MA <current long we sell
            if previous_short >= previous_long and current_short < current_long:
                results.append(x)

        previous_short = short_avg_dict[x]
        previous_long = long_avg_dict[x]

    return results


# crossover_method(data, start_date, end_date) -> [buy_list, sell_list]
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def crossover_method(data, start_date, end_date):
    try:
        check_validity(start_date, end_date)
    except Exception as ex:
        print(ex)
    else:
        short_moving = moving_avg_short(data, start_date, end_date)
        long_moving = moving_avg_long(data, start_date, end_date)
        buy_list = find_buy_list(short_moving, long_moving)
        sell_list = find_sell_list(short_moving, long_moving)

        return [buy_list, sell_list]


# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program

    # Example variable initialization
    # data is always the cryptocompare_btc.csv read in using a DictReader

    data = []

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

        print(moving_avg_short(data, '28/04/2015', '30/04/2015'))
        moving_avg_long(data, '28/04/2015', '30/05/2015')

        crossover_method(data, '01/05/2017', '12/06/2017')

    pass




#check results



print(crossover_method(data,'01/05/2017','12/06/2017'))

print('\n')

print(crossover_method(data,'05/09/2018','27/09/2018'))

print('\n')

print(crossover_method(data,'03/11/2019','14/11/2019'))







