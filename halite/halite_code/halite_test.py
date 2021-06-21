import time
from kaggle_environments import make


env = make("halite", debug=True)
env.run(["halite_faster_sim.py", "rules_halite.py", "halite_demo.py", "halite_slow_random.py"])
with open("../halite_replays/" + str(time.time()) + ".html", "w") as text_file:
    text_file.write(env.render(mode="html", width=800, height=600))
