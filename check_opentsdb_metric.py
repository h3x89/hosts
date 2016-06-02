#!/usr/bin/python2.6
import requests
import optparse
import json
import datetime
import sys

# ./check_opentsdb_metric.py -t 1h-ago -m "sum:XXX.haproxy.queue.current{dc=sjc,backend=pod0,instance=l2-stateless,bserver=app13_6180}" -u https://opentsdb.XXX-internal.com:4242/api/query -w 1 - c 2

parser = optparse.OptionParser()

parser.add_option('-t', '--time',
                        action="store",
                        dest="time",
                        help="define time fe.: 1h-ago (we are getting last value from this period)",
                        default="1h-ago")

parser.add_option('-m', '--metric',
                        action="store",
                        dest="metric",
                        help="define metric without spaces fe.: sum:XXX.haproxy.sessions.limit{dc=sjc,backend=pod0,instance=l2-stateless}",
                        # default="sum:XXX.haproxy.sessions.limit{dc=sjc,backend=pod0,instance=l2-stateless}")
                        default="sum:XXX.haproxy.queue.current{dc=sjc,backend=pod0,instance=l2-stateless,bserver=app24_6180}")
                        # default="sum:XXX.loadavg.1m{dc=sjc,host=app13,service=cfs}")

parser.add_option('-u', '--url',
                        action="store",
                        dest="host",
                        help="host fe.: https://opentsdb.XXX-internal.com:4242/api/query",
                        default="https://opentsdb.XXX-internal.com:4242/api/query")

parser.add_option('-w', '--warning',
                        action="store",
                        dest="warning",
                        help="define warning threshold",
                        default="5")

parser.add_option('-c', '--critical',
                        action="store",
                        dest="critical",
                        help="define critical threshold",
                        default="10")

parser.add_option("-v", action="store_true", dest="verbose")



options, args = parser.parse_args()

warning = float(options.warning)
critical = float(options.critical)

if warning >= critical:
    print("critical should be bigger that warning")
    sys.exit(3)


# print 'time string:', options.time
# print 'time string:', options.metric

# curl -d start=1h-ago  -d m="sum:XXX.haproxy.sessions.limit{dc=sjc,backend=pod0,instance=l2-stateless}" -d ascii= --get  https://opentsdb.XXX-internal.com:4242/api/query -H "Content-Type: application/json; charset=UTF-8" | python -m json.tool
# http://localhost:4242/api/query?start=1h-ago&m=sum:rate:proc.stat.cpu{host=foo,type=idle}


payload = {
    'start': options.time,
    'm': options.metric
}

json_string = requests.get(
    url=options.host,
    params=payload
).content

parsed_json = json.loads(json_string)

# get interesting values
value_dict = parsed_json[0]['dps']


# get last key
# last_key = value_dict.keys()[-1]
last_key = sorted(value_dict)[-1]

# get last value from last kay
last_value = value_dict[last_key]
last_value = float(last_value)

if options.verbose == True:
    print parsed_json
    print
    print sorted(value_dict)
    print
    print last_key
    print
    print last_value

time = (
    datetime.datetime.fromtimestamp(
        int(last_key)
    ).strftime('%Y-%m-%d %H:%M:%S')
)

answer = ("Value:%f warning:%f critical:%f - Time:%s" % (last_value, warning, critical, time))


if last_value <= warning:
    print("OK %s" % (answer))
    sys.exit(0)
elif last_value <= critical:
    print("WARNING %s" % (answer))
    sys.exit(1)
elif last_value > critical:
    print("CRITICAL %s" % (answer))
    sys.exit(2)
else:
    print("UNKNOWN %s" % (answer))
    sys.exit(3)


# http://localhost:4242/api/query/last?timeseries=proc.stat.cpu{host=foo,type=idle}&timeseries=proc.stat.mem{host=foo,type=idle}

# payload = {
#     'timeseries': "XXX.haproxy.sessions.limit{dc=sjc,backend=pod0,instance=l2-stateless}"}
# print requests.get(
#     url="https://opentsdb.XXX-internal.com:4242/api/query/last",
#     params=payload
# ).content
