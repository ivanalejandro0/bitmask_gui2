import QtQuick 2.0
import QtQuick.Controls 1.1

Rectangle {
  id: login
  property bool loggedIn: false
  property bool accepted: false
  property alias username: username_input
  property alias password: password_input

  width: 400
  height: 200
  color: "#222"

  Grid {
    columns: 2
    spacing: 10
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter

    Rectangle {
      height: 20
      width: 100
      color: "#222"
      Text {
        anchors.fill: parent
        text: "User:"
        font.pixelSize: 16
        color: "white"
      }
    }

    Rectangle {
      height: 20
      width: 200
      TextInput {
        id: username_input

        text: "1234test1234@wtfismyip.com/chat_app"  // Hard-coded username
        anchors.fill: parent
        focus: true
        font.pixelSize: 16
        onAccepted: password_input.focus = true
        anchors.verticalCenterOffset: 5
        layer.enabled: true
      }
    }

    Rectangle {
      height: 20
      width: 100
      color: "#222"
      Text {
        anchors.fill: parent
        text: "Password:"
        font.pixelSize: 16
        color: "white"
      }
    }

    Rectangle {
      height: 20
      width: 200
      TextInput {
        id: password_input

        text: 'asdfasdf'  // Hard-coded password
        anchors.fill: parent
        font.pixelSize: 16
        echoMode: TextInput.Password
        onAccepted: login.accepted = true
        anchors.verticalCenterOffset: 5
      }
    }
    Button {
        text: "Log in"
        onClicked: login.accepted = true
    }
  }
}
