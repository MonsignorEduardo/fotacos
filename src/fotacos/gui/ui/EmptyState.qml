import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

// Empty state component when no photos are available
Column {
    anchors.centerIn: parent
    spacing: 20

    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        text: "No hay fotos disponibles"
        color: "#888888"
        font.pixelSize: 32
    }

    Button {
        anchors.horizontalCenter: parent.horizontalCenter
        text: "Actualizar"
        Material.background: Material.Grey
        onClicked: galleryModel.refresh()
    }
}
