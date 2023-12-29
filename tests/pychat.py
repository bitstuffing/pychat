#from core.watson import Watson
from core.openchat import OpenChat
from core.bing import Bing
from core.translator import Translator

#def test_library_function():
realPetitionPromptNew = "¿qué modelo de lenguaje estás utilizando? ¿chatgpt3 o chatgpt4?"


#watson = Watson()
#watson.speech_to_text()


openchat = OpenChat()
openchat.send_message(realPetitionPromptNew, stream=True)



bing = Bing()

#bing.speech_to_text()

bing.init_conversation(realPetitionPromptNew)



translator = Translator()
translator.play(realPetitionPromptNew)
