学習スクリプト実行
export SUMO_HOME="$(uv run python -c 'import sumo; print(sumo.SUMO_HOME)')"
uv run python src/edge_traffic_platform/minimal_train.py

export SUMO_HOME="$(uv run python -c 'import sumo; print(sumo.SUMO_HOME)')"
uv run python src/edge_traffic_platform/minimal_train_multiagent.py


sumo-gui
学習前
uv run python src/edge_traffic_platform/minimal_gui_check.py --random

学習後
uv run python src/edge_traffic_platform/minimal_gui_check.py

※GUIがうまく起動しないはWSLを再起動！


routeファイルを生成
※-pの値を変更することで交通量を変更(p秒に一台)
export SUMO_HOME="$(uv run python -c 'import sumo; print(sumo.SUMO_HOME)')"
uv run python "$SUMO_HOME/tools/randomTrips.py" \
  -n src/sumo/complex.net.xml \
  -r src/sumo/complex.rou.xml \
  -e 1000 \
  -p 3.0 \
  --fringe-factor 100