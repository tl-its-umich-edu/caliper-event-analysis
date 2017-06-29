import requests
import json
import time
import logging


def api_handler(data,sess):
    AUTHORIZATION = 'Authorization'
    BASIC = 'Basic '
    MIME_TYPE_JSON = 'application/json'
    CONTENT_TYPE = 'Content-type'
    headers = {CONTENT_TYPE: MIME_TYPE_JSON, AUTHORIZATION: BASIC + TOKEN}
    response = None
    try:
        response = sess.post(url, data=data, headers=headers)
    except (requests.exceptions.RequestException, Exception) as exception:
        failure_resp.write("Connection to LRS failed %s\n" % exception)

    return response


print ("Start Of Script")
logging.basicConfig(level=logging.INFO)

TOKEN = 'xxxx'
url = 'https://xxxx.org'
fileToRead = '<absolute-path-to-file>'

success_resp = open('success_response.txt', 'w')
failure_resp = open('failed_response.txt', 'w')
failed_events = open('failed_events.json', 'w')

success_count = 0
failure_count = 0
events_count = 0

caliper_events = open(fileToRead)
fileContent = caliper_events.read()
# TODO take delimiter between event data from command line, for this instance of the script assumes it to be 'BREAK'
events = fileContent.split("BREAK\n")
start = time.time()
session = requests.session()
for event in events:
    events_count += 1
    res = api_handler(event,session)
    if res is None:
        failed_events.write("%sBREAK\n" % event)
        continue
    if res.status_code != 200:
        failure_count += 1
        failure_resp.write("%s\n" % res.text)
        failed_events.write("%sBREAK\n" % event)
        continue
    loads = json.loads(res.text)
    success_count += 1
    success_resp.write("%s\n" % res.text)
end = time.time()
caliper_events.close()
success_resp.close()
failure_resp.close()

print('Total events ', events_count)
print('Number of events send to LRS ', success_count)
print('Number of failed events ', failure_count)
print('Time taken to sending events in sec',end-start);

if events_count == success_count:
    print('All Events Sent to LRS')
else:
    print('Check for \'failed_events.json\' for unsuccessful event list and \'failed_responses.txt\' reasons for failure')
print ('End of script')
