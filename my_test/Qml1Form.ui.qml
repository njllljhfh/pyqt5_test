import QtQuick 2.0

Column {
    width: 200
    height: 200

    TextInput {
        id: myTextInput
        text: "Hello World"
    }

    Text {
        text: myTextInput11.text
    }
    Text {
        text: "123"
    }
}
