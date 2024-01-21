# pyChat

This project tries to be a free library to create a python assistant with GPT4 and other providers like Bing Search, Watson Speech to Text, Bing Speech to Text, Google Text to Speech and more.

It's a python library that can be used to import in other projects, without any API key, and with free internet partners.

## Models engine implemented

| Provider | GPT3.5 | GPT4 | C. Memory | I. Browser | Stream | Working | Notes |
|------------|------------|------------|------------|------------|------------|------------|------------|
| OpenChat | ✘ | ✔ | ✔ | ✘ | ✔ | ✔ | |
| GPT4FREE | ✘ | ✔ | ✔ | ✘ | ✔ | ✔ | English provider|
| Wrtn  | ✔ | ✔ | ✘  | ✘  | ✔ | ✔ | South Korean provider (so you have to require in your command the answer in your language if you don't want to read in Korean) |
| ChatGPTSpanish | ✔ | ✔ | ✘ | ✘ | ✘ | ✔ | You're able to ask one time per petition, but you can clean and ask again |
| You | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | GPT-4 promps are limited to 5 per account, but support auto register a random account |
| Bing  | ✔ | ✔ | ✘ | ✔ | ✔ | ✔ | Automatized with Firefox and Linux (required to solve captcha and get a validated cookie) |
|  |  |  |  |  |  |  |  |

## Speech to text engines

| Provider | Working |
|------------|------------|
| Watson | ✔  |
| Bing | ✔ |

## Text to speech engine

| Provider | Working |
|------------|------------|
| Google | ✔  |


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


### Real AI, including ChatGPT-4 free models

There are a lot of libraries and other stuff you can use in Internet with ads saying you that his service uses GPT-4, and it's a lie. 

GPT-4 is a paid model, and not all people want afford it in his home. Of course, not all people is a business to use it. 

But there are some providers/models that are free to use. This development tries to support that.

### GUI frameworks

Now I'm centered in core functionalities, but I've tried to develop a multiplatform GUI:

![WebView GUI](https://i.ibb.co/pjbMq8c/Captura-desde-2024-01-06-22-59-58.png)

With a working mobile version:

![Mobile GUI](https://i.ibb.co/NFsRKVb/photo-2024-01-01-21-41-27.jpg)

Briefcase/Toga/Gbulb has a ![bug](https://github.com/beeware/gbulb/issues/116) with aiohttp and GTK (related to his subproject gbulb, that it has not implement very well wss throw ssl),
so I will discart it until it's fixed (and apparently developers know it from 2 years before and don't want solve it, for me it's unsupported framework with bugs, 
and I tried to fix it, without success, and I'm not the first one ![to try it](https://github.com/beeware/gbulb/pull/60)).

If you want know about how to use it with Toga/Briefcase take a look about this [commit](https://github.com/bitstuffing/pychat/tree/a7f715f9040323538998e2b9fe520e91fbbdb4d7)


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
