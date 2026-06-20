import webbrowser



def open_browser():
    webbrowser.open("https://www.google.com")


def open_ytb():
    webbrowser.open("https://www.youtube.com")


commands = {"открой браузер": open_browser,
            "открой ютуб": open_ytb,
        }


def commands_list_func(text_from_user):
    text_l = text_from_user.lower()
    for key, val in commands.items():
        if key in text_l:
            print("WWWWW")
            val()
            return True


    return False
