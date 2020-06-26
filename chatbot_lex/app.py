# doing necessary imports
from wsgiref import simple_server

from flask import Flask, request
from flask import Response
from flask_cors import cross_origin
from DataRequests import MakeApiRequests
from saveConversation import Conversations

app = Flask(__name__)  # initialising the flask app with the name 'app'


# geting and sending response to Amazon Lex
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    intent = request.json['Intent']
    curr_slots = request.json['curr_slots']
    print(curr_slots)
    res = processRequest(intent,curr_slots)
    return Response(res)

def processRequest(intent,curr_slots):
    log = Conversations.Log()
    #db = configureDataBase()
    if intent == 'covid_searchcountry' :
        cust_country = curr_slots.get("country_name")
        #print('Mrinal',cust_country)
        if (cust_country == "United States"):
            cust_country = "USA"

        fulfillmentText, deaths_data, testsdone_data = makeAPIRequest(cust_country,"country_name")
        webhookresponse = "######Covid Report######### \n\n" + " New cases :" + str(fulfillmentText.get('new')) + \
                          "\n" + " Active cases : " + str(
            fulfillmentText.get('active')) + "\n" + " Critical cases : " + str(fulfillmentText.get('critical')) + \
                          "\n" + " Recovered cases : " + str(
            fulfillmentText.get('recovered')) + "\n" + " Total cases : " + str(fulfillmentText.get('total')) + \
                          "\n" + " Total Deaths : " + str(deaths_data.get('total')) + "\n" + " New Deaths : " + str(
            deaths_data.get('new')) + \
                          "\n" + " Total Test Done : " + str(deaths_data.get('total')) + "\n\n*******END********* \n "
        print(webhookresponse)

    elif intent == "covid_searchstate":
        cust_state = curr_slots.get("India_state")
        print('Mrinal', cust_state)
        fulfillmentText, deaths_data, testsdone_data = makeAPIRequest(cust_state ,"India_state")
        print (fulfillmentText)
        webhookresponse = fulfillmentText
    elif intent == "totalnumber_cases":
        fulfillmentText = makeAPIRequest("world","world")

        webhookresponse = "***World wide Report*** \n\n" + " Confirmed cases :" + str(
            fulfillmentText.get('confirmed')) + \
                          "\n" + " Deaths cases : " + str(
            fulfillmentText.get('deaths')) + "\n" + " Recovered cases : " + str(fulfillmentText.get('recovered')) + \
                          "\n" + " Active cases : " + str(
            fulfillmentText.get('active')) + "\n" + " Fatality Rate : " + str(
            fulfillmentText.get('fatality_rate') * 100) + "%" + \
                          "\n" + " Last updated : " + str(
            fulfillmentText.get('last_update')) + "\n\n*******END********* \n "
        print(webhookresponse)

    return webhookresponse

def makeAPIRequest(query,search):
    api = MakeApiRequests.Api()
    print("query",query)
    if search == "world":
        return api.makeApiWorldwide()
    if search == "India_state":
        return api.makeApiRequestForIndianStates(query)

    else:
        return api.makeApiRequestForCounrty(query)



#port = int(os.getenv("PORT"))
if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()