import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

// Gallery grid view component
Item {
    id: root

    signal backToSlideshow()
    signal photoSelected(int index)

    property int selectedIndex: 0

    Rectangle {
        anchors.fill: parent
        color: "#000000"

        // Header bar
        GalleryHeader {
            id: galleryHeader
            photoCount: gridView.count

            onBackClicked: root.backToSlideshow()
            onRefreshClicked: galleryModel.refresh()
            onQuitClicked: Qt.quit()
        }

        // Photo grid
        GridView {
            id: gridView
            anchors.top: galleryHeader.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 20
            cellWidth: 350
            cellHeight: 350
            clip: true

            model: galleryModel.photos

            delegate: PhotoGridItem {
                width: gridView.cellWidth
                height: gridView.cellHeight
                photoPath: modelData.path
                photoFilename: modelData.filename
                isSelected: index === root.selectedIndex

                onClicked: root.photoSelected(index)
            }

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
            }
        }
    }
}
