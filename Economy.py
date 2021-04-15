import json
import pprint
import uuid
from time import gmtime, strftime


class EconomyDatabase():
    EconomyData = {}
    ProductData = {}
    Ledger = []
    prettySfxList = ""

    def __init__(self, coinsPerInterval):
        self.LoadData()
        self.coinsPerInterval = coinsPerInterval

        for sfx in self.ProductData:
            self.prettySfxList = self.prettySfxList + sfx + ': ' + \
                str(self.ProductData[sfx]['currentValue']) + '\n'

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
        try:
            with open('./discord_products.json') as f:
                self.ProductData = json.load(f)
        except:
            print("!MISSING PRODUCT DATA!")
        pass

    def AddUserData(self, member):
        if not member in self.EconomyData:
            self.EconomyData[member] = 0
            self.WriteDataToFile()
        pass

    def GetUserData(self, inMember):
        for member in self.EconomyData:
            if member == inMember:
                return self.EconomyData[inMember]
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
            json.dump(self.EconomyData, json_file, indent=4)
        pass

    def WriteToLedger(self, transaction):
        self.Ledger.append(transaction)
        with open('ledger.json', 'w') as json_file:
            json.dump(self.Ledger, json_file, indent=4)
        pass

    async def Transaction(self, member, message):
        memberBalance = self.EconomyData[member]
        product = message.content.lower()
        currentProduct = self.ProductData[product]
        balanceDifference = memberBalance - currentProduct["currentValue"]
        if balanceDifference >= 0:
            self.EconomyData[member] -= currentProduct["currentValue"]
            self.WriteDataToFile()

            newTransaction = {
                "id": str(uuid.uuid4()),
                "date": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                "member": member,
                "product": message.content.lower(),
                "product_value": currentProduct
            }
            print(newTransaction)
            self.WriteToLedger(newTransaction)
            await message.reply('*Kertching* Deducted: ' + str(currentProduct["currentValue"]) + ' For Buying: ' + message.content.lower(), mention_author=False)
            return True

        else:
            await message.reply('You do not have enough money', mention_author=False)
            return False

        pass
