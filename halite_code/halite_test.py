import time
from kaggle_environments import make


env = make("halite", debug=True)
env.run(["halite.py", "random", "random", "random"])
with open("halite_replays/" + str(time.time()) + ".html", "w") as text_file:
    text_file.write(env.render(mode="html", width=800, height=600))
