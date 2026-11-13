from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import stable_baselines3.common.results_plotter as rp
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import VecMonitor
import sumo_rl
import supersuit as ss

# 1. ログを保存するディレクトリを指定
log_dir = Path("./logs")
log_dir.mkdir(exist_ok=True)

env = sumo_rl.parallel_env(
    net_file="src/sumo/kousaten5.net.xml",
    route_file="src/sumo/kousaten5.rou.xml",
    use_gui=False,
    num_seconds=1000,
    reward_fn="diff-waiting-time",
)


env = ss.pad_observations_v0(env)  # 信号ごとに観測次元が違うので、大きい方に合わせてパディングする
env = ss.pad_action_space_v0(env)  # 行動空間(フェーズ数)も同様に合わせる
env = ss.pettingzoo_env_to_vec_env_v1(env)
env = ss.concat_vec_envs_v1(
    env, num_vec_envs=1, num_cpus=1, base_class="stable_baselines3"
)

# VecMonitorに直接filenameを指定してログを保存する
dqn_dir = Path("./dqn")

env = VecMonitor(env, filename=str(log_dir / "monitor.csv"))

model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=5000)
model.save(dqn_dir / "dqn_kousaten5")

print("done: dqn_kousaten5.zip を保存しました")


# ログファイルの読み込み（VecMonitorは指定したプレフィックス等でファイルを作るため、保存名に合わせる）
csv_files = list(log_dir.glob("*.csv"))
if csv_files:
  df = pd.read_csv(csv_files[0], skiprows=1)

  # エピソードごとの報酬（r）の推移をプロット
  plt.figure(figsize=(10, 5))
  plt.plot(df.index, df["r"], alpha=0.6, label="Episode Reward")

  plt.xlabel("Episode")
  plt.ylabel("Reward")
  plt.title("Learning Curve (SUMO-RL)")
  plt.legend()
  plt.grid(True)

  # グラフを保存
  plt.savefig(log_dir / "learning_curve.png")
  plt.show()
  print("学習曲線を learning_curve.png として保存しました")

# セッション終了
env.close()
print("SUMO環境とセッションを正常に終了しました。")