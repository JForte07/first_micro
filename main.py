from flask import Flask
import requests
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'silicon-works-373618-47f27a542f68.json'
VIEW_ID = '282324097' #You can find this in Google Analytics > Admin > Property > View > View Settings (VIEW ID)

@app.route('/', methods=["GET"])
def hello_world():
 prefix_google = """
 <!-- Google tag (gtag.js) -->
<script async
src="https://www.googletagmanager.com/gtag/js?id=G-XFPGT0NR9L"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', ' G-XFPGT0NR9L');
</script>
 """
 return prefix_google + "Hello World"

#add logger 
@app.route('/logger', methods=["GET"])
def logger():
    #print('hi')
    app.logger.info('testing info log in the console')
    script = """
    <script> console.log("Hello, if you see me it means is working")</script>"""
    print('Hello, if you see me it means is working')

    ##print a message in textbox
    script2 = """
    <script>
        function myFunction() {
        var message = document.getElementById("message").value;
        console.log(message);
        }
    </script>"""

    return """
    <input type="text" id="message" placeholder="Enter a message">
    <button onclick="myFunction()">Print</button>""" + script2

    ## Manipulate Cookies 
@app.route('/cookies', methods=["GET"])
def cookies():
 req = requests.get("https://analytics.google.com/analytics/web/#/p344941720/reports/intelligenthome")
 return req.text

#print the numbers of visitors 
def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': []
        }]
      }
  ).execute()


def get_visitors(response):
  visitors = 0 # in case there are no analytics available yet
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dateRangeValues = row.get('metrics', [])

      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          visitors = value

  return str(visitors)


@app.route('/visitors')
def visitors():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  visitors = get_visitors(response)

  return "nb visitors :" + visitors