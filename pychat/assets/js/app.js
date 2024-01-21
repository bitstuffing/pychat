function b64DecodeUnicode(str) {
    // Going backwards: from bytestream, to percent-encoding, to original string.
    return decodeURIComponent(atob(str).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
}

function updateChatMessageNode(id, message) {
    // update and decode base64 string message 
    message = b64DecodeUnicode(message);
    var reader = new commonmark.Parser();
    var writer = new commonmark.HtmlRenderer();
    var content = reader.parse(message);
    var text = writer.render(content);
    document.getElementById(id).innerHTML = text;
    scrollToBottom();    
}

function createChatMessageNode(id, name, message, imageUrl) {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'chat_container_board';

    const personContainer = document.createElement('div');
    personContainer.className = 'chat_message';

    const avatar = document.createElement('div');
    avatar.className = 'chat_message__avatar';
    const avatarImg = document.createElement('img');
    avatarImg.src = imageUrl;
    avatarImg.alt = name;
    avatar.appendChild(avatarImg);

    const nickname = document.createElement('span');
    nickname.className = 'chat_message__nickname';
    nickname.textContent = name;

    personContainer.appendChild(avatar);
    personContainer.appendChild(nickname);

    const messageContext = document.createElement('div');
    messageContext.className = 'chat_context';

    const messageBubble = document.createElement('div');
    messageBubble.className = 'chat_bubble';
    const messageText = document.createElement('span');
    messageText.id = id;
    messageText.textContent = message;
    messageBubble.appendChild(messageText);

    messageContext.appendChild(messageBubble);

    const options = document.createElement('div');
    options.className = 'chat_options';

    const emojiButton = document.createElement('button');
    emojiButton.className = 'btn-icon chat_board__message__option-button option-item emoji-button';
    const emojiSvg = document.createElement('svg');
    emojiSvg.className = 'feather feather-smile sc-dnqmqq jxshSx';
    emojiSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    emojiSvg.setAttribute('width', '24');
    emojiSvg.setAttribute('height', '24');
    emojiSvg.setAttribute('viewBox', '0 0 24 24');
    emojiSvg.setAttribute('fill', 'none');
    emojiSvg.setAttribute('stroke', 'currentColor');
    emojiSvg.setAttribute('stroke-width', '2');
    emojiSvg.setAttribute('stroke-linecap', 'round');
    emojiSvg.setAttribute('stroke-linejoin', 'round');
    emojiSvg.setAttribute('aria-hidden', 'true');

    const circle1 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle1.setAttribute('cx', '12');
    circle1.setAttribute('cy', '12');
    circle1.setAttribute('r', '10');

    const path1 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path1.setAttribute('d', 'M8 14s1.5 2 4 2 4-2 4-2');

    const line1 = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line1.setAttribute('x1', '9');
    line1.setAttribute('y1', '9');
    line1.setAttribute('x2', '9.01');
    line1.setAttribute('y2', '9');

    const line2 = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line2.setAttribute('x1', '15');
    line2.setAttribute('y1', '9');
    line2.setAttribute('x2', '15.01');
    line2.setAttribute('y2', '9');

    emojiSvg.appendChild(circle1);
    emojiSvg.appendChild(path1);
    emojiSvg.appendChild(line1);
    emojiSvg.appendChild(line2);

    emojiButton.appendChild(emojiSvg);

    const moreButton = document.createElement('button');
    moreButton.className = 'btn-icon chat_board__message__option-button option-item more-button';
    const moreSvg = document.createElement('svg');
    moreSvg.className = 'feather feather-more-horizontal sc-dnqmqq jxshSx';
    moreSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    moreSvg.setAttribute('width', '24');
    moreSvg.setAttribute('height', '24');
    moreSvg.setAttribute('viewBox', '0 0 24 24');
    moreSvg.setAttribute('fill', 'none');
    moreSvg.setAttribute('stroke', 'currentColor');
    moreSvg.setAttribute('stroke-width', '2');
    moreSvg.setAttribute('stroke-linecap', 'round');
    moreSvg.setAttribute('stroke-linejoin', 'round');
    moreSvg.setAttribute('aria-hidden', 'true');

    const circle2 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle2.setAttribute('cx', '12');
    circle2.setAttribute('cy', '12');
    circle2.setAttribute('r', '1');

    const circle3 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle3.setAttribute('cx', '19');
    circle3.setAttribute('cy', '12');
    circle3.setAttribute('r', '1');

    const circle4 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle4.setAttribute('cx', '5');
    circle4.setAttribute('cy', '12');
    circle4.setAttribute('r', '1');

    moreSvg.appendChild(circle2);
    moreSvg.appendChild(circle3);
    moreSvg.appendChild(circle4);

    moreButton.appendChild(moreSvg);

    options.appendChild(emojiButton);
    options.appendChild(moreButton);

    messageContainer.appendChild(personContainer);
    messageContainer.appendChild(messageContext);
    messageContainer.appendChild(options);

    const parentElement = document.getElementById('message-container');
    parentElement.appendChild(messageContainer);
    
}

function createChatMessageNodeUser(name, message, imageUrl) {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'chat_container_board reversed';

    const personContainer = document.createElement('div');
    personContainer.className = 'chat_message';

    const avatar = document.createElement('div');
    avatar.className = 'chat_message__avatar';
    const avatarImg = document.createElement('img');
    avatarImg.src = imageUrl;
    avatarImg.alt = name;
    avatar.appendChild(avatarImg);

    const nickname = document.createElement('span');
    nickname.className = 'chat_message__nickname';
    nickname.textContent = name;

    personContainer.appendChild(avatar);
    personContainer.appendChild(nickname);

    const messageContext = document.createElement('div');
    messageContext.className = 'chat_context';

    const messageBubble = document.createElement('div');
    messageBubble.className = 'chat_bubble';
    const messageText = document.createElement('span');
    messageText.textContent = message;
    messageBubble.appendChild(messageText);

    messageContext.appendChild(messageBubble);

    const options = document.createElement('div');
    options.className = 'chat_options';

    const emojiButton = document.createElement('button');
    emojiButton.className = 'btn-icon chat_board__message__option-button option-item emoji-button';
    const emojiSvg = document.createElement('svg');
    emojiSvg.className = 'feather feather-smile sc-dnqmqq jxshSx';
    emojiSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    emojiSvg.setAttribute('width', '24');
    emojiSvg.setAttribute('height', '24');
    emojiSvg.setAttribute('viewBox', '0 0 24 24');
    emojiSvg.setAttribute('fill', 'none');
    emojiSvg.setAttribute('stroke', 'currentColor');
    emojiSvg.setAttribute('stroke-width', '2');
    emojiSvg.setAttribute('stroke-linecap', 'round');
    emojiSvg.setAttribute('stroke-linejoin', 'round');
    emojiSvg.setAttribute('aria-hidden', 'true');

    const circle1 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle1.setAttribute('cx', '12');
    circle1.setAttribute('cy', '12');
    circle1.setAttribute('r', '10');

    const path1 = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path1.setAttribute('d', 'M8 14s1.5 2 4 2 4-2 4-2');

    const line1 = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line1.setAttribute('x1', '9');
    line1.setAttribute('y1', '9');
    line1.setAttribute('x2', '9.01');
    line1.setAttribute('y2', '9');

    const line2 = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line2.setAttribute('x1', '15');
    line2.setAttribute('y1', '9');
    line2.setAttribute('x2', '15.01');
    line2.setAttribute('y2', '9');

    emojiSvg.appendChild(circle1);
    emojiSvg.appendChild(path1);
    emojiSvg.appendChild(line1);
    emojiSvg.appendChild(line2);

    emojiButton.appendChild(emojiSvg);

    const moreButton = document.createElement('button');
    moreButton.className = 'btn-icon chat_board__message__option-button option-item more-button';
    const moreSvg = document.createElement('svg');
    moreSvg.className = 'feather feather-more-horizontal sc-dnqmqq jxshSx';
    moreSvg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    moreSvg.setAttribute('width', '24');
    moreSvg.setAttribute('height', '24');
    moreSvg.setAttribute('viewBox', '0 0 24 24');
    moreSvg.setAttribute('fill', 'none');
    moreSvg.setAttribute('stroke', 'currentColor');
    moreSvg.setAttribute('stroke-width', '2');
    moreSvg.setAttribute('stroke-linecap', 'round');
    moreSvg.setAttribute('stroke-linejoin', 'round');
    moreSvg.setAttribute('aria-hidden', 'true');

    const circle2 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle2.setAttribute('cx', '12');
    circle2.setAttribute('cy', '12');
    circle2.setAttribute('r', '1');

    const circle3 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle3.setAttribute('cx', '19');
    circle3.setAttribute('cy', '12');
    circle3.setAttribute('r', '1');

    const circle4 = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle4.setAttribute('cx', '5');
    circle4.setAttribute('cy', '12');
    circle4.setAttribute('r', '1');

    moreSvg.appendChild(circle2);
    moreSvg.appendChild(circle3);
    moreSvg.appendChild(circle4);

    moreButton.appendChild(moreSvg);

    options.appendChild(emojiButton);
    options.appendChild(moreButton);

    messageContainer.appendChild(personContainer);
    messageContainer.appendChild(messageContext);
    messageContainer.appendChild(options);

    const parentElement = document.getElementById('message-container');
    parentElement.appendChild(messageContainer);
}

function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}

document.addEventListener("DOMContentLoaded", function() {
    //createChatMessageNode('bot', "message", 'https://randomuser.me/api/portraits/men/32.jpg');
    //createChatMessageNodeUser('User', "message answer", 'https://randomuser.me/api/portraits/men/9.jpg');
});