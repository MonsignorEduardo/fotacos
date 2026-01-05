import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

// Tactile navigation button for slideshow
RoundButton {
    id: root

    property string direction: "left" // "left" or "right"

    width: 80
    height: 80
    opacity: 0.7

    Material.background: Material.Grey
    Material.elevation: 6

    Text {
        anchors.centerIn: parent
        text: root.direction === "left" ? "◀" : "▶"
        font.pixelSize: 40
        color: "#ffffff"
    }
}
