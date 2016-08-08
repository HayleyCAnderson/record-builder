from argparse import ArgumentParser
from nsone import NSONE, Config
from file_parser import parseCSV
from twisted.internet import defer, reactor

# Get configuration settings from command line for added flexibility.
parser = ArgumentParser(description='Asychronously create DNS records from file.')
parser.add_argument('-f', dest='filename', required=True, type=str, nargs='?', help='relative path to file')
parser.add_argument('-k', dest='apikey', required=True, type=str, nargs='?', help='NS1 API key')
args = parser.parse_args()

# Set configuration with API key and asynchronous Twisted transport setting.
config = Config()
config.createFromAPIKey(args.apikey)
config['transport'] = 'twisted'
nsone = NSONE(config=config)

def getData(filename):
    # Return Deferred.
    # Parse file into dict containing zones with record data.
    # Currently only parses CSV files.
    # Could add other file type parsing and select based on filename.
    data = parseCSV(filename)
    return defer.succeed(data)

def handleData(data):
    # Return DeferredList.
    # Register success when record additions for all zones have completed.
    zones = []
    for domain, records in data.iteritems():
        zone = loadZone(domain)
        zone.addCallback(addRecords, records)
        zone.addErrback(handleError)
        zones.append(zone)
    return defer.DeferredList(zones)

def loadZone(zone):
    # Return Deferred.
    # Load zone object from API.
    # Raise error if zone not found or invalid.
    return nsone.loadZone(zone)

def addRecords(zone, records):
    # Return DeferredList.
    # Register success when all record additions for zone have completed.
    builders = []
    for data in records:
        builder = getZone(zone)
        builder.addCallback(addRecord, data)
        builder.addCallbacks(printRecord, handleRecordError)
        builder.addErrback(handleError)
        builders.append(builder)
    return defer.DeferredList(builders)

def getZone(zone):
    # Return Deferred.
    # Get zone object already fetched from API.
    return defer.succeed(zone)

def addRecord(zone, record):
    # Return Deferred.
    # Build and return record object through API.
    # Raise error if record already created or invalid.
    builder = getattr(zone, 'add_' + record['type'])
    return builder(record['name'], record['data'], ttl=record['ttl'])

def printRecord(record):
    # Print successful record addition result.
    print 'Record successfully added:'
    print record.data

def handleRecordError(failure):
    # Gracefully handle record addition error.
    print 'Record not added:'
    print failure.getErrorMessage()

def handleError(failure):
    # Print failure object including traceback.
    print failure

def endProgram(result):
    # Stop reactor at planned end of execution.
    reactor.stop()

data = getData(args.filename)
data.addCallback(handleData)
data.addErrback(handleError)
data.addCallback(endProgram)

reactor.run()
