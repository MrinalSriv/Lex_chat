import requests
import json
class Api:
    def __init__(self):
        pass

    def makeApiRequestForCounrty(self, country_name):
        url = "https://covid-193.p.rapidapi.com/statistics"
        querystring = {"country": country_name}
        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': "5d2d6eca48mshdad55fb93eb97ecp12d8e7jsnbe380885c652"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        js = json.loads(response.text)
        print("******", js)
        result = js.get('response')[0]
        print(result.get('cases'))
        print("*" * 20)
        return result.get('cases') , result.get('deaths'),result.get('tests')


    def makeApiRequestForIndianStates(self, cust_state):
        url = "https://covid19-data.p.rapidapi.com/india"
        headers = {
            'x-rapidapi-host': "covid19-data.p.rapidapi.com",
            'x-rapidapi-key': "582a8f8516msh16204eb9d1f4f68p1a9146jsnf33914c7300e"
        }
        response = requests.request("GET", url, headers=headers)
        js = json.loads(response.text)
        webhookresponse1 = ''
        print(cust_state)
        for i in range(0, 37):
            webhookresponse = js[i]
            if webhookresponse['state'] == cust_state:
                webhookresponse1 += "*********\n" + " State :" + str(webhookresponse['state']) + \
                                    "\n" + " Confirmed cases : " + str(
                    webhookresponse['confirmed']) + "\n" + " Death cases : " + str(webhookresponse['deaths']) + \
                                    "\n" + " Active cases : " + str(
                    webhookresponse['active']) + "\n" + " Recovered cases : " + str(
                    webhookresponse['recovered']) + "\n*********"
                break;

        return webhookresponse1, '@@@', '@@@'


    def makeApiWorldwide(self):
        url = "https://covid-19-statistics.p.rapidapi.com/reports/total"
        headers = {
            "x-rapidapi-host": "covid-19-statistics.p.rapidapi.com",
            "x-rapidapi-key": "582a8f8516msh16204eb9d1f4f68p1a9146jsnf33914c7300e"
        }
        response = requests.request("GET", url, headers=headers)
        # print(response.text)
        js = json.loads(response.text)
        print("******", js)
        result = js.get('data')

        return result

