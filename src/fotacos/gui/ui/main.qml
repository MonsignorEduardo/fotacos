import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: mainWindow
    visible: true
    visibility: Window.FullScreen
    title: "Galería Fotacos"
    color: "#000000"

    property int currentIndex: 0
    property bool showGallery: false

    // Main fullscreen slideshow view
    Item {
        id: slideshowView
        anchors.fill: parent
        visible: !showGallery

        // Current photo display
        SwipeView {
            id: swipeView
            anchors.fill: parent
            currentIndex: mainWindow.currentIndex
            interactive: true

            onCurrentIndexChanged: {
                mainWindow.currentIndex = currentIndex
            }

            Repeater {
                model: galleryModel.photos

                Item {
                    Rectangle {
                        anchors.fill: parent
                        color: "#000000"

                        Image {
                            id: fullscreenImage
                            anchors.fill: parent
                            source: modelData.path
                            fillMode: Image.PreserveAspectFit
                            asynchronous: true
                            smooth: true

                            Rectangle {
                                anchors.fill: parent
                                color: "#000000"
                                visible: fullscreenImage.status === Image.Loading

                                BusyIndicator {
                                    anchors.centerIn: parent
                                    running: parent.visible
                                }
                            }

                            Text {
                                anchors.centerIn: parent
                                text: "Failed to load photo"
                                color: "#ff5555"
                                font.pixelSize: 24
                                visible: fullscreenImage.status === Image.Error
                            }
                        }

                        // Double tap detector to switch to gallery
                        MouseArea {
                            anchors.fill: parent
                            onDoubleClicked: {
                                showGallery = true
                            }
                        }
                    }
                }
            }
        }

        // Left navigation button (tactile)
        RoundButton {
            id: leftButton
            anchors.left: parent.left
            anchors.leftMargin: 30
            anchors.verticalCenter: parent.verticalCenter
            width: 80
            height: 80
            visible: swipeView.count > 0
            opacity: 0.7

            icon.source: "qrc:/qt-project.org/imports/QtQuick/Controls/Material/images/left-arrow.png"
            icon.width: 40
            icon.height: 40

            Material.background: Material.Grey
            Material.elevation: 6

            onClicked: {
                if (swipeView.currentIndex > 0) {
                    swipeView.decrementCurrentIndex()
                } else {
                    swipeView.currentIndex = swipeView.count - 1
                }
            }

            Text {
                anchors.centerIn: parent
                text: "◀"
                font.pixelSize: 40
                color: "#ffffff"
            }
        }

        // Right navigation button (tactile)
        RoundButton {
            id: rightButton
            anchors.right: parent.right
            anchors.rightMargin: 30
            anchors.verticalCenter: parent.verticalCenter
            width: 80
            height: 80
            visible: swipeView.count > 0
            opacity: 0.7

            Material.background: Material.Grey
            Material.elevation: 6

            onClicked: {
                if (swipeView.currentIndex < swipeView.count - 1) {
                    swipeView.incrementCurrentIndex()
                } else {
                    swipeView.currentIndex = 0
                }
            }

            Text {
                anchors.centerIn: parent
                text: "▶"
                font.pixelSize: 40
                color: "#ffffff"
            }
        }

        // Photo counter and info overlay
        Rectangle {
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: 30
            width: infoText.width + 40
            height: 50
            color: "#000000"
            opacity: 0.8
            radius: 25
            visible: swipeView.count > 0

            Text {
                id: infoText
                anchors.centerIn: parent
                text: (swipeView.currentIndex + 1) + " / " + swipeView.count
                color: "#ffffff"
                font.pixelSize: 20
                font.bold: true
            }
        }

        // Hint text for double tap
        Text {
            anchors.top: parent.top
            anchors.topMargin: 30
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Double tap to view gallery"
            color: "#888888"
            font.pixelSize: 16
            opacity: 0.6
        }

        // Empty state
        Column {
            anchors.centerIn: parent
            spacing: 20
            visible: swipeView.count === 0

            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "No photos available"
                color: "#888888"
                font.pixelSize: 32
            }

            Button {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Refresh"
                Material.background: Material.Grey
                onClicked: galleryModel.refresh()
            }
        }
    }

    // Gallery grid view (accessed via double tap)
    Item {
        id: galleryView
        anchors.fill: parent
        visible: showGallery

        Rectangle {
            anchors.fill: parent
            color: "#000000"

            // Header bar
            Rectangle {
                id: galleryHeader
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
                        text: "◀ Back to Slideshow"
                        font.pixelSize: 18
                        Material.background: Material.Grey
                        onClicked: showGallery = false
                    }

                    Label {
                        text: "Fotacos Gallery - " + gridView.count + " photos"
                        color: "#ffffff"
                        font.pixelSize: 20
                        Layout.fillWidth: true
                    }

                    Button {
                        text: "Refresh"
                        Material.background: Material.Grey
                        onClicked: galleryModel.refresh()
                    }

                    Button {
                        text: "Quit"
                        Material.background: Material.Red
                        onClicked: Qt.quit()
                    }
                }
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

                delegate: Item {
                    width: gridView.cellWidth
                    height: gridView.cellHeight

                    Rectangle {
                        anchors.fill: parent
                        anchors.margins: 10
                        color: "#1a1a1a"
                        radius: 8
                        border.color: index === mainWindow.currentIndex ? "#4CAF50" : "transparent"
                        border.width: 4

                        Image {
                            id: photoImage
                            anchors.fill: parent
                            anchors.margins: 5
                            source: modelData.path
                            fillMode: Image.PreserveAspectFit
                            asynchronous: true
                            smooth: true

                            Rectangle {
                                anchors.fill: parent
                                color: "#2a2a2a"
                                visible: photoImage.status === Image.Loading

                                BusyIndicator {
                                    anchors.centerIn: parent
                                    running: parent.visible
                                }
                            }

                            Text {
                                anchors.centerIn: parent
                                text: "Failed to load"
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
                                text: modelData.filename
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
                            onClicked: {
                                mainWindow.currentIndex = index
                                showGallery = false
                            }
                        }
                    }
                }

                ScrollBar.vertical: ScrollBar {
                    policy: ScrollBar.AsNeeded
                }
            }
        }
    }

    // Keyboard shortcuts
    Shortcut {
        sequence: "Esc"
        onActivated: {
            if (showGallery) {
                showGallery = false
            } else if (mainWindow.visibility === Window.FullScreen) {
                mainWindow.visibility = Window.Windowed
            } else {
                Qt.quit()
            }
        }
    }

    Shortcut {
        sequence: "Left"
        enabled: !showGallery
        onActivated: {
            if (swipeView.currentIndex > 0) {
                swipeView.decrementCurrentIndex()
            } else {
                swipeView.currentIndex = swipeView.count - 1
            }
        }
    }

    Shortcut {
        sequence: "Right"
        enabled: !showGallery
        onActivated: {
            if (swipeView.currentIndex < swipeView.count - 1) {
                swipeView.incrementCurrentIndex()
            } else {
                swipeView.currentIndex = 0
            }
        }
    }

    Shortcut {
        sequence: "G"
        onActivated: showGallery = !showGallery
    }

    Shortcut {
        sequence: "F11"
        onActivated: {
            mainWindow.visibility = mainWindow.visibility === Window.FullScreen
                ? Window.Windowed
                : Window.FullScreen
        }
    }

    Shortcut {
        sequence: "Ctrl+Q"
        onActivated: Qt.quit()
    }

    Shortcut {
        sequence: "F5"
        onActivated: galleryModel.refresh()
    }

    Shortcut {
        sequence: "Space"
        enabled: !showGallery
        onActivated: {
            if (swipeView.currentIndex < swipeView.count - 1) {
                swipeView.incrementCurrentIndex()
            } else {
                swipeView.currentIndex = 0
            }
        }
    }
}
