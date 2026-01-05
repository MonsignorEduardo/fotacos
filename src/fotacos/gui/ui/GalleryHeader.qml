import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

// Header bar for gallery view
Rectangle {
    id: root

    signal backClicked()
    signal refreshClicked()
    signal quitClicked()

    property int photoCount: 0

    anchors.top: parent.top
    anchors.left: parent.left
    anchors.right: parent.right
    height: 80
    color: "#212121"
    z: 10

    RowLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 15

        Button {
            text: "◀ Volver a la presentación"
            font.pixelSize: 18
            Material.background: Material.Grey
            onClicked: root.backClicked()
        }

        Label {
            text: "Galería Fotacos - " + root.photoCount + " fotos"
            color: "#ffffff"
            font.pixelSize: 20
            Layout.fillWidth: true
        }

        Button {
            text: "Actualizar"
            Material.background: Material.Grey
            onClicked: root.refreshClicked()
        }

        Button {
            text: "Salir"
            Material.background: Material.Red
            onClicked: root.quitClicked()
        }
    }
}
