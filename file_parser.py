from csv import reader

def parseCSV(filename):
    # Return dict containing zones with record data.
    # Initial version assumes format is valid, simplistic, and in expected order.
    data = {}
    with open(filename) as f:
        csv_reader = reader(f)
        next(csv_reader, None)
        for row in csv_reader:
            if len(row) == 5:
                name = row[0]
                zone = row[1]
                rtype = row[2]
                ttl = int(row[3])
                answer = row[4]
                if rtype != 'TXT':
                    answer = answer.split(' ')
                if name == '@':
                    name = zone
                record = {'name': name, 'type': rtype, 'ttl': ttl, 'data': answer}
                if zone not in data:
                    data[zone] = []
                data[zone].append(record)
    return data
