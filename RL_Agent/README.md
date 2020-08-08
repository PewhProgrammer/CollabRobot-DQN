# Reinforcement Learning Code for Mobile Agents

This source code contains the implementation of DQN with its renowned extensions Double-DQN, Dueling-DQN and Prioritized Experience Replay. In addition, it contains a custom environment, an trajectories logger, several reward function implementations and sensor information feature for the robot. To read more about the functionality, we recommend you to request the thesis for this project.

# Install

Make sure to have python >= v2.7 installed.

Install the requirements

``pip install -r requirements.txt``

Execute this command to run the application

``python run.py``

The run.py file contains various evaluation configurations. The parameters are listed in the config.py file.

# Following Evaluation are Available

- C1 Avoid static hindrances
- C2 Avoid dynamic hindrances
    - C2.1 on a side track
    - C2.2 in an empty room
- C3 Task allocation
- C4 Multi-agent collaboration

# Tensorboard

Various predefined commands for displaying the tensorboard interface:

tensorboard --logdir ./study/algorithm_test/double_dueling_prioritized/sparse_700000

tensorboard --logdir ./study/algorithm_test/concept-1/small_warehouse;./study/algorithm_test/concept-1/small_warehouse

tensorboard --logdir ./study/algorithm_test/concept-1/small_warehouse/tensorboard/experiments

