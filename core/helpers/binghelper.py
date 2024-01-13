import json

class BingTextResponse:
    def __init__(self, text = None, offset = None, duration = None, recognitionStatus = None, displayText = None, primaryLanguage = None):
        self.text = text
        self.offset = offset
        self.duration = duration
        self.recognitionStatus = recognitionStatus
        self.displayText = displayText
        if primaryLanguage is not None:
            self.primaryLanguage = BingPrimaryLanguage(primaryLanguage.get('Language'),primaryLanguage.get('Confidence'))

class BingPrimaryLanguage:
    def __init__(self, language = None, confidence = None):
        self.language = language
        self.confidence = confidence

class BingResponse:
    def __init__(self, response):
        if "type" in response and response.get('type') == 1:
            self.chatmessage = BingMessage(
                response.get('type'),
                response.get('target'),
                response.get('arguments')
            )

class BingMessage:
    def __init__(self,type,target,arguments):
        self.type = type
        self.target = target
        self.arguments = ChatArguments(arguments)


class ChatArguments:
    def __init__(self,arguments):
        for argument in arguments:
            messages = []
            for message in argument.get('messages'):
                chatmessage = ChatMessage(
                    message.get('text'),
                    message.get('author'),
                    message.get('createdAt'),
                    message.get('timestamp'),
                    message.get('messageId'),
                    message.get('requestId'),
                    message.get('offense'),
                    message.get('adaptativeCards'),
                    message.get('sourceAttributions'),
                    message.get('feedback'),
                    message.get('contentOrigin'),
                    message.get('scores'),
                    message.get('suggestedResponses')
                )
                messages.append(chatmessage)
            self.messages = messages
            #self.requestId = arguments.get('requestId')

class ChatMessage:
    def __init__(self,text,author,createdAt,timestamp,messageId,requestId,offense,adaptativeCards, sourceAttributions, feedback, contentOrigin, scores, suggestedResponses):
        self.text = text
        self.author = author
        self.createdAt = createdAt
        self.timestamp = timestamp
        self.messageId = messageId
        self.requestId = requestId
        self.offense = offense
        adaptativeCards = []
        for adaptativeCard in adaptativeCards:
            adaptativeCard = AdaptativeCard(adaptativeCard.get('type'),adaptativeCard.get('version'),adaptativeCard.get('body'))
            adaptativeCards.append(adaptativeCard)
        self.adaptativeCards = adaptativeCards
        sourceAttributions = []
        for sourceAttribution in sourceAttributions:
            sourceAttribution = SourceAttribution(sourceAttribution.get('providerDisplayName'),sourceAttribution.get('seeMoreUrl'), sourceAttribution.get('searchQuery'), sourceAttribution.get('provider'))
            sourceAttributions.append(sourceAttribution)
        self.feedback = Feedback(feedback.get('tag'),feedback.get('updatedOn'),feedback.get('type'))
        self.contentOrigin = contentOrigin,
        scores = []
        for score in scores:
            score = Score(score.get('component'),score.get('score'))
            scores.append(score)
        self.scores = scores
        suggestedResponses = []
        for suggestedResponse in suggestedResponses:
            suggested = SuggestedResponse(suggestedResponse.get('text'),suggestedResponse.get('author'), suggestedResponse.get('createdAt'), suggestedResponse.get('timestamp'), suggestedResponse.get('messageId'), suggestedResponse.get('messageType'), suggestedResponse.get('offense'), suggestedResponse.get('feedback'), suggestedResponse.get('contentOrigin'))
            suggestedResponses.append(suggested)
        self.suggestedResponses = suggestedResponses


class AdaptativeCard:
    def __init__(self,type,version,body):
        self.type = type
        self.version = version
        body = []
        for body in body:
            body = Body(body.get('type'),body.get('text'), body.get('wrap'))
            body.append(body)

class Body:
    def __init__(self,type,text,wrap):
        self.type = type
        self.text = text
        self.wrap = wrap

class SourceAttribution:
    def __init__(self,providerDisplayName,seeMoreUrl,searchQuery,provider):
        self.providerDisplayName = providerDisplayName
        self.seeMoreUrl = seeMoreUrl
        self.searchQuery = searchQuery
        self.provider = provider

class Feedback:
    def __init__(self,tag,updatedOn,type):
        self.tag = tag
        self.updatedOn = updatedOn
        self.type = type

class Score:
    def __init__(self,component,score):
        self.component = component
        self.score = score

class SuggestedResponse:
    def __init__(self,text,author,createdAt,timestamp,messageId,messageType,offense,feedback,contentOrigin):
        self.text = text
        self.author = author
        self.createdAt = createdAt
        self.timestamp = timestamp
        self.messageId = messageId
        self.messageType = messageType
        self.offense = offense
        self.feedback = Feedback(feedback.get('tag'),feedback.get('updatedOn'),feedback.get('type'))
        self.contentOrigin = contentOrigin