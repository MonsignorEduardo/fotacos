import QtQuick 2.15
import QtQuick.Controls 2.15

// Individual photo slide in the slideshow
Item {
    id: root

    property string photoPath: ""

    signal doubleClicked()

    Rectangle {
        anchors.fill: parent
        color: "#000000"

        Image {
            id: fullscreenImage
            anchors.fill: parent
            source: root.photoPath
            fillMode: Image.PreserveAspectFit
            asynchronous: true
            smooth: true

            // Loading indicator
            Rectangle {
                anchors.fill: parent
                color: "#000000"
                visible: fullscreenImage.status === Image.Loading

                BusyIndicator {
                    anchors.centerIn: parent
                    running: parent.visible
                }
            }

            // Error message
            Text {
                anchors.centerIn: parent
                text: "Error al cargar la foto"
                color: "#ff5555"
                font.pixelSize: 24
                visible: fullscreenImage.status === Image.Error
            }
        }

        // Double tap detector
        MouseArea {
            anchors.fill: parent
            onDoubleClicked: root.doubleClicked()
        }
    }
}
