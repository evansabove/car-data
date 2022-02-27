import csv 

def initialize_csv(drive_id, keys):
    with open('drives/' + str(drive_id) + '.csv', 'a', newline='') as file:
        print("Writing headers: ", ','.join(keys))

        writer = csv.DictWriter(file, keys)
        writer.writeheader()

def write_to_csv(drive_id, dict):
    with open('drives/' + str(drive_id) + '.csv', 'a', newline='') as file:
        print("Writing data", ','.join([str(i) for i in dict.values()]))

        writer = csv.DictWriter(file, list(dict.keys()))
        writer.writerow(dict)