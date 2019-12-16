from flask import Flask
app = Flask(__name__)

@app.route(f"/auth/register")
def register():
    return "Hello World!"

@app.route(f"/auth/login")
def login():
    return "Welcome back!"

if __name__ == "__main__":
    app.run()