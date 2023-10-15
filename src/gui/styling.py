from src.consts import assets as assets_const
from src.utils import assets

font_size = 14

style = """
    QWidget#MainWidget {
        background-color: #302626;
    }

    QWidget {
        font-family: "CookieRun Bold";
        font-size: %s;
        color: #C3AF75;
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
