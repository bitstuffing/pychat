# pyChat

It's a python library that can be used to import in other projects, without any API key, and with free internet partners.

You can add this simply selecting a provider and making a query search.


# Renew

The new idea is increase support with new providers which give you modern models:

- GPT o1, GPT o1-mini, GPT-4o
- DeepThink (R1) with web search
- Claude 3.5 Sonnet
- GPT-4o mini
- Copilot 

...

# History

This project start with a try to be a free library to create a python assistant with GPT4 and other providers like Bing Search, Watson Speech to Text, Bing Speech to Text, Google Text to Speech and more.

Now the time has increased the number of models and the support of old pages are better (someones) removed and replaced than use GPT4 or other models. If you want to use this there is a lot of providers (in this project) that use old models (GPT4, GPT3.5, Old Bing Search Engine with GPT4...) and text-to-speech, also speech-to-text (it's working fine with Bing and Google providers)


# Example of use

Select a provider and use it:

```python
from core.bing import Bing
b=Bing()
b.init_conversation("hello")
```

and you will see:

```bash
BingMessageType1, author: bot, message: Hi
BingMessageType1, author: bot, message: Hi there
BingMessageType1, author: bot, message: Hi there!
BingMessageType1, author: bot, message: Hi there! How
BingMessageType1, author: bot, message: Hi there! How can
BingMessageType1, author: bot, message: Hi there! How can I
BingMessageType1, author: bot, message: Hi there! How can I assist
BingMessageType1, author: bot, message: Hi there! How can I assist you
BingMessageType1, author: bot, message: Hi there! How can I assist you today
BingMessageType1, author: bot, message: Hi there! How can I assist you today?
BingMessageType1, author: bot, message: Hi there! How can I assist you today? 😊
BingMessageType1, author: bot, message: Hi there! How can I assist you today? 😊
```

A queue with the stream will be created, you can catch it to get the stream in real time.

or:

```python
from core.wrtnai import WRTNAI
w=WRTNAI()
w.create_conversation()
w.sendMessage("hello")
```

with the queue:

```bash
response: 42/v1/guest-chat,["data",{"chunk":"Hello"}]
Hello
response: 42/v1/guest-chat,["data",{"chunk":"Hello !"}]
Hello !
response: 42/v1/guest-chat,["data",{"chunk":"Hello!  How"}]
Hello!  How
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How "}]
Hello! How 
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How can  뤼"}]
Hello! How can  뤼
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How can 뤼 튼"}]
Hello! How can 뤼 튼
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How can 뤼튼 "}]
Hello! How can 뤼튼 
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How can 뤼튼  assist"}]
Hello! How can 뤼튼  assist
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How can 뤼튼 assist "}]
Hello! How can 뤼튼 assist 
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How can 뤼튼 assist  you"}]
Hello! How can 뤼튼 assist  you
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How can 뤼튼 assist you  today"}]
Hello! How can 뤼튼 assist you  today
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How can 뤼튼 assist you today ?"}]
Hello! How can 뤼튼 assist you today ?
response: 42/v1/guest-chat,["data",{"chunk":"Hello! How can 뤼튼 assist you today?"}]
Hello! How can 뤼튼 assist you today?
```
Or:

```python
from core.chatgptspanish import ChatGPTSpanish
c=ChatGPTSpanish()
c.send_message("hello")
```

```bash
'¡Hola! ¿En qué puedo ayudarte hoy?'
```

You're able to manage it, because it's an stream, you could get the last element, wait... do what you want in real time, or simply display it.


# License

This project is licensed under the terms of the CC BY-NC-ND 4.0 license, and released by @bitstuffing with love.

It's a open development in an investigation phase, and it's not allowed for business use.