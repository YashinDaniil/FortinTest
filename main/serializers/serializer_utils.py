def get_days_count(year, month):
    num_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if (year % 4 == 0) or (year % 100 == 0 and year % 400 == 0):
        num_days[1] = 29

    return num_days[month-1]