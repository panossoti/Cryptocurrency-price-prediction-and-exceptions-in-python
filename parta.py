# import relevant libraries

import csv
import time
import calendar

# Function to convert epoch time to date timestamp

def epoch_to_date(timestamp):
    dt = time.gmtime(timestamp)
    date_string = time.strftime('%d/%m/%Y', dt)
    return date_string


# from date to epoch
def date_to_epoch(epoch):
    timestamp = calendar.timegm(time.strptime(epoch, "%d/%m/%Y"))
    return timestamp


"""
    Part A
    Please provide definitions for the following functions
"""


# highest_price(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def highest_price(data, start_date, end_date):
    high_list = []
    start_d = date_to_epoch(start_date)
    end_d = date_to_epoch(end_date)
    # make a for loop to append highest prices only if inside our given date range
    for row in data:

        if start_d <= int(row['time']) <= end_d:
            high_list.append(float(row['high']))

    # replace None with an appropriate return value

    return max(high_list)


# lowest_price(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def lowest_price(data, start_date, end_date):
    low_list = []

    start_d = date_to_epoch(start_date)
    end_d = date_to_epoch(end_date)
#same logic as before but now with low column
    for row in data:
        if start_d <= int(row['time']) <= end_d:
            low_list.append(float(row['low']))


    # replace None with an appropriate return value
    return min(low_list)


# max_volume(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def max_volume(data, start_date, end_date):
    # replace None with an appropriate return value
    volume_list = []
#playing around with implementations it could be done just as above ^
    for row in data:
        if date_to_epoch(start_date) <= int(row['time']) <= date_to_epoch(end_date):
            volume_list.append(float(row['volumefrom']))

    return max(volume_list)


# best_avg_value(data, start_date, end_date) -> float
# data: the data from a csv file
# start_date: string in "dd/mm/yyyy" format
# start_date: string in "dd/mm/yyyy" format
def best_avg_price(data, start_date, end_date):
    avg_list = []
    start_d = date_to_epoch(start_date)
    end_d = date_to_epoch(end_date)
#special case when start date= end date this will make code more efficient and accounts for one more case instead of itterating every time
    if start_d == end_d:
        items = list(filter(lambda i: int(i['time']) == start_d, data))

        if len(items) == 1:
            item = items[0]
            return float(item['volumeto']) / float(item['volumefrom'])

    for row in data:
        if start_d <= int(row['time']) <= end_d:
            avg_list.append(float(row['volumeto']) / float(row['volumefrom']))

    # replace None with an appropriate return value
    return max(avg_list)


#Steps for Moving average :
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
    avg_list = []
    start_d = date_to_epoch(start_date)
    end_d = date_to_epoch(end_date)
    sum = 0
    number_of_entries = 0

    for row in data:
        if start_d <= int(row['time']) <= end_d:
            sum += best_avg_price(data, epoch_to_date(int(row['time'])), epoch_to_date(int(row['time'])))
            number_of_entries += 1
    # return answer in 2 decimal places
    return round(sum / number_of_entries, 2)


# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program

    # Example variable initialization
    # data is always the cryptocompare_btc.csv read in using a DictReader

    data = []
    with open("cryptocompare_btc.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    # access individual rows from data using list indices
    first_row = data[0]
    # to access row values, use relevant column heading in csv
    print(f"timestamp = {first_row['time']}")
    print(f"daily high = {first_row['high']}")
    print(f"volume in BTC = {first_row['volumefrom']}")

    # check results

    print("highest price between {} and {} is\n{}".format('01/01/2016', '31/01/2016', highest_price(data, '01/01/2016', '31/01/2016')))
    print(str(highest_price(data, '01/02/2016', '28/02/2016')))
    print(highest_price(data, '01/12/2016', '31/12/2016'))

    print(lowest_price(data, '01/01/2016', '31/01/2016'))
    print(lowest_price(data, '01/02/2016', '28/02/2016'))
    print(lowest_price(data, '01/12/2016', '31/12/2016'))

    print(max_volume(data, '01/01/2016', '31/01/2016'))
    print(max_volume(data, '01/02/2016', '28/02/2016'))
    print(max_volume(data, '01/12/2016', '31/12/2016'))

    print(best_avg_price(data, '01/01/2016', '31/01/2016'))
    print(best_avg_price(data, '01/02/2016', '28/02/2016'))
    print(best_avg_price(data, '01/12/2016', '31/12/2016'))

    print(moving_average(data, '01/01/2016', '31/01/2016'))
    print(moving_average(data, '01/02/2016', '28/02/2016'))
    print(moving_average(data, '01/12/2016', '31/12/2016'))



    pass

