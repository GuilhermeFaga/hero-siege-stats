
font_size = 14

style = """
    QWidget {
        font-size: %s;
        background-color: black;
        color: white;
    }

    #Motd, #Motd > * {
        background-color: none;
        color: none;
        font-size: auto;
    }

    QListView { 
        min-height: 100px;
    }

    QListView::item:selected:active {
        background-color: black;
    }
    
    QListView::item:selected {
        background-color: black;
    }

    QListView::item:selected:!active {
        background-color: black;
        color: white;
    }

""" % (font_size)
