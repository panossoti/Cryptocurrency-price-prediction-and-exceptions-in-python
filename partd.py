#relevant libraries
import csv
import time
import calendar
from exceptions import MyException as MyException

"""
    Part D
    Please provide definitions for the following clas and functions
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


# Class Investment:
# Instance variables
#	start date
#	end date
#	data
# Functions
#	highest_price(data, start_date, end_date) -> float
#	lowest_price(data, start_date, end_date) -> float
#	max_volume(data, start_date, end_date) -> float
#	best_avg_value(data, start_date, end_date) -> float
#	moving_average(data, start_date, end_date) -> float
class Investment:
    def __init__(self, start_d, end_d, data):
        self.start_date = start_d
        self.end_date = end_d
        self.data = data
#define highest price for arguments that are empty and if any of the arguments are empty take the instance variables
    def highest_price(self, start_date=None, end_date=None, data=None):
        if start_date is None or end_date is None or data is None:
            start_date = self.start_date
            end_date = self.end_date
            data = self.data
#exception handlers as done in part b
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
#same logic as above
    def lowest_price(self, start_date=None, end_date=None, data=None):
        if start_date is None or end_date is None or data is None:
            start_date = self.start_date
            end_date = self.end_date
            data = self.data

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

    def max_volume(self, start_date=None, end_date=None, data=None):
        if start_date is None or end_date is None or data is None:
            start_date = self.start_date
            end_date = self.end_date
            data = self.data

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

    def best_avg_value(self, start_date=None, end_date=None, data=None):
        if start_date is None or end_date is None or data is None:
            start_date = self.start_date
            end_date = self.end_date
            data = self.data

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

    def moving_average(self, start_date=None, end_date=None, data=None):
        if start_date is None or end_date is None or data is None:
            start_date = self.start_date
            end_date = self.end_date
            data = self.data

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
                    result += self.best_avg_value(data=data, start_date=epoch_to_date(int(row['time'])),
                                                  end_date=epoch_to_date(int(row['time'])))
                    number_of_entries += 1
            # replace None with an appropriate return value
            return round(result / number_of_entries, 2)

    pass


# predict_next_average(investment) -> float
# investment: Investment type, where type can be avg,high,low
def predict_next_average(investment):
    return regression(investment, 'avg')[0]


# predict_next_average(investment) -> float
# investment: Investment type
def regression(investment, t):
    start_date = date_to_epoch(investment.start_date)
    end_date = date_to_epoch(investment.end_date)
    data = investment.data
    #initialize variables as 0 and then iincrement to take the sum
    entries_count = 0
    timestamp_sum = 0
    price_sum = 0

    for row in data:
        if start_date <= int(row['time']) <= end_date:
            timestamp_sum += int(row['time'])

            if t == 'avg':
                price_sum += (float(row['volumeto']) / float(row['volumefrom']))
            elif t == 'high':
                price_sum += float(row['high'])
            elif t == 'low':
                price_sum += float(row['low'])

            entries_count += 1

    average_price = price_sum / entries_count
    average_timestamp = timestamp_sum / entries_count

    nominator = 0
    denominator = 0

    for row in data:
        if start_date <= int(row['time']) <= end_date:
            price = 0
            if t == 'avg':
                price = float(row['volumeto']) / float(row['volumefrom'])
            elif t == 'high':
                price = float(row['high'])
            elif t == 'low':
                price = float(row['low'])

            nominator += (int(row['time']) - average_timestamp) * (price - average_price)
            denominator_base = (int(row['time']) - average_timestamp)
            denominator += (denominator_base * denominator_base)

    m = nominator / denominator
    b = average_price - (m * average_timestamp)
    y = (m * average_timestamp) + b

    print(y)
    print(m)

    return (y, m)


# classify_trend(investment) -> str
# investment: Investment type
def classify_trend(investment):
    low = regression(investment, 'low')
    high = regression(investment, 'high')
#trend per document instructions
    if high[1] > 0 and low[1] < 0:
        return 'volatile'
    elif high[1] > 0 and low[1] > 0:
        return 'increasing'
    elif high[1] < 0 and low[1] < 0:
        return 'decreasing'
    else:
        return 'other'


# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program
    data = []
    with open("cryptocompare_btc.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

        investment1 = Investment('04/05/2015', '27/05/2015', data)
        investment2 = Investment('01/02/2016', '28/02/2016', data)
        investment3 = Investment('08/12/2016', '11/12/2016', data)

        regression(investment1, 'avg')
        print('----------------------')
        regression(investment2, 'avg')
        print('----------------------')
        regression(investment3, 'avg')
        print('----------------------')
        print('----------------------')
        print('----------------------')

        print(classify_trend(investment1))
        print('----------------------')
        print(classify_trend(investment2))
        print('----------------------')
        print(classify_trend(investment3))
    pass