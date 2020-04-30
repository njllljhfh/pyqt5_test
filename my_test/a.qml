import QtQuick 2.3
import QtQuick.Controls 1.2
import a.qt.Dealer 1.3

ApplicationWindow {
    id: test
    visible: true
    width: 100; height: 100;

    Text {
        text: "hello world!";
    }

    //像一般控件一样定义后使用
    Dealer {
        id: dealer
    }
}

