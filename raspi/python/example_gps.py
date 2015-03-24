import gps

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
        # Wait for a 'TPV' report and display the current time
        # To see all report data, uncomment the line below
        # print report
        if report['class'] == 'TPV':
            if hasattr(report, 'time'):
                print report.time
                print
                print ' GPS reading'
                print '----------------------------------------'
                print 'latitude ' , session.fix.latitude
                print 'longitude ' , session.fix.longitude
                print 'time utc ' , session.utc, session.fix.time
                print 'altitude ' , session.fix.altitude
                print 'eph ' , session.fix.eph
                print 'epv ' , session.fix.epv
                print 'ept ' , session.fix.ept
                print 'speed ' , session.fix.speed
                print 'climb ' , session.fix.climb
                print
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print "GPSD has terminated"