from mycroft import MycroftSkill, intent_file_handler


class GaurkoanZer(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('zer.gaurkoan.intent')
    
    def handle_zer_gaurkoan(self, message):
        self.speak_dialog('zer.gaurkoan')


def create_skill():
    return GaurkoanZer()

