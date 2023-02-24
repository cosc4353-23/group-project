from website import createApp
app = createApp()

# if we run this file (main.py), then we run the app
# if you import main.py from another file, then web server would automatically run
# we only want web server to run if you execute main.py
if __name__ == '__main__':
    # app.run --> starts up a web server, debug=True means web server re runs anytime a change is made
    app.run(debug=True)
