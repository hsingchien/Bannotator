def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()
        else:
            del item

def reset_table(table):
    model = table.model()
    model.state_change.disconnect(table.setState)
    table.setModel(None)
    del model