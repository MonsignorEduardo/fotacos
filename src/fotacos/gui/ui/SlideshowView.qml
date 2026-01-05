import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

// Main fullscreen slideshow view component
Item {
    id: root

    signal switchToGallery()

    property alias currentIndex: swipeView.currentIndex
    property int photoCount: swipeView.count

    // Auto-advance timer (30 seconds)
    Timer {
        id: autoAdvanceTimer
        interval: 30000 // 30 segundos
        running: swipeView.count > 0
        repeat: true

        onTriggered: {
            if (swipeView.currentIndex < swipeView.count - 1) {
                swipeView.incrementCurrentIndex()
            } else {
                swipeView.currentIndex = 0
            }
        }
    }

    // Current photo display with swipe support
    SwipeView {
        id: swipeView
        anchors.fill: parent
        interactive: true

        Repeater {
            model: galleryModel.photos

            PhotoSlide {
                photoPath: modelData.path
                onDoubleClicked: root.switchToGallery()
            }
        }
    }

    // Left navigation button (tactile)
    NavigationButton {
        anchors.left: parent.left
        anchors.leftMargin: 30
        anchors.verticalCenter: parent.verticalCenter
        direction: "left"
        visible: swipeView.count > 0

        onClicked: {
            if (swipeView.currentIndex > 0) {
                swipeView.decrementCurrentIndex()
            } else {
                swipeView.currentIndex = swipeView.count - 1
            }
        }
    }

    // Right navigation button (tactile)
    NavigationButton {
        anchors.right: parent.right
        anchors.rightMargin: 30
        anchors.verticalCenter: parent.verticalCenter
        direction: "right"
        visible: swipeView.count > 0

        onClicked: {
            if (swipeView.currentIndex < swipeView.count - 1) {
                swipeView.incrementCurrentIndex()
            } else {
                swipeView.currentIndex = 0
            }
        }
    }

    // Photo counter overlay
    PhotoCounter {
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 30
        visible: swipeView.count > 0
        currentPhoto: swipeView.currentIndex + 1
        totalPhotos: swipeView.count
    }

    // Hint text for double tap
    Text {
        anchors.top: parent.top
        anchors.topMargin: 30
        anchors.horizontalCenter: parent.horizontalCenter
        text: "Doble toque para ver la galería"
        color: "#888888"
        font.pixelSize: 16
        opacity: 0.6
    }

    // Empty state
    EmptyState {
        visible: swipeView.count === 0
    }
}
