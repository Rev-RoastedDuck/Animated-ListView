from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QApplication, QListView, QVBoxLayout

from card_delegate import CardDelegate
from card_list_view import CardListView


if __name__ == "__main__":
    app = QApplication([])

    widget = QWidget()
    widget.resize(500, 300)
    widget.setStyleSheet("background-color:rgb(25, 53, 73);")

    card_data_list = [
        {"title": "PHP",
         "description": "PHP is a server-side scripting language used for web development and dynamic content generation. It is often used in conjunction with HTML, CSS, and JavaScript to create fully featured web applications."},
        {"title": "JavaScript",
         "description": "JavaScript is the most widely used programming language for creating interactive web applications. It runs on the client side in web browsers and on the server side on web servers."},
        {"title": "Go",
         "description": "Go is a relatively new programming language designed for building fast, reliable, and efficient software. It is a popular choice for developing networked and distributed systems."},
        {"title": "Python",
         "description": "Python is a high-level programming language that is easy to learn. It is used for web development, data analysis, and artificial intelligence applications."},
        {"title": "Java",
         "description": "Java is a popular programming language known for its portability, security, and versatility. It is often used in large-scale enterprise applications, mobile development, and web services."},
        {"title": "C#",
         "description": "C# is a modern, versatile programming language developed by Microsoft. It is commonly used for Windows desktop applications, video games, and web services."},
        {"title": "C++",
         "description": "C++ is a powerful object-oriented programming language widely used in system software, embedded systems, games, and high-performance applications."},
        {"title": "C",
         "description": "C is a high-level, general-purpose programming language that was originally developed for system programming. "},
        {"title": "MySQL",
         "description": "MySQL is a popular open-source relational database management system. It provides a reliable, scalable, and secure way to store and manage structured data. "},
        {"title": "Rust",
         "description": "Rust is a fast and safe systems programming language with a modern syntax. It provides memory safety and thread safety without compromising performance."},
    ]

    model = QStandardItemModel()
    for card_data in card_data_list:
        item = QStandardItem()
        item.setData(card_data, Qt.DisplayRole)
        model.appendRow(item)

    delegate = CardDelegate()
    listView = CardListView()
    listView.setStyleSheet("""AnimListView{background-color:rgb(13, 31, 45);border:none;};""")
    listView.resize(500, 300)
    listView.setFixedHeight(300)
    listView.setItemDelegate(delegate)
    listView.setModel(model)

    # listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    listView.setFlow(QListView.LeftToRight)
    listView.setIconSize(QSize(200, 100))

    layout = QVBoxLayout()
    layout.addWidget(listView)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(layout)
    widget.show()

    app.exec()
