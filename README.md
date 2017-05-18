# The Mystery Machine

Jack (Shuchuan) Ye, Allen Kim, and Gautam Ramasubramanian

This project is to create a automated narrative generation system - generating small stories using Monte Carlo Tree Search and Reinforcement Learning (Q-Learning).

First, change directories into story_generator.
`cd story_generator`

To generate a story, run:
`python main.py`

To alter parameters, one must edit the main.py file. Towards the bottom, there are a list of parameters one can change that will affect how the stories are generated.

1. max_iter : Number of sentances in story = number of story nodes - 1 = number of story edges
2. max_expansion : Number of expansions in search
3. max_simlength : Maximum length of rollout
4. C : Exploration Constant for selection
5. thres : Minimum MCTS Visits for node expansion
6. mixlambda: The blending constant between MCTS and reinforcement learning - 0 is pure reinforcement learning, 1 is pure MCTS
