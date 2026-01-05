import QtQuick 2.15
import QtQuick.Controls 2.15

// Individual photo item in the gallery grid
Item {
    id: root

    property string photoPath: ""
    property string photoFilename: ""
    property bool isSelected: false

    signal clicked()

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        color: "#1a1a1a"
        radius: 8
        border.color: root.isSelected ? "#4CAF50" : "transparent"
        border.width: 4

        Image {
            id: photoImage
            anchors.fill: parent
            anchors.margins: 5
            source: root.photoPath
            fillMode: Image.PreserveAspectFit
            asynchronous: true
            smooth: true

            // Loading indicator
            Rectangle {
                anchors.fill: parent
                color: "#2a2a2a"
                visible: photoImage.status === Image.Loading

                BusyIndicator {
                    anchors.centerIn: parent
                    running: parent.visible
                }
            }

            // Error message
            Text {
                anchors.centerIn: parent
                text: "Error al cargar"
                color: "#ff5555"
                visible: photoImage.status === Image.Error
            }
        }

        // Filename label at bottom
        Rectangle {
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: 40
            color: "#000000"
            opacity: 0.8
            radius: 8

            Text {
                anchors.centerIn: parent
                text: root.photoFilename
                color: "#ffffff"
                font.pixelSize: 12
                elide: Text.ElideMiddle
                width: parent.width - 20
                horizontalAlignment: Text.AlignHCenter
            }
        }

        MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            onClicked: root.clicked()
        }
    }
}
