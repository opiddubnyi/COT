"""
TODO: Add module docstring
"""

import datetime
import time
import os
import shutil
import dload


_UPDATE = 'https://www.cftc.gov/files/dea/history/deacot2021.zip'
_DB_PATH = r'D:/Python/My_projects/COT/database/'
_DB = r'D:/Python/My_projects/COT/database/data.txt'


def get_symbol_data(file_address, cftc_code):
    """Returning a data list for specific cftcCode in file
    :rtype: list
    """

    symbol_yearly_data = []
    array = []
    # reading txt file and writing its content into a list
    # txt -> list of strings
    with open(file_address) as file:
        for line in file:
            array.append(line.strip('\n'))

    # get all that contain cftc_code
    for lines in range(len(array)):
        if array[lines].count(cftc_code) >= 1:
            symbol_yearly_data.append(array[lines])
    return symbol_yearly_data


def update_valid_dates_list():
    """
    Updates list with all CFTC report dates for data validation
    :return: list of valid dates
    """

    dates = []

    # Updating list
    with open(f'{_DB_PATH}datelist.txt', 'w') as _:
        for line in get_symbol_data(_DB, "098662"):
            dates.append(line.split(',')[2])
    return dates


valid_dates = update_valid_dates_list()


def accumulate_all_data(*files):
    """
    Accepts all files that need to be merged in one large DB
    Params should be used from newer years to older to get descending order
    File needs to be deleted before next weekly update
    :param files: yearly data files from cftc.gov
    :return: None. Writes all to data.txt
    """
    result_address = _DB

    for file in files:
        file_address = f'D://Python//My_projects//COT//database/{file}'
        with open(result_address, 'a+') as fin:
            with open(file_address) as fout:
                fin.writelines(fout)


def download_update_data(update_link=_UPDATE):
    """
    Downloads archive with data from update_link, unzips archive and saves
    to annual + {current year}.txt into database folder
    :param update_link: 'https:/...'
    :return: None
    """
    year = datetime.datetime.now().year
    download_location = "D:/Python/My_projects/COT/database/update"
    # download and unzip file
    dload.save_unzip(update_link, f'{download_location}')

    # move file to DB
    shutil.move(f'{download_location}/annual.txt', _DB_PATH)

    # rename file
    os.rename(f'{_DB_PATH}/annual.txt', f'{_DB_PATH}/annual{year}.txt')


def get_open_interest(cftc_code, date='last', period=None):
    """
    Works with list returned by @get_symbol_data and returns OI.

    Default OI period is set to last reported week,
    :return: list of strings "data = oi" for specified cftc_code
    """
    # get all symbol data from DB
    data = get_symbol_data(_DB, cftc_code)

    # splitting by separator ',' and locating last OI if no date were provided
    if date == 'last':
        print(f'Last reported OI is {data[0].split(",")[7]} on '
              f'{data[0].split(",")[2]}')

    if check_valid_date(date, valid_dates):
        for line in range(len(data)):
            if data[line].count(date) >= 1:
                print(f'Last reported OI is {data[line].split(",")[7]} on '
                      f'{data[line].split(",")[2]}')
    if not check_valid_date(date, valid_dates):
        print('Please enter date in format : YYYY-MM-DD')

    #     TODO: custom period for OI data


def check_valid_date(date, array):
    """
    Return True if entered date is in
    :return:
    """
    return True if date in array else False


start_time = time.time()
# sandbox for testing functions

print("--- %s seconds ---" % (time.time() - start_time))
