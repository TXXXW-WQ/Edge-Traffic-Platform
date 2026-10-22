学習スクリプト実行
export SUMO_HOME="$(uv run python -c 'import sumo; print(sumo.SUMO_HOME)')"
uv run python src/edge_traffic_platform/minimal_train.py

sumo-gui
学習前
uv run python src/edge_traffic_platform/minimal_gui_check.py --random

学習後
uv run python src/edge_traffic_platform/minimal_gui_check.py

※GUIがうまく起動しないはWSLを再起動！


