
import gps
import time

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

i = 0

now = time.time()

while True:
    # if (time.time() - now >= 2.0 ):
    #     now = time.time()
    try:
        print '=== Try ==='
        report = session.next()
        # Wait for a 'TPV' report and display the current time
        # To see all report data, uncomment the line below

        # print report
        if report['class'] == 'TPV':
            print time.time() - now
            now = time.time()
            if hasattr(report, 'time'):
                print report.time
            if hasattr(report, 'lat'):
                print report.lat
            if hasattr(report, 'lon'):
                print report.lon


    except KeyError:
        print '=== KeyError ==='
        pass
    except KeyboardInterrupt:
        print '=== KeyboardInterrupt ==='
        quit()
    except StopIteration:
        print '=== StopIteration ==='
        session = None
        print "GPSD has terminated"

    # else:
    #     print 'Wait'

    # print '=== {} : {} ==='.format( i, time.time() - now )
    # i += 1

    # time.sleep(2)
