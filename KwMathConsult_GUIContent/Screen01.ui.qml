

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import KwMathConsult_GUI
import QtQuick.Layouts

Rectangle {
    id: main_screen
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor

    ColumnLayout {
        id: main_layout
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.topMargin: 10
        anchors.bottomMargin: 10

        Rectangle {
            id: top_section
            width: 200
            height: 50
            color: "#ffffff"
            Layout.minimumHeight: 80
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.fillWidth: true
            Layout.maximumHeight: 80

            RowLayout {
                id: input_layout
                anchors.fill: parent
                anchors.leftMargin: 5
                anchors.rightMargin: 5
                anchors.topMargin: 5
                anchors.bottomMargin: 5

                TextField {
                    id: id_input
                    objectName: "id_input"
                    text: ""
                    font.pixelSize: 36
                    hoverEnabled: false
                    focus: true
                    Layout.minimumHeight: 40
                    Layout.fillHeight: true
                    font.family: "Sarasa Fixed TC"
                    Layout.fillWidth: true
                    placeholderText: qsTr("")
                    onAccepted: controller.handle_input(text)
                }

                Button {
                    id: kb_btn
                    objectName: "kb_btn"
                    text: qsTr("開啟鍵盤")
                    Layout.maximumHeight: 70
                    Layout.minimumHeight: 70
                    Layout.fillHeight: true
                    icon.source: "images/kb.png"
                    font.pointSize: 16
                    font.family: "Sarasa Fixed TC"

                    onClicked: controller.toggle_numpad()
                }
            }
        }

        Rectangle {
            id: bottom_section
            width: 200
            height: 200
            color: "#ffffff"
            Layout.fillHeight: true
            Layout.fillWidth: true

            Text {
                id: main_text
                objectName: "main_text"
                text: qsTr("請刷卡或輸入卡號")
                anchors.verticalCenter: parent.verticalCenter
                font.pixelSize: 36
                font.family: "Sarasa Fixed TC"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: teacher_text
                objectName: "teacher_text"
                text: qsTr("")
                anchors.bottom: main_text.top
                anchors.bottomMargin: 10
                font.pixelSize: 36
                font.family: "Sarasa Fixed TC"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            GridLayout {
                id: numpad_layout
                objectName: "numpad_layout"
                visible: false
                anchors.fill: parent
                uniformCellWidths: true
                uniformCellHeights: false
                rowSpacing: 2
                columnSpacing: 2
                rows: 4
                columns: 3

                Repeater {
                    id: repeater
                    objectName: "repeater"
                    model: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Del", "0", "OK"]

                    Button {
                        id: button1
                        text: modelData
                        objectName: "numpad_button_" + modelData
                        font.pointSize: 24
                        font.family: "Sarasa Fixed TC"
                        display: AbstractButton.TextOnly
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        onClicked: controller.handle_numpad_click(modelData)  // Call Python function
                    }
                }
            }
        }
    }
    states: [
        State {
            name: "clicked"
        }
    ]
}



