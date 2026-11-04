import argparse
from pathlib import Path
import sumo_rl
from stable_baselines3 import DQN
import supersuit as ss

parser = argparse.ArgumentParser()
parser.add_argument(
    "--random",
    action="store_true",
    help="学習済みモデルを使わず、ランダム行動(学習前相当)で動かす",
)
args = parser.parse_args()

# 1. 学習時と同じ parallel_env で環境を構築（GUIを有効化）
env = sumo_rl.parallel_env(
    net_file="src/sumo/complex.net.xml",
    route_file="src/sumo/complex.rou.xml",
    use_gui=True,
    num_seconds=1000,
    reward_fn="diff-waiting-time",
    additional_sumo_cmd="--delay 100",  # 1ステップ100ms
)

# 2. 学習時と同じ前処理（パディング）を適用
env = ss.pad_observations_v0(env)
env = ss.pad_action_space_v0(env)

# モデルの読み込み
model = None if args.random else DQN.load("dqn_multiagent_test.zip")

observations, infos = env.reset()
done = False
total_accumulated_waiting_time = 0.0

while not done:
    actions = {}
    for agent_id, obs in observations.items():
        if model is None:
            action = env.action_space(agent_id).sample()
        else:
            # 【注意】VecEnv用モデルのpredictにPettingZooの個別obsをそのまま渡すとshape不一致エラーになるリスクがあります
            action, _ = model.predict(obs, deterministic=True)
        actions[agent_id] = int(action)

    observations, rewards, terminations, truncations, infos = env.step(actions)

    # インデントをループ内に正しく修正
    base_env = env.unwrapped if hasattr(env, "unwrapped") else env
    
    if hasattr(base_env, "traffic_signals"):
        traffic_signals = base_env.traffic_signals.values()
    elif hasattr(base_env, "env") and hasattr(base_env.env, "traffic_signals"):
        traffic_signals = base_env.env.traffic_signals.values()
    else:
        traffic_signals = []

    step_waiting_time = sum(
        sum(ts.get_accumulated_waiting_time_per_lane()) for ts in traffic_signals
    )
    total_accumulated_waiting_time += step_waiting_time

    # すべてのエージェントが終了したか判定
    done = all(terminations.values()) or all(truncations.values())

mode = "random (学習前相当)" if args.random else "trained (学習後)"
print(f"mode: {mode}")
print("累積待ち時間:", total_accumulated_waiting_time)
env.close()