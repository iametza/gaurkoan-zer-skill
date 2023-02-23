from mycroft import MycroftSkill, intent_file_handler

import requests

class GaurkoanZer(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)
        self.api = Api()

    @intent_file_handler('zer.gaurkoan.intent')

    def handle_zer_gaurkoan(self, message):
        efemerideak = self.api.getEfemerideak()

        #self.speak_dialog('zer.gaurkoan')
        self.speak('Gaurko egunez %d efemeride aurkitu ditut'%(len(efemerideak['data'])))

        for efemeridea in efemerideak['data']:
            self.speak(efemeridea['izena'])

    @intent_file_handler('aste.honetan.zer.intent')

    def handle_aste_honetan_zer(self, message):
        efemerideak = self.api.getEfemerideak('astekoak')

        self.speak('Aste honetan %d efemeride aurkitu ditut'%(len(efemerideak['data'])))

        for efemeridea in efemerideak['data']:
            self.speak(efemeridea['izena'])

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