# pyChat

This project tries to be a free library to create a python assistant with GPT4 and other providers like Bing Search, Watson Speech to Text, Bing Speech to Text, Google Text to Speech and more.

In a summary, it's a python library that can be used to create a python assistant, without any API key, and with free models.


## Why pyChat?

I always want to know how the things works, and other libraries don't show you how the things works. 

I want to offer an updated library with some free models, to use it for free, and all will be open source.

## How test it?

Now I'm centered in core, but I've tried to develop a multiplatform GUI:

![WebView GUI](https://i.ibb.co/pjbMq8c/Captura-desde-2024-01-06-22-59-58.png)

With a working mobile version:

![Mobile GUI](https://i.ibb.co/NFsRKVb/photo-2024-01-01-21-41-27.jpg)

Briefcase/Toga/Gbulb has a ![bug](https://github.com/beeware/gbulb/issues/116) with aiohttp and GTK (related to his subproject gbulb, that it has not implement very well wss throw ssl),
so I will discart it until it's fixed (and apparently developers know it from 2 years before and don't want solve it, for me it's unsupported framework with bugs, 
and I tried to fix it, without success, and I'm not the first one ![to try it](https://github.com/beeware/gbulb/pull/60)).

So I declined use it, and I will study integrate pyside6 or similars (it's not decided yet).

### Real AI, including ChatGPT-4 free models

There are a lot of libraries and other stuff you can use in Internet with ads saying you that his service uses GPT-4, and it's a lie. 

GPT-4 is a paid model, and not all people want afford it in his home. Of course, not all people is a business to use it. 

But there are some providers/models that are free to use. This development tries to support that.

## Which parts are being implemented?

GPT4 assistants:
- [x] ChatGPT4 providers (with conversation memory)
- [x] Bing Search (needs Firefox installed and X environment, at least first time)

Speech-to-text:
- [x] Watson Speech to Text
- [x] Bing Speech to Text

Text-to-speech:
- [x] Google Text to Speech

# Development

There was a test.py file that could be used to test the library. Anyway you can use it for your own tests, for instance:

```python

realPetitionPromptNew = "¿qué modelo de lenguaje estás utilizando? ¿chatgpt3 o chatgpt4?"

# Test ChatGPT4
from core.openchat import OpenChat
openchat = OpenChat()
openchat.send_message(realPetitionPromptNew, stream=True)

# Test Bing Assistant 
from core.bing import Bing
bing = Bing()
# Test Bing speech to text
bing.speech_to_text()

# Test BingGPT AI
bing.init_conversation(realPetitionPromptNew)

# Test Watson speech to text
from core.watson import Watson
watson = Watson()
watson.speech_to_text()

# Test Google text to speech
from core.translator import Translator
translator = Translator()
translator.play(realPetitionPromptNew)

```

And enjoy it!

## Developer issues

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
