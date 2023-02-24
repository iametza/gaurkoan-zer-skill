from mycroft import MycroftSkill, intent_file_handler

import requests

class GaurkoanZer(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)
        self.api = Api()
        self.efemerideak = 0

    @intent_file_handler('zer.gaurkoan.intent')

    def handle_zer_gaurkoan(self, message):
        self.tartea = 'gaurkoak'

        efemerideak = self.api.getEfemerideak(self.tartea)

        self.efemerideak = efemerideak

        #self.speak_dialog('zer.gaurkoan')
        self.speak('Gaurko egunez %d efemeride aurkitu ditut'%(len(efemerideak['data'])))

        for efemeridea in efemerideak['data']:
            egutegia = Egutegia(efemeridea['data'])
            self.speak(egutegia.getProcessed() + ' ' + efemeridea['izena'])

    @intent_file_handler('aste.honetan.zer.intent')

    def handle_aste_honetan_zer(self, message):
        self.tartea = 'astekoak'

        efemerideak = self.api.getEfemerideak('astekoak')

        self.efemerideak = efemerideak

        self.speak('Aste honetan %d efemeride aurkitu ditut'%(len(efemerideak['data'])))

        for efemeridea in efemerideak['data']:
            egutegia = Egutegia(efemeridea['data'])
            self.speak(egutegia.getProcessed() + ' ' + efemeridea['izena'])

    @intent_file_handler('informazio.gehiago.intent')

    def handle_informazio_gehiago(self, message):
        if not self.efemerideak:
            self.speak("Ez dago efemeriderik sakontzeko")

        else:
            for efemeridea in self.efemerideak['data']:
                egutegia = Egutegia(efemeridea['data'])
                self.speak(egutegia.getProcessed() + ' ' + efemeridea['azalpena'])

    def stop(self):
        pass


def create_skill():
    return GaurkoanZer()

class Api:
    url = 'https://gaurkoanzer.eus/api'
    version = 'v1'
    
    def getEfemerideak(self, tartea = 'gaurkoak'):
        self.method = 'efemerideak'
        return self.doCall('?tartea=' + tartea)

    def doCall(self, params = ''):
        url = self.getUrl()
        url += params
        result = requests.get(url)
        if (result.status_code != 200):
            return result.status_code
        else:
            return result.json() 

    def getUrl(self):
        return self.url + '/' + self.version + '/' + self.method

class Egutegia:

    def __init__(self, data=''):
        self.data = data
        self.urtea, self.hilabetea, self.eguna = self.data.split('-')

    def getData(self):
        return self.data

    def getUrtea(self):
        return self.urtea

    def getHilabetea(self):
        return self.hilabetea

    def getEguna(self):
        return self.eguna

    def processHilabetea(self):
        hilabeteak = ['Urtarrila', 'Otsaila', 'Martxoa', 'Apirila', 'Maiatza', 'Ekaina', 'Uztaila', 'Abuztua', 'Iraila', 'Urria', 'Azaroa', 'Abendua']
        hilabetea = int(self.hilabetea) - 1
        if (hilabetea < 0 or hilabetea > len(hilabeteak)-1):
            return "" 
        return hilabeteak[hilabetea]

    def getProcessed(self):
        return "%dko %sren %da"%(int(self.urtea), self.processHilabetea(), int(self.eguna))
