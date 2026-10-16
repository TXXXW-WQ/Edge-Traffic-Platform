from pathlib import Path

import sumo_rl
from stable_baselines3 import DQN

net_dir = Path(sumo_rl.__file__).parent / "nets" / "single-intersection"

env = sumo_rl.SumoEnvironment(
    net_file=str(net_dir / "single-intersection.net.xml"),
    route_file=str(net_dir / "single-intersection.rou.xml"),
    single_agent=True,
    use_gui=False,
    num_seconds=1000,
)

model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=5000)
model.save("dqn_test")

env.close()
print("done: dqn_test.zip を保存しました")

