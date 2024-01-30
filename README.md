# pyChat

This project tries to be a free library to create a python assistant with GPT4 and other providers like Bing Search, Watson Speech to Text, Bing Speech to Text, Google Text to Speech and more.

It's a python library that can be used to import in other projects, without any API key, and with free internet partners.

## Models engine implemented

| Provider | GPT3.5 | GPT4 | C. Memory | I. Browser | Stream | Working | In GUI | Notes |
|------------|------------|------------|------------|------------|------------|------------|------------|------------|
| OpenChat | ✘ | ✔ | ✔ | ✘ | ✔ | ✔ | ✔ | Sometimes online services is down for maintenance |
| Bing  | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Automatized captcha solver with pySide6 GUI (Desktop), and prompt (last one needs Firefox and Linux)  |
| GPT4FREE | ✘ | ✔ | ✔ | ✘ | ✔ | ✔ | ✔ | English by default |
| Wrtn  | ✔ | ✔ | ✘  | ✘  | ✔ | ✔ | ✔ | South Korean by default (so you have to require in your command the answer in your language if you don't want to read in Korean) |
| ChatGPTSpanish | ✔ | ✔ | ✘ | ✘ | ✘ | ✔ | ✔ | You're able to ask one time per petition, but you can clean and ask again |
| You | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | GPT-4 promps needs login and are limited to 5 per account, but supports auto register a random account and login |
| ch4  | ✔ | ✔ | ✔ | ✘ | ✔ | ✔ | ✘ | It's too slow, even streaming, but works. Needs to be logged in (you've auto-registration, but it's preferible use always the same cookie). Sometimes platform forces using Gemini-Pro, but... it's a platform bug. |
|  |  |  |  |  |  |  |  |  |

## Speech to text engines

| Provider | Working | In GUI |
|------------|------------|------------|
| Watson | ✔ | ✘ |
| Bing | ✔ | ✔ |
|  |  |  | 

## Text to speech engine

| Provider | Working | In GUI |
|------------|------------|------------|
| Google | ✔  | ✘ |
|  |  |  | 


# How to use it (future wiki section)

There is a pytest file that could be used to test the library. Anyway you can use it for your own tests, for instance:

```python

realPetitionPromptNew = "¿qué modelo de lenguaje estás utilizando? ¿chatgpt3 o chatgpt4?"

# You
from core.you import You
you=You()
you.send_message(realPetitionPromptNew, stream=True)

# openchat
from core.openchat import OpenChat
openchat = OpenChat()
openchat.send_message(realPetitionPromptNew, stream=True)

# wrtn.ai
from core.wrtnai import WRTNAI
wrtnai = WRTNAI()
wrtnai.prompt(realPetitionPromptNew)

# gpt4free.io/chat
from core.gpt4free import Gpt4free
gpt4free=Gpt4free()
gpt4free.prompt(realPetitionPromptNew)

# chatgptspanish
from core.chatgptspanish import ChatGPTSpanish
chatgptspanish = ChatGPTSpanish()
chatgptspanish.send_message(realPetitionPromptNew)

# ch4
from core.ch4usto import Ch4usto
c=Ch4usto()
c.send_message(realPetitionPromptNew)

# Bing
from core.bing import Bing
bing = Bing()
# Bing speech to text
bing.speech_to_text()
# BingGPT AI
bing.init_conversation(realPetitionPromptNew)

# Watson speech to text
from core.watson import Watson
watson = Watson()
watson.speech_to_text()

# Google text to speech
from core.translator import Translator
translator = Translator()
translator.play(realPetitionPromptNew)

```
And enjoy it!

### Streams

In this kind of APIs you will concern the `streaming` ability to get a `real time` response. In this library with the partners which provide `streaming` you have to add a queue:

```
import queue
myQueue = queue.Queue()
```

and use it:

```
from core.wrtnai import WRTNAI
wrtnai = WRTNAI()
wrtnai.prompt(cmd=realPetitionPromptNew, queue=myQueue, stream=True)
```

Queue could be read from outside if you consider use asyncio implementation.

## Developer notes 

## Why?

I always want to know how the things works, and other libraries don't show you how the things works. 

I want to offer an updated library with some free models, to use it for free, and all will be open source.

### GUI frameworks

Now I'm centered in core functionalities, but I've tried to develop a multiplatform GUI:

![GUI](https://i.ibb.co/vPpfDWh/Captura-desde-2024-01-24-21-25-57.png)


Currently I'm working on poetry and pySide6 multiplatform GUI. To build it run:
```
curl -sSL https://install.python-poetry.org | python -
python -m poetry shell
pip install -r requirements.txt
poetry update
poetry install
poetry run gui
```

But if you want to make all in two commands, make it easy:
```
pip install -r requirements.txt
python main.py
```

And enjoy.


### dev Briefcase issues

In the past I used Briefcase with Toga. It was an awesome project but Briefcase/Toga/Gbulb-GTK has some ![bugs](https://github.com/beeware/gbulb/issues/116) with aiohttp and asyncio calls in GTK (related to his subproject gbulb, that it has not implement very well wss throw ssl, and toga-gtk, forgiven too many time for developers),
so I discarted it officially. I tried to fix it, without success, and I'm not the first one ![to try it](https://github.com/beeware/gbulb/pull/60)). So, multiplatform GUI was implemented but unsupported with briefcase.

With a working mobile version:

![Mobile GUI](https://i.ibb.co/NFsRKVb/photo-2024-01-01-21-41-27.jpg)

If you want know about how to use it with Toga/Briefcase take a look about this [commit](https://github.com/bitstuffing/pychat/tree/a7f715f9040323538998e2b9fe520e91fbbdb4d7) in the README.md file.


### PIP issues

In ArchLinux pip is configured to be used with --break-system-packages or system, buildozer needs a fix.
Edit ~/.config/pip/pip.conf

```
[global]
break-system-packages = true
```

And enjoy it!

# License

This project is licensed under the terms of the [CC BY-NC-ND 4.0](http://creativecommons.org/licenses/by-nc-nd/4.0/?ref=chooser-v1) license, and released by [@bitstuffing](https://github.com/bitstuffing) with love. 

It's a open development in an investigation phase, and it's not allowed for business use. 
