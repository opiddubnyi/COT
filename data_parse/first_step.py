def getSymbolData(file_address, cftc_code):
    """Returning a list of strings for specific cftcCode of symbol
    :rtype: object
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
