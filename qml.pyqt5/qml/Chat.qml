import QtQuick 1.0

Rectangle {
  id: root
  width: 640
  height: 480

  Flickable {
    id: flickable
    flickableDirection: Flickable.HorizontalFlick
    anchors.fill: parent
    interactive: false

    Login {
      id: login
      width: parent.width
      height: parent.height
      onAcceptedChanged: controller.login(username.text, password.text, login)
    }
    ChatWith {
      id: chatWith
      width: parent.width
      height: parent.height
      x: width
      onAcceptedChanged: {
        controller.set_user_to(jid.text, bitmask_jid.text)
        flickable.state = "CHAT"
      }
    }
    ChatView {
      id: chatView
      width: parent.width
      height: parent.height
      x: width * 2
      onMessageTextChanged: controller.send_message(chatView.message)
    }

    state: "LOGIN"
    states: [
      State {
      name: "LOGIN"
      PropertyChanges { target: flickable; contentX: 0 }
      PropertyChanges { target: login.username; focus: true }
    },
    State {
      name: "CHATWITH"
      when: login.loggedIn
      PropertyChanges { target: flickable; contentX: root.width }
      PropertyChanges { target: chatWith.jid; focus: true }
    },
    State {
      name: "CHAT"
      PropertyChanges { target: flickable; contentX: root.width * 2 }
      PropertyChanges { target: chatView.message; focus: true }
    }
    ]

    transitions: Transition {
      PropertyAnimation { property: "contentX"; easing.type: Easing.InOutQuart; duration: 500 }
    }

  }

}
