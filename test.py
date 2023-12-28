realPetitionPromptNew = "¿qué modelo de lenguaje estás utilizando? ¿chatgpt3 o chatgpt4?"

from core.watson import Watson
watson = Watson()
watson.speech_to_text()

from core.openchat import OpenChat
openchat = OpenChat()
openchat.send_message(realPetitionPromptNew, stream=True)


from core.bing import Bing
bing = Bing()

bing.speech_to_text()

bing.init_conversation(realPetitionPromptNew)


from core.translator import Translator
translator = Translator()
translator.play(realPetitionPromptNew)
