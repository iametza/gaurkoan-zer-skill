from mycroft import MycroftSkill, intent_file_handler

import requests

class GaurkoanZer(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)
        self.api = Api()
        self.efemerideak = 0

    @intent_file_handler('zer.gaurkoan.intent')

    def handle_zer_gaurkoan(self, message):
        self.get_efemerideak('gaurkoak')
        self.print_efemerideak('Gaurko egunez %d efemeride aurkitu ditut')

    @intent_file_handler('aste.honetan.zer.intent')

    def handle_aste_honetan_zer(self, message):
        self.get_efemerideak('astekoak')
        self.print_efemerideak('Aste honetan %d efemeride aurkitu ditut')

    @intent_file_handler('hilabete.honetan.zer.intent')

    def handle_hilabete_honetan_zer(self, message):
        self.get_efemerideak('hilekoak')
        self.print_efemerideak('Hilabete honetan %d efemeride aurkitu ditut')

    @intent_file_handler('informazio.gehiago.intent')

    def handle_informazio_gehiago(self, message):
        if not self.efemerideak:
            self.speak("Ez dago efemeriderik sakontzeko")

        else:
            for efemeridea in self.efemerideak['data']:
                egutegia = Egutegia(efemeridea['data'])
                self.speak(egutegia.getProcessed() + ' ' + efemeridea['azalpena'])

    def get_efemerideak(self, tartea, mota = 0):
        self.tartea = tartea
        self.efemerideak = self.api.getEfemerideak(self.tartea, mota)
        return self.efemerideak

    def get_efemerideak_mota(self, mota):
        self.mota = mota
        self.efemerideak = self.api.getMotaEfemerideak(mota)
        return self.efemerideak

    def print_efemerideak(self, testua = ''):

        if testua != '':
            self.speak(testua%(len(self.efemerideak['data'])))

        # @todo: Paginazioa dagoen kasuan denak rekorritu beharko genituzke
        if self.efemerideak:
            for efemeridea in self.efemerideak['data']:
                egutegia = Egutegia(efemeridea['data'])
                self.speak(egutegia.getProcessed() + ' ' + efemeridea['izena'])

    @intent_file_handler('gaurko.pertsonaia.intent')

    def handle_gaurko_pertsonaia(self, message):
        # Gaurko efemerideak eskuratu
        self.get_efemerideak('gaurkoak')

        # Gaurko efemerideen pertsonaian eskuratu
        self.pertsonaiak = set()
        for efemeridea in self.efemerideak['data']:
            for pertsonaia in efemeridea['pertsonaiak']:
                self.pertsonaiak.update([pertsonaia['id']])

        # Pertsonaien informazioa eskuratu eta inprimatu
        for pertsonaia in self.pertsonaiak:
            pertsonaia = self.api.getPertsonaia(pertsonaia)
            pertsonaia = pertsonaia['data'][0]
            self.speak('. '.join([pertsonaia['izena'], 
                                  pertsonaia['jaiotze_data'], 
                                  pertsonaia['jaioterria'],
                                  pertsonaia['biografia']]))

    @intent_file_handler('jaiotzak.intent')

    def handle_jaiotzak(self, message):
        self.get_efemerideak('gaurkoak', 2) # 2: Jaiotzak mota, 'hardcoded', sorry ^^
        self.print_efemerideak('Gaur %d jaiotza aurkitu ditut')

    def stop(self):
        pass


def create_skill():
    return GaurkoanZer()

class Api:
    url = 'https://gaurkoanzer.eus/api'
    version = 'v1'

    def getEfemeridea(self, id = 0):
        self.method = 'efemerideak'
        return self.doCall('/' + str(id))
    
    def getEfemerideak(self, tartea = 'gaurkoak', mota = 0):
        self.method = 'efemerideak'
        filtroak = '?tartea=' + tartea
        if mota != 0:
            filtroak = filtroak + '&mota_id=' + str(mota)
        return self.doCall(filtroak)

    def getPertsonaia(self, id = 0):
        self.method = 'pertsonaiak'
        return self.doCall('/' + str(id))

    def getPertsonaiak(self, id = 0):
        self.method = 'pertsonaiak'
        return self.doCall()

    def getMota(self, id = 0):
        self.method = 'motak'
        return self.doCall('/' + str(id))

    def getMotak(self, id = 0):
        self.method = 'motak'
        return self.doCall()

    def getMotaEfemerideak(self, id = 0):
        self.method = 'motak'
        return self.doCall('/' + str(id) + '/efemerideak')

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
