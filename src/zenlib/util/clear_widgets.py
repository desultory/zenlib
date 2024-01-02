from PyQt6.QtWidgets import QWidgetItem


# This function is used to clear the widgets from the layout
def clear_widgets(qt_object):
    for i in range(qt_object.count()):
        item = qt_object.itemAt(i)
        if isinstance(item, QWidgetItem) and item.widget():
            item.widget().deleteLater()
