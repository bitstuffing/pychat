# pyChat

This project tries to be a free library to create a python assistant with GPT4 and other providers like Bing Search, Watson Speech to Text, Bing Speech to Text, Google Text to Speech and more.

In a summary, it's a python library that can be used to create a python assistant.

## Why pyChat?

I always want to know how the things works, and other libraries don't show you how the things works. 

I want to offer an updated library with some free models, to use it for free, and all will be open source.

Some other projects provide libraries to create promps with GPT4, but they are complicated, unsupported and not really fixed, because these providers try to have your data.

Actually, it's a library that can be used in any python project, but it will became a complete assistant with GUI in the future.

### Real AI, including ChatGPT-4 free models

There are a lot of libraries and other stuff you can use in Internet with ads saying you that his service uses GPT-4, and it's a lie. 

GPT-4 is a paid model, and not all people want afford it in his home. Of course, not all people is a business to use it. 

But there are some providers/models that are free to use. This development tries to support that.

# Development

Currently it's a library for investigation purposes, regarding to obtain a real python assistant, a multiplatform library with GUI that can be used for free for any user.

## Which parts are being implemented?

GPT4 assistants:
- [x] ChatGPT4 providers (with conversation memory)
- [x] Bing Search (needs Firefox installed and X environment, at least first time)

Speech-to-text:
- [x] Watson Speech to Text
- [x] Bing Speech to Text

Text-to-speech:
- [x] Google Text to Speech

## How test it?

Now I'm developing a multiplatform GUI (Toga) for that reasons:

![Odd GUI](https://i.ibb.co/q7jDv4W/Captura-desde-2023-12-29-17-56-35.png)

if you want to test it, launch:
    
```bash
briefcase update
briefcase run linux
```

or 
    
```bash
briefcase dev
```

There was a test.py file that could be used to test the library. 

For instance:

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
