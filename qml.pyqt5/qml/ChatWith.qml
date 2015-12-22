import QtQuick 2.0

Rectangle {
  id: chatWith
  property alias jid: jid_input
  property alias bitmask_jid: bitmask_jid_input
  property bool accepted: false

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
        text: "Chat with:"
        font.pixelSize: 16
        color: "white"
      }
    }

    Rectangle {
      height: 20
      width: 200
      TextInput {
        id: jid_input

        text: "123test123@wtfismyip.com"
        anchors.fill: parent
        focus: true
        font.pixelSize: 16
        anchors.verticalCenterOffset: 5
        // onAccepted: chatWith.accepted = true
        onAccepted: bitmask_jid_input.focus = true
      }

    }

    Rectangle {
      height: 20
      width: 100
      color: "#222"
      Text {
        anchors.fill: parent
        text: "Bitmask jid:"
        font.pixelSize: 16
        color: "white"
      }
    }

    Rectangle {
      height: 20
      width: 200
      TextInput {
        id: bitmask_jid_input

        text: "ivan@dev.bitmask.net"
        anchors.fill: parent
        font.pixelSize: 16
        anchors.verticalCenterOffset: 5
        onAccepted: chatWith.accepted = true
      }

    }

  }
}
