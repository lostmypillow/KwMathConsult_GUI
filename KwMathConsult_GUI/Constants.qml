pragma Singleton
import QtQuick 2.15
import QtQuick.Controls 2.15

QtObject {
    readonly property int width: 480
    readonly property int height: 320

    property string relativeFontDirectory: "fonts"
    property string fontPath: Qt.resolvedUrl("../KwMathConsult_GUIContent/" + relativeFontDirectory + "/SarasaFixedTC-Regular.ttf")

    // Load the custom font by specifying the family name directly
    readonly property font font: Qt.font({
        family: "SarasaFixedTC",  // Replace with the font family name you registered
        pixelSize: 12  // Set the font size as needed
    })

    readonly property font largeFont: Qt.font({
        family: "SarasaFixedTC",  // Replace with the font family name you registered
        pixelSize: 19  // Larger font size
    })

    readonly property color backgroundColor: "#EAEAEA"

}
