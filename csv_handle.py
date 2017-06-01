import csv

def csv_readlist(file, file_path):
    ## csv read as list
    csv_list = []
    full_path = file_path + file
    with open(full_path) as f:
        reader = csv.DictReader(f)
        for i in reader:
            csv_list.append(i)
    return csv_list

def csv_writelist(file, file_path, data):
    ## csv write list
    full_path = file_path + file
    field = data[0].keys()
    
    with open(full_path, 'wb') as f:
        writer = csv.DictWriter(f, field)
        writer.writeheader()
        writer.writerows(data)
    
    
if __name__ == "__main__":
    file_path = '/srv/www/idehe.com/store2/stock_data/'
    file = 'ETF.csv'
    test_data = [{'aa':'BB'}]
    csv_writelist(file, file_path, test_data)
    #print csv_readlist(file, file_path)