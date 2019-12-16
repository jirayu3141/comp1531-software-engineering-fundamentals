import statistics

def calculate_and_print_stats(list_of_numbers):
    ssum = sum(list_of_numbers)
    mean = statistics.mean(list_of_numbers)
    median = statistics.median(list_of_numbers)

    print('-----------------Stats-----------------')
    print(f"SUM: {ssum}")
    print(f"MEAN: {mean}")
    print(f"MEDIAN: {median}")

if __name__ == '__main__':
	calculate_and_print_stats([6,3,5,9,38,22])