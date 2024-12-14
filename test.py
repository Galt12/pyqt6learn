from PyQt6 import QtCore, QtGui, QtWidgets

# tree = {'parent 1': {'child 1 - 1': {'child 1 - 1 - 1': {'child 4 levl parent 1': {}}}, 'child 1 - 2': {'children 2- 1': {}}, 'child 1- 3': {}}, 'parent 2': {'parent 2- 1 - chil': {}}, 'parent 3': {}, 'parent 4': {}}
# vvv см. ниже

tree = {
    'parent 1': {
        'child 1 - 1': {
            'child 1 - 1 - 1': {
                'child 4 levl parent 1': {}
            }
        },
    },                                              # ++
    ## 
    'child 1 - 2': {
        'children 2- 1': {}
    }, 
    #             +
    'child 1- 3': {                                 # - {}
    }, 
    'parent 2': {
        'parent 2- 1 - chil': {}
    }, 
    'parent 3': {}, 
    'parent 4': {}
}


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.tree_view = QtWidgets.QTreeView()
        self.add_btn = QtWidgets.QPushButton("Нажми меня")  # Создаем кнопку с текстом "Нажми меня"
        # self.add_btn.clicked.connect(self.onButtonClick)  # Подключаем обработчик события нажатия на кнопку
        layout = QtWidgets.QVBoxLayout()  # Создаем вертикальный layout
        layout.addWidget(self.tree_view)  # Добавляем виджет tree_view в layout
        layout.addWidget(self.add_btn)  # Добавляем кнопку в layout
        central_widget = QtWidgets.QWidget()  # Создаем виджет для размещения layout
        central_widget.setLayout(layout)  # Устанавливаем layout для central_widget
        self.setCentralWidget(central_widget)

        model = QtGui.QStandardItemModel()
        self.populateTree(tree, model.invisibleRootItem())
        self.tree_view.setModel(model)
        self.tree_view.expandAll()
        self.tree_view.selectionModel().selectionChanged.connect(self.onSelectionChanged)




    def populateTree(self, children, parent):
        for child in children:
            child_item = QtGui.QStandardItem(child)
            parent.appendRow(child_item)
            if isinstance(children, dict):
                self.populateTree(children[child], child_item)

    def onSelectionChanged(self, *args):
        for sel in self.tree_view.selectedIndexes():
            val = "/"+sel.data()
            while sel.parent().isValid():
                sel = sel.parent()
                val = "/"+ sel.data()+ val
            print(val)

    def add_level(tree, parent_key, child_key=None):
        if parent_key not in tree:
            tree[parent_key] = {}
        if child_key:
            if 'children' not in tree[parent_key]:
                tree[parent_key]['children'] = {}
            tree[parent_key]['children'][child_key] = {}
        return tree

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())