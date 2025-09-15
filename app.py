from flask import Flask, session, render_template, make_response, request, redirect, url_for
from game import Engine, init_engine


app = Flask(__name__)
app.secret_key = 'dev-string'


def get_engine() -> Engine:
    save_bytes = session.get("engine")
    if not save_bytes:
        raise Exception("Engine not found in session")
    return init_engine(save_bytes)


def get_or_create_engine() -> Engine:
    try:
        return get_engine()
    except:
        return Engine()


def save_engine(engine: Engine):
    session.update({"engine": engine.save()})


def clear_engine():
    session.pop("engine")



@app.route("/")
def view():
    message = request.args.get("message")

    e = get_or_create_engine()
    e.buffer().clear()

    x_pos = e.player().x()
    y_pos = e.player().y()
    room = e.world().room(x_pos, y_pos)
    if not room:
        return make_response(500, "I think you broke the game!")

    e.buffer().print(room.intro_text())

    if room.enemy():
        if room.enemy().alive():
            e.buffer().print(room.enemy().alive_text())
        else:
            e.buffer().print(room.enemy().dead_text())

    if room.trader():
        e.buffer().print(room.trader().greet_text())

    actions = e.get_actions()
    for action in actions:
        e.buffer().print("{}. {}".format(action.key(), action.desc()))

    debug = {
        "world": e.world(),
        "player": e.player(),
        "room": room,
        "enemy": room.enemy(),
    }
    save_engine(e)
    return render_template("home.html", console=e.buffer().console(), message=message, debug=debug)


@app.route("/process",  methods=["POST"])
def process():
    if request.method != "POST":
        return make_response(500, "Unexpected form method")
    
    e = get_engine()
    input = request.form["input"].lower()
    
    ok = e.handle_input(input)
    if not ok:
        return redirect(url_for(".view", message="Invalid input"))
    
    save_engine(e)
    return redirect(url_for(".view"))


@app.route("/reset")
def reset():
    try:
        clear_engine()
    except KeyError:
        pass
    return redirect(url_for(".view"))



if __name__ == "__main__":
#    with app.test_client() as client:
#        response = client.get("/")
    app.run(debug=True)