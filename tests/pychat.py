# pytest test file with functionalities of the core modules
# At this moment it requires to have an user validation manually
# because voice recognition and timeout prompts are implemented for
# security reasons. In a future, it will be automatized.

import queue
from core.watson import Watson
from core.openchat import OpenChat
from core.bing import Bing
from core.translator import Translator
from core.wrtnai import WRTNAI
from core.gpt4free import Gpt4free

realPetitionPromptNew = "¿qué modelo de lenguaje estás utilizando? ¿chatgpt3 o chatgpt4?"

watson = Watson()
watson.speech_to_text()

openchat = OpenChat()
openchat.send_message(realPetitionPromptNew, stream=True)

wrtnai = WRTNAI()
wrtnai.prompt(realPetitionPromptNew)


queue=queue.Queue()
gpt4free=Gpt4free()
gpt4free.prompt(realPetitionPromptNew,queue=queue)

bing = Bing()
bing.speech_to_text()
bing.init_conversation(realPetitionPromptNew)

translator = Translator()
translator.play(realPetitionPromptNew)
