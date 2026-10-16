import argparse
from pathlib import Path

import sumo_rl
from stable_baselines3 import DQN

parser = argparse.ArgumentParser()
parser.add_argument(
    "--random",
    action="store_true",
    help="学習済みモデルを使わず、ランダム行動(学習前相当)で動かす",
)
args = parser.parse_args()

net_dir = Path(sumo_rl.__file__).parent / "nets" / "single-intersection"

env = sumo_rl.SumoEnvironment(
    net_file=str(net_dir / "single-intersection.net.xml"),
    route_file=str(net_dir / "single-intersection.rou.xml"),
    single_agent=True,
    use_gui=True,
    num_seconds=1000,
    additional_sumo_cmd="--delay 100",  # 1ステップ100ms
)
model = None if args.random else DQN.load("dqn_test.zip")

obs, info = env.reset()
done = False
total_reward = 0.0
while not done:
    if model is None:
        action = env.action_space.sample()
    else:
        action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(int(action))
    total_reward += reward
    done = terminated or truncated

mode = "random (学習前相当)" if args.random else "trained (学習後)"
print(f"mode: {mode}")
print("total_reward:", total_reward)
env.close()

