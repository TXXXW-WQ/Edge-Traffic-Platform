import supersuit as ss
import sumo_rl
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import VecMonitor

env = sumo_rl.parallel_env(
    net_file="src/sumo/complex.net.xml", # 適宜読み替え
    route_file="src/sumo/complex.rou.xml", # 適宜読み替え
    use_gui=False,
    num_seconds=1000,
)
env = ss.pad_observations_v0(env)  # 信号ごとに観測次元が違うので、大きい方に合わせてパディングする
env = ss.pad_action_space_v0(env)  # 行動空間(フェーズ数)も同様に合わせる
env = ss.pettingzoo_env_to_vec_env_v1(env)
env = ss.concat_vec_envs_v1(env, num_vec_envs=1, num_cpus=1, base_class="stable_baselines3")
env = VecMonitor(env)

model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=50000)
model.save("dqn_multiagent_test")

print("done: dqn_multiagent_test.zip を保存しました")

