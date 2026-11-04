from pathlib import Path
import sumo_rl
import matplotlib.pyplot as plt
import pandas as pd
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor

# 1. ログを保存するディレクトリを指定
log_dir = Path("./logs")
log_dir.mkdir(exist_ok=True)

net_dir = Path(sumo_rl.__file__).parent / "nets" / "single-intersection"

env = sumo_rl.SumoEnvironment(
    net_file=str(net_dir / "single-intersection.net.xml"),
    route_file=str(net_dir / "single-intersection.rou.xml"),
    single_agent=True,
    use_gui=False,
    num_seconds=1000,
)

# Monitorラッパーで環境を包む（エピソードごとの報酬や長さが自動でCSVに記録される）
env = Monitor(env, filename=str(log_dir))

model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=5000)
model.save("dqn_test")

env.close()
print("done: dqn_test.zip を保存しました")


csv_files = list(log_dir.glob("*.csv"))
if csv_files:
    df = pd.read_csv(csv_files[0], skiprows=1)

    # エピソードごとの報酬（r）の推移をプロット
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["r"], alpha=0.6, label="Episode Reward")

    # トレンドを見やすくするために移動平均（Moving Average）線も追加すると綺麗になります
    window_size = 10
    if len(df) >= window_size:
        df["rolling_mean"] = df["r"].rolling(window=window_size).mean()
        plt.plot(
            df.index,
            df["rolling_mean"],
            color="red",
            linewidth=2,
            label=f"Rolling Mean ({window_size} episodes)",
        )

    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Learning Curve (SUMO-RL)")
    plt.legend()
    plt.grid(True)

    # グラフを保存
    plt.savefig(log_dir / "learning_curve.png")
    plt.show()
    print("学習曲線を learning_curve.png として保存しました")

