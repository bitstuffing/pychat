
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
        if "type" in response: 
            if response.get('type') == 1:
                self.chatmessage = BingMessageType1(
                    response.get('type'),
                    response.get('target'),
                    response.get('arguments')
                )
            elif response.get('type') == 2:
                self.chatmessage = BingMessageType2(
                    response.get('type'),
                    response.get('invocationId'),
                    response.get('item')
                )
class BingMessageType:
    def __init__(self,type,invocationId):
        self.type = type
        self.invocationId = invocationId

class BingMessageType2(BingMessageType):
    def __init__(self,type,invocationId,item):
        super().__init__(type,invocationId)
        self.item = BingItem(item.get('messages'),item.get('firstNewMessageIndex'),item.get('defaultChatName'),item.get('conversationId'),item.get('requestId'),item.get('conversationExpiryTime'),item.get('shouldInitiateConversation'),item.get('telemetry'),item.get('throttling'),item.get('result'))
        
class BingItem:
    def __init__(self, messages, firstNewMessageIndex, defaultChatName, conversationId, requestId, conversationExpiryTime, shouldInitiateConversation, telemetry, throttling, result):
        messages_ = []
        for message in messages:
            chatmessage = ChatMessage(
                message.get('text'),
                message.get('author'),
                message.get('createdAt'),
                message.get('timestamp'),
                message.get('messageId'),
                message.get('requestId'),
                message.get('offense')
            )
            messages_.append(chatmessage)
        self.messages = messages_
        self.firstNewMessageIndex = firstNewMessageIndex
        self.defaultChatName = defaultChatName
        self.conversationId = conversationId
        self.requestId = requestId
        self.conversationExpiryTime = conversationExpiryTime
        self.shouldInitiateConversation = shouldInitiateConversation
        self.telemetry = BingTelemetry(telemetry.get('startTime'))
        self.throttling = BingThrottling(throttling.get('maxNumUserMessagesInConversation'),throttling.get('numUserMessagesInConversation'),throttling.get('maxNumLongDocSummaryUserMessagesInConversation'), throttling.get('numLongDocSummaryUserMessagesInConversation'))
        self.result = BingResult(result.get('value'),result.get('message'),result.get('serviceVersion'))

class BingTelemetry:
    def __init__(self,startTime):
        self.startTime = startTime

class BingThrottling:
    def __init__(self,maxNumUserMessagesInConversation,numUserMessagesInConversation,maxNumLongDocSummaryUserMessagesInConversation,numLongDocSummaryUserMessagesInConversation):
        self.maxNumUserMessagesInConversation = maxNumUserMessagesInConversation
        self.numUserMessagesInConversation = numUserMessagesInConversation
        self.maxNumLongDocSummaryUserMessagesInConversation = maxNumLongDocSummaryUserMessagesInConversation
        self.numLongDocSummaryUserMessagesInConversation = numLongDocSummaryUserMessagesInConversation                      

class BingResult:
    def __init__(self,value,message,serviceVersion):
        self.value = value
        self.message = message
        self.serviceVersion = serviceVersion

class BingMessageType1:
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
            self.requestId = argument.get('requestId')

class ChatMessage:
    def __init__(self, text = "", author = "", createdAt = "", timestamp = "", messageId = "", requestId = "", offense = "", 
            adaptativeCards = [], sourceAttributions = [], feedback = None, contentOrigin = None, scores = None, suggestedResponses = None
            #TODO put additional type2 arguments in this line with default value
            ):
        self.text = text
        self.author = author
        self.createdAt = createdAt
        self.timestamp = timestamp
        self.messageId = messageId
        self.requestId = requestId
        self.offense = offense
        if adaptativeCards is not None:
            adaptativeCards_ = []
            for adaptativeCard in adaptativeCards:
                adaptativeCard = AdaptativeCard(adaptativeCard.get('type'),adaptativeCard.get('version'),adaptativeCard.get('body'))
                adaptativeCards_.append(adaptativeCard)
            self.adaptativeCards = adaptativeCards_
        if sourceAttributions is not None:
            sourceAttributions_ = []
            for sourceAttribution in sourceAttributions:
                sourceAttribution = SourceAttribution(sourceAttribution.get('providerDisplayName'),sourceAttribution.get('seeMoreUrl'), sourceAttribution.get('searchQuery'), sourceAttribution.get('provider'))
                sourceAttributions_.append(sourceAttribution)
            self.sourceAttributions = sourceAttributions_
        if feedback is not None:
            self.feedback = Feedback(feedback.get('tag'),feedback.get('updatedOn'),feedback.get('type'))
        if contentOrigin is not None:
            self.contentOrigin = contentOrigin,
        if scores is not None:
            scores_ = []
            for score in scores:
                score = Score(score.get('component'),score.get('score'))
                scores_.append(score)
            self.scores = scores_
        if suggestedResponses is not None:
            suggestedResponses_ = []
            for suggestedResponse in suggestedResponses:
                suggested = SuggestedResponse(suggestedResponse.get('text'),suggestedResponse.get('author'), suggestedResponse.get('createdAt'), suggestedResponse.get('timestamp'), suggestedResponse.get('messageId'), suggestedResponse.get('messageType'), suggestedResponse.get('offense'), suggestedResponse.get('feedback'), suggestedResponse.get('contentOrigin'))
                suggestedResponses_.append(suggested)
            self.suggestedResponses = suggestedResponses_


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
        try:
            self.feedback = Feedback(feedback.get('tag'),feedback.get('updatedOn'),feedback.get('type'))
        except:
            pass
        self.contentOrigin = contentOrigin