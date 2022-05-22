/*
 * Chat controller
 * @author Oliver Kovarna
 */

var myChat = angular.module("myChat", ["ngSanitize"]);

myChat.controller("chatController", ['$scope', '$http', '$location', '$anchorScroll', '$timeout',
                  ($scope, $http, $location, $anchorScroll, $timeout) => {
    /*  SOCKET Client  */
    $scope.connectionOptions =  {
        "force new connection" : true,
        "reconnectionAttempts": "Infinity",
        "timeout" : 10000,
        secure: true
    };

    // initialize socket client and send a connect request to the socket server.
    $scope.socket = io.connect('https://' + document.domain + '/', $scope.connectionOptions);

    $scope.chatHistory = '';
    $scope.unreadMessagesBox;
    $scope.currentChatPartner = '';
    $scope.isNotificationBoxDisplayed = false;
    $scope.isPartnerTyping = false;

    $scope.input = document.querySelector('#emoji_btn');
    $scope.picker = new EmojiButton({
        position: 'top'
    });

    /*
     * The callback in the listener 'emoji' is used to concatenate the chosen emoji to the current
     * user text.
     *
     * @author Oliver Kovarna
     */
    $scope.picker.on('emoji', function(emoji) {
        let message = String(message_content.value);
        let message_arr = message.split('');
        message_arr.splice(message_content.selectionEnd, 0, emoji);
        message_content.value = message_arr.toString().replace(/,/g, '');
        $scope.textModel = message_arr.toString().replace(/,/g, '');
        $scope.trackChatUserActivity();
    });

    /*
     * The callback in the listener 'click' updates the visibility of the emoji picker.
     *
     * @author Oliver Kovarna
     */
    $scope.input.addEventListener('click', function() {
        $scope.picker.pickerVisible ? $scope.picker.hidePicker() : $scope.picker.showPicker($scope.input);
    });

    /*
     * The callback in the listener 'connect' is used to connect the client with the socket.
     * It emits an event on the socket server side and sends a certain message as well as the userId
     * to confirm its successful connection.
     *
     * @author Oliver Kovarna
     */
    $scope.socket.on('connect', function() {
        $scope.socket.emit('confirm connection', {
            message: 'client is connected to the SocketServer...',
            userId: window.sessionStorage.getItem('userId')
        });
    });

    /*
     * The callback in the listener 'refreshed partner chat' is used to automatically update the user chat
     * view with a specific partner by referring to the name of the partner in the session storage of the user's browser.
     *
     * @author Oliver Kovarna
     */
    $scope.socket.on('refreshed partner chat', function(data) {
        let userId = window.sessionStorage.getItem('userId');
        $scope.loadChats(userId);

        if ($scope.isFooterNotHidden) {
            let chatPartnerName = window.sessionStorage.getItem('chatPartnerName');

            if(data.senderUserId !== userId && data.senderChatPartnerId === userId
                && data.senderName === chatPartnerName) {
                $scope.loadChats(userId);
                $scope.loadChatHistory(userId, chatPartnerName, true);
                $scope.isPartnerTyping = false;
            }
        }
    });

    /*
     * The callback in the listener 'refreshed partner chat activity' updates the chat footer (message field) view
     * with a certain box ('partner is writing a message...') when its partner writes a message.
     *
     * @author Oliver Kovarna
     */
    $scope.socket.on('refreshed partner chat activity', function(data) {
        if ($scope.isFooterNotHidden) {
            let userId = window.sessionStorage.getItem('userId');
            let chatPartnerName = window.sessionStorage.getItem('chatPartnerName');

            if(data.senderUserId !== userId && data.senderChatPartnerId === userId
                && data.senderName === chatPartnerName) {
                let messageContent = data.content;

                if (messageContent !== '') {
                    document.getElementById('partner_typing_message').innerHTML = '<b>' + chatPartnerName + ' is writing a message...</b>';
                    $scope.isPartnerTyping = true;
                    $scope.$apply();
                }
                else {
                    $scope.isPartnerTyping = false;
                    $scope.$apply();
                }
            }
        }
    });

    /*
     * The callback in the listener 'refreshed chat list' is used to update the user chat sidebar view with
     * the contacts (chat partner). This way, the user knows if its contact is active or inactive (online or offline).
     *
     * @author Oliver Kovarna
     */
    $scope.socket.on('refreshed chat list', function(data) {
        let userId = window.sessionStorage.getItem('userId');
        $scope.loadChats(userId);
    });

    /*
     * The controller function 'sendMessage' is for sending messages from client to server.
     *
     * @author Oliver Kovarna
     */
    $scope.sendMessage = function() {
        let textMessage = document.getElementById('message_content').value;
        if(typeof textMessage === 'undefined' || textMessage === '') {
            alert('Please enter a text message!');
            return;
        }

        let chatPartner = window.sessionStorage.getItem('chatPartnerName');
        let userId = window.sessionStorage.getItem('userId');

        let chatObj = {
            chatPartner,
            textMessage,
            timeStamp: new Date()
        };
        $http.post('/user/id/' + userId + '/chat/message', chatObj)
        .then((response) => {
            messageObj = response.data;
            $scope.textModel = '';
            document.getElementById('message_content').value = '';

            // Set flag to false
            $scope.loadChatHistory(userId, chatPartner, false);

            // The socket client emits an event to update the user chat view
            $scope.socket.emit('refresh partner chat', {
                message: 'refresh partner chat',
                senderChatPartnerName: chatPartner,
                senderUserId: userId
            });

            $scope.socket.emit('refresh partner main page', {
                message: 'refresh partner main page',
                senderChatPartnerName: chatPartner,
                senderUserId: userId
            });
        },
        (err) => {
            console.log(err);
        });
    }

    /*
     * The controller function 'showContacts' is for showing contacts of the client in the side bar.
     *
     * @author Oliver Kovarna
     */
    $scope.showContacts = function() {
        let searchInput = $scope.searchInputModel;
        let userId = window.sessionStorage.getItem('userId');

        $http.get('/user/id/' + userId + '/contacts?search=' + searchInput)
        .then((response) => {
            if(response.data instanceof Array) {
                return;
            }
            $scope.loadChats(userId);
        },
        (err) => {
            console.log(err);
        });
    }

    /*
     * The controller function 'showChat' is for initializing chat related data.
     * It calls another function 'loadChatHistory' to load the entire chat history when a specific chat
     * is clicked by the user.
     *
     * @author Oliver Kovarna
     */
    $scope.showChat = function($event) {
        let userId = window.sessionStorage.getItem('userId');
        // '$event.currentTarget' takes the chat partner name from the html page
        let chatPartnerName = $event.currentTarget.children[0].children[1].children[0].innerHTML;
        chatPartnerName = chatPartnerName.substring(0, chatPartnerName.indexOf('(')).trim();
        window.sessionStorage.setItem('chatPartnerName', chatPartnerName);

        if ($scope.currentChatPartner !== chatPartnerName) {
            // current chat partner is assigned to the one clicked at
            $scope.currentChatPartner = chatPartnerName;
            // '$scope.chatPartnerTitle' is used to display the name of the new chat partner on the html page
            $scope.chatPartnerTitle = chatPartnerName;
            $scope.isProfilePictureNotHidden = true;
            $scope.isFooterNotHidden = true;
            $scope.isPartnerTyping = false;

            // initialize '$scope.chatHistory' as empty string, used to place some html tags inside to display
            // all the messages that are saved in the DB for the current chat partners (chat histories)
            $scope.chatHistory = '';
            // gets every person that the current user has already had a chat with
            $scope.loadChats(userId);
            // loads all messages that have already been sent to and from the partner
            $scope.loadChatHistory(userId, chatPartnerName, true);
            // delete notifications if there were any, because the messages can now be marked as 'read'
            $scope.refreshMessageNotificationStatus(userId, chatPartnerName);
        }
    }

    /*
     * The controller function 'loadChatHistory' is for loading the chat history of a specific chat.
     *
     * @author Oliver Kovarna
     */
    $scope.loadChatHistory = function(userId, chatPartnerName, isEvent) {

        $http.get('/user/id/' + userId + '/chat?partner=' + chatPartnerName)
        .then((response) => {
            if(typeof response.data === 'string') {
                $scope.messageCount = '0 messages';
            } else {
                $scope.messageList = response.data;
                $scope.messageCount = $scope.messageList.length + ' messages';
                $scope.historyMessageIndex = 0;

                $scope.historyMessageNodes = angular.element(document.getElementsByClassName('card-body msg_card_body'))[0].childNodes;
                $scope.historyMessageNodeCount = $scope.historyMessageNodes.length;

                if ($scope.historyMessageNodeCount > 0) {
                    $scope.historyMessageIndex = $scope.historyMessageNodeCount;

                    $scope.unreadMessagesBox = angular.element(document.getElementById('unread_messages'));
                    if ($scope.unreadMessagesBox !== undefined && $scope.unreadMessagesBox !== null
                        && Object.keys($scope.unreadMessagesBox).length !== 0) {
                        $scope.historyMessageIndex -= 1;
                    }
                }

                for(; $scope.historyMessageIndex < $scope.messageList.length; $scope.historyMessageIndex++) {
                    let messageObj = $scope.messageList[$scope.historyMessageIndex];

                    if (isEvent && !$scope.isNotificationBoxDisplayed && messageObj[3] === 1
                        && messageObj[2] !== userId) {

                        $scope.chatHistory += '<div id="unread_messages" class="unread_msg_container">Unread messages</div>';
                        $scope.isNotificationBoxDisplayed = true;
                    }

                    if(String(messageObj[messageObj.length - 2]) !== userId) {
                        $scope.chatHistory += '<div class="d-flex justify-content-start mb-4 total_msg_container">' +
                                                  '<div class="img_cont_msg">' +
                                                      '<img src="/image" class="rounded-circle user_img_msg">' +
                                                  '</div>' +
                                                  '<div class="msg_cotainer">' +
                                                      '<div class="msg_cotainer">' + messageObj[0] + '</div>' +
                                                      '<span class="msg_time">' + messageObj[1] + '</span>' +
                                                  '</div>' +
                                              '</div>';
                    }
                    else {
                        $scope.chatHistory += '<div class="d-flex justify-content-end mb-4 total_msg_container">' +
                                                  '<div class="msg_cotainer_send">' +
                                                      '<div class="msg_cotainer_send">' + messageObj[0] + '</div>' +
                                                      '<span class="msg_time_send">' + messageObj[1] + '</span>' +
                                                  '</div>' +
                                                  '<div class="img_cont_msg">' +
                                                      '<img src="/image" class="rounded-circle user_img_msg">' +
                                                  '</div>' +
                                              '</div>';
                    }
                }

                $timeout(function() {
                    $scope.historyMessageNodes = angular.element(document.getElementsByClassName('card-body msg_card_body'))[0].childNodes;
                    $scope.historyMessageNodeCount = $scope.historyMessageNodes.length;
                    $scope.lastMessageNode = $scope.historyMessageNodes[$scope.historyMessageNodeCount - 1];

                    if ($scope.lastMessageNode !== null && $scope.lastMessageNode !== undefined) {
                        $scope.lastMessageNode.scrollIntoView();
                    }
                }, 5);
            }
        },
        (err) => {
            console.log(err);
        });
    }

    /*
     * The controller function 'refreshMessageNotificationStatus' is for refreshing the status of partner messages in
     * the database. When messages are refreshed they will not be displayed as new (unread) messages with a certain box
     * ('Unread messages').
     *
     * @author Oliver Kovarna
     */
    $scope.refreshMessageNotificationStatus = function(userId, chatPartnerName) {
        let chatPartnerObj = {
            chatPartnerName
        }
        $http.put('/user/id/' + userId + '/chat/notification-status', chatPartnerObj)
        .then((response) => {
        },
        (err) => {
            console.log(err);
        });
    }

    /*
     * The controller function 'loadChats' is for loading all chats related to the current user.
     *
     * @author Oliver Kovarna
     */
    $scope.loadChats = function(userId) {
        $http.get('/user/id/' + userId + '/chats')
        .then((response) => {
            let chatListPartner = response.data;
            $scope.chatList = '';
            if(chatListPartner instanceof Array) {
                for(let i = 0; i < chatListPartner.length; i++) {
                    let userRole = '';
                    if (chatListPartner[i].isAgent === 1) {
                        userRole = '(Agent)'
                    }
                    else if (chatListPartner[i].isManager === 1) {
                        userRole = '(Manager)'
                    }
                    else if (chatListPartner[i].isChatBot === 1) {
                        userRole = '(AI)'
                    }
                    else {
                        userRole = '(Customer)'
                    }

                    $scope.notificationCount = chatListPartner[i].notificationCount;
                    $scope.notificationLIClass = '';
                    $scope.notificationSPAN = '';

                    if ($scope.notificationCount > 0) {
                        $scope.notificationLIClass = 'notification';
                        $scope.notificationSPAN = '<span class="badge">' + $scope.notificationCount + '</span>';
                    }

                    if (chatListPartner[i].status === 1) {
                        $scope.chatList +=  '<li class="chat_entry ' + $scope.notificationLIClass + '" tabindex="1" ng-click="showChat($event)">' +
                                                '<div class="d-flex bd-highlight"><div class="img_cont">' +
                                                    '<img src="/image" class="rounded-circle user_img">' +
                                                    $scope.notificationSPAN +
                                                    '<span class="online_icon"></span>' +
                                                '</div>' +
                                                '<div class="user_info">' +
                                                    '<span>' + chatListPartner[i].name + ' ' + userRole + '</span>' +
                                                    '<p>is online</p>' +
                                                '</div>' +
                                                '</div>' +
                                           '</li>';
                    }
                    else {
                        $scope.chatList += '<li class="chat_entry ' + $scope.notificationLIClass + '" tabindex="1" ng-click="showChat($event)">' +
                                                '<div class="d-flex bd-highlight"><div class="img_cont">' +
                                                    '<img src="/image" class="rounded-circle user_img">' +
                                                    $scope.notificationSPAN +
                                                    '<span class="offline"></span>' +
                                                '</div>' +
                                                '<div class="user_info">' +
                                                    '<span>' + chatListPartner[i].name + ' ' + userRole + '</span>' +
                                                    '<p>is offline</p>' +
                                                '</div>' +
                                                '</div>' +
                                           '</li>';
                    }
                }
            } else {
                console.log(response.data);
            }
        },
        (err) => {
            console.log(err);
        });
    }

    /*
     * The controller function 'trackChatUserActivity' tracks a chat user. As soon as he writes something in the
     * text field of a certain partner chat, an event 'refresh partner chat activity' is sent to the socket server
     * to request an update of the partner chat.
     *
     * @author Oliver Kovarna
     */
    $scope.trackChatUserActivity = function() {
        let messageContent = document.getElementById('message_content').value;
        let userId = window.sessionStorage.getItem('userId');
        let chatPartnerName = window.sessionStorage.getItem('chatPartnerName');

        $scope.socket.emit('refresh partner chat activity', {
            message: 'client is currently typing...',
            content: messageContent,
            senderChatPartnerName: chatPartnerName,
            senderUserId: userId
        });

        $scope.unreadMessagesBox = angular.element(document.getElementById('unread_messages'));

        if ($scope.unreadMessagesBox !== undefined && $scope.unreadMessagesBox !== null
            && Object.keys($scope.unreadMessagesBox).length !== 0) {

            $scope.unreadMessagesBox.remove();
            $scope.chatHistory = $scope.chatHistory.replace(
                    '<div id="unread_messages" class="unread_msg_container">Unread messages</div>', '');
        }

        $scope.isNotificationBoxDisplayed = false;
        $scope.refreshMessageNotificationStatus(userId, chatPartnerName);
        $scope.loadChats(userId);
    }

    /*
     * This controller 'init' is for initializing the user's chat page when he logs in.
     *
     * @author Oliver Kovarna
     */
    $scope.init = function() {
        let userId = window.sessionStorage.getItem('userId');
        $scope.loadChats(userId);
    }
    $scope.init();
}]);

/*
 * The controller directive 'compile' is to enable the compiling of all scope related stuff.
 *
 * @author Oliver Kovarna
 */
myChat.directive('compile', ['$compile', function ($compile) {
    return function(scope, element, attrs) {
        scope.$watch(
            function(scope) {
                return scope.$eval(attrs.compile);
            },
            function(value) {
                element.html(value);
                $compile(element.contents())(scope);
            }
        );
    };
}])

/*
 * The controller directive 'myEnter' is to enable sending messages via key press 'enter'.
 *
 * @author Oliver Kovarna
 */
myChat.directive('myEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.myEnter);
                });

                event.preventDefault();
            }
        });
    };
});
