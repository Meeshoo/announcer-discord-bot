import json
import pprint
import uuid


class EconomyDatabase():
    EconomyData = {}
    Ledger = []
    coinsPerInterval = 0

    def __init__(self, coinsPerInterval):
        self.LoadData()
        self.coinsPerInterval = coinsPerInterval
        pass

    def LoadData(self):
        try:
            with open('./database.json') as f:
                self.EconomyData = json.load(f)
        except:
            self.WriteDataToFile()
        try:
            with open('./ledger.json') as f:
                self.Ledger = json.load(f)
        except:
            self.WriteToLedger({})
        pass

    def AddUserData(self, member):
        if not member in self.EconomyData:
            self.EconomyData[member] = 0
            self.WriteDataToFile()
        pass

    def GetUserData(self, member):
        for member in self.EconomyData:
            if member == member:
                return self.EconomyData[member]
        pass

    def GetAllUserData(self):
        return pprint.pformat(self.EconomyData)

    def GiveUsersMoney(self, members):
        for member in members:
            if member.name in self.EconomyData:
                self.EconomyData[member.name] += int(self.coinsPerInterval)
        self.WriteDataToFile()
        pass

    def WriteDataToFile(self):
        with open('database.json', 'w') as json_file:
            json.dump(self.EconomyData, json_file)
        pass

    def WriteToLedger(self, transaction):
        self.Ledger.append(transaction)
        with open('ledger.json', 'w') as json_file:
            json.dump(self.Ledger, json_file)
        pass

    async def Transaction(self, member, product, message):
        memberBalance = self.EconomyData[member]
        balanceDifference = memberBalance - product["value"]
        if balanceDifference >= 0:
            self.EconomyData[member] -= product["value"]
            self.WriteDataToFile()

            newTransaction = {
                "id": str(uuid.uuid4()),
                "member": member,
                "value": product["value"]}
            print(newTransaction)
            self.WriteToLedger(newTransaction)
            await message.reply('*Kertching* Deducted: ' + str(product["value"]) + ' Playing sound', mention_author=False)

            # Play the audio product
        else:
            await message.reply('You do not have enough money', mention_author=False)
            # mesage saying they don't have enough
        pass