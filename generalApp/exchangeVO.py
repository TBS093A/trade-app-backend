from django.http import HttpResponse
from datetime import datetime
from .models import *
from .utilities import *
import threading
import requests
import json
import os

class ExchangeVO():

    triggerList = None

    def __init__(self):
        pass

    @classmethod
    def checkTrigger(self):
        triggerAll = Triggers.objects.filter(status = 1).values("id", "user_id", "status", "course_values_for_trigger", "date_of_trigger")
        self.triggerList = []
        for x in triggerAll:
            self.triggerList.append(x)
        actualGraph = self.refreshGraph(1800)
        for candle in actualGraph['candles']:
            candleDate = datetime.strptime(candle['Date'], "%Y-%m-%d %H:%M:%S")
            inArea = 0
            for trigger in self.triggerList:
                triggerDate = datetime.strptime(trigger['date_of_trigger'], "%Y-%d-%m %H:%M")
                if int(trigger['course_values_for_trigger']) > int(candle['Min']) and triggerDate < candleDate:
                    inArea += 1
                if int(trigger['course_values_for_trigger']) < int(candle['Max']) and triggerDate < candleDate:
                    inArea += 1
                if inArea == 2:
                    disableTrigger = Triggers.objects.get(id = int(trigger['id']))
                    disableTrigger.status = 0
                    message = f"Exchange got Your Trigger Value! \nTrigger Value: {trigger['course_values_for_trigger']} \nCandle Date: {candle['Date']}"
                    newNotification = Notifications(user_id = int(trigger['user_id']), message = message)
                    newNotification.save()
                    disableTrigger.save()
                inArea = 0
        print(self.triggerList)

    @classmethod
    def createActualPrognosis(self, request, time, price, privilige):
        actualGraph = self.refreshGraph(time)
        svg = []
        svgAll = 0
        volume = []
        actualCourse = 0
        for candle in actualGraph['candles']:
            svg.append((float(candle['Close'] + candle['Open']) / 2))
            volume.append(float(candle['Volume']))
            actualCourse = float(candle['Close'])
            datePayment = candle['Date']
            if svgAll == 0:
                svgAll = svgAll + svg[-1]
            else:
                svgAll = (svgAll + svg[-1]) / 2
        onePercentOfActualCourse = actualCourse / 100
        percentsFromPriceToCourse = price / onePercentOfActualCourse
        onePercentOfSvgCourse = svgAll / 100
        priceAfterCourse = percentsFromPriceToCourse * onePercentOfSvgCourse
        difference = priceAfterCourse - price
        percentDifference = difference / onePercentOfSvgCourse
        data = {
            "price" : price,
            "price_forecast" : priceAfterCourse,
            "percent_of_difference" : percentDifference,
            "course_on_payment" : actualCourse,
            "svg_of_all" : svgAll,
            "date_of_transaction" : datePayment
        }
        return HttpResponse(json.dumps(data))

    @classmethod
    def refreshGraph(self, time):
        graph = []
        try:
            graph = self.createGraph(time)
        except:
            currentDirectory = os.path.dirname(__file__)
            jsonPath = os.path.join(currentDirectory, '../testGraph.txt')
            with open(jsonPath) as graphJson:
                graph = json.load(graphJson)
        return self.createGraph(time)

    @classmethod
    def createGraph(self, time):
        miliseconds = 1000
        firstResult = int(datetime.now().timestamp() * miliseconds)
        lastResult = firstResult - 100000 * (time * 2)
        url = f"https://api.bitbay.net/rest/trading/candle/history/BTC-PLN/{time}?from={lastResult}&to={firstResult}"
        querystring = {"from": f"{lastResult}","to": f"{firstResult}"}
        exchangeGraph = requests.request("GET", url, params=querystring)
        response = json.loads(exchangeGraph.text)
        graph = { 'candles': [], 'candlesCount' : 0, 'graphMin': float(response['items'][0][1]['h']), 'graphMax': 0 }
        for x in range(len(response['items'])):
            graph['candles'].append({'Open': 0, 'Close': 0, 'Max': 0, 'Min': 0, 'Volume': 0, 'Date': 0 })
            graph['candles'][x]['Open'] = float(response['items'][x][1]['o'])
            graph['candles'][x]['Close'] = float(response['items'][x][1]['c'])
            graph['candles'][x]['Max'] = float(response['items'][x][1]['h'])
            graph['candles'][x]['Min'] = float(response['items'][x][1]['l'])
            graph['candles'][x]['Volume'] = float(response['items'][x][1]['v'])
            graph['candles'][x]['Date'] = str(datetime.fromtimestamp(int(response['items'][x][0])/1000.0))
            if graph['candles'][x]['Min'] < graph['graphMin']:
                graph['graphMin'] = graph['candles'][x]['Min']
            if graph['candles'][x]['Max'] > graph['graphMax']:
                graph['graphMax'] = graph['candles'][x]['Max']
        graph['candlesCount'] = len(response['items']) - 1
        return graph

    @classmethod
    def getGraphView(self, request, time):
        graph = []
        try:
            graph = self.createGraph(time)
        except:
            currentDirectory = os.path.dirname(__file__)
            jsonPath = os.path.join(currentDirectory, '../testGraph.txt')
            with open(jsonPath) as graphJson:
                graph = json.load(graphJson)
        return HttpResponse(json.dumps(graph))
