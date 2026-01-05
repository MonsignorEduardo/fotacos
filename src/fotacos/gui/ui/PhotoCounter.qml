import QtQuick 2.15
import QtQuick.Controls 2.15

// Photo counter overlay for slideshow
Rectangle {
    id: root

    property int currentPhoto: 1
    property int totalPhotos: 0

    width: counterText.width + 40
    height: 50
    color: "#000000"
    opacity: 0.8
    radius: 25

    Text {
        id: counterText
        anchors.centerIn: parent
        text: root.currentPhoto + " / " + root.totalPhotos
        color: "#ffffff"
        font.pixelSize: 20
        font.bold: true
    }
}
