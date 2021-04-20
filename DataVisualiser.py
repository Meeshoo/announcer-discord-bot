import json
import math
import plotly.express as px


class DataVisualiser():

    Ledger = []
    DateData = []
    PriceData = []

    def __init__(self):
        self.LoadData()

        pass

    def LoadData(self):
        try:
            with open('./ledger.json') as f:
                self.Ledger = json.load(f)
        except:
            print("Unable to load ledger data")

        pass

    def MakeGraph(self, soundName):

        self.DateData.clear()
        self.PriceData.clear()

        for entry in self.Ledger:
            if entry['product'] == soundName:
                self.DateData.append(entry['date'])
                self.PriceData.append(entry['product_value']['currentValue'])

        graph = px.line(x=self.DateData,  y=self.PriceData)
        graph.update_layout(title=soundName,
                   xaxis_title='Date',
                   yaxis_title='Price')

        graph.write_image("graph.jpeg")

        return