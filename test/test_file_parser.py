from file_parser import *

filename = 'test/test_data.csv'
data = {
    'example2.test': [
        {
            'name': 'example2.test',
            'type': 'A',
            'ttl': 300,
            'data': ['1.2.3.4']
        },
        {
            'name': 'example2.test',
            'type': 'MX',
            'ttl': 86400,
            'data': ['10', 'mail2.mailer.com']
        },
        {
            'name': 'www',
            'type': 'CNAME',
            'ttl': 60,
            'data': ['example2.test']
        },
        {
            'name': 'example2.test',
            'type': 'TXT',
            'ttl': 86400,
            'data': 'v=spf1 mx a -all'
        }
    ],
    'other2.test': [
        {
            'name': 'ftp',
            'type': 'A',
            'ttl': 3600,
            'data': ['5.6.7.8']
        }
    ]
}

def test_parseCSV():
    result = parseCSV(filename)
    assert(result) == data
