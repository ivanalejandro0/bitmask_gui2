import QtQuick 2.0
import QtQuick.Controls 1.1

Rectangle {
  id: chatView
  property alias message: message_input
  property string messageText: ''
  width: 400
  height: 300

  Column {
    anchors.fill: parent

    ListView {
      id: messagesList

      width: parent.width
      height: parent.height - 20  // leave space for the input
      clip: true

      // model: listModel
      delegate: listDelegate
    }

    Component {
      id: listDelegate

      Rectangle {
        width: messagesList.width
        height: 40
        color: ((index % 2 == 0)?"#222":"#111")

        Text {
          id: title

          text: model.messageItem.text
          wrapMode: Text.Wrap
          color: "white"
          anchors {
            margins: 10
            verticalCenterOffset: 5
            left: parent.left
            right: parent.right
            top: parent.top
          }
          verticalAlignment: Text.AlignVCenter
        }
      }
    }

    Rectangle {
      border.color: 'black'
      border.width: 2
      width: messagesList.width
      height: 40

      TextInput {
        id: message_input

        anchors.fill: parent
        width: parent.width
        height: 20
        focus: true
        font.pixelSize: 16
        onAccepted: chatView.messageText = text
      }
    }
    Button {
      text: "Send"
      // onClicked: login.accepted = true
    }
  }
}
