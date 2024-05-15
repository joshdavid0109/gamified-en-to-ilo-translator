import numpy as np

from DQNAagent import DQNAgent

# Define a simple environment for testing
class TestEnvironment:
    def __init__(self):
        self.state = np.random.rand(4)  # Initial state (4 dimensions)
        self.actions = [0, 1, 2]  # Possible actions (3 actions)
        self.done = False

    def reset(self):
        self.state = np.random.rand(4)
        self.done = False
        return self.state

    def step(self, action):
        # Simulate the effect of the action on the environment
        # For testing purposes, we'll just update the state randomly
        self.state = np.random.rand(4)

        # Calculate the reward based on the action
        reward = 1 if action == np.argmax(self.state) else -1

        # Check if the episode is done (for testing purposes, let's say it's never done)
        done = False

        return self.state, reward, done, {}

# Test the DQNAgent
def test_dqn_agent():
    env = TestEnvironment()
    state_size = 4
    action_size = 3
    agent = DQNAgent(state_size, action_size)

    # Test the act() method
    state = env.reset()
    action = agent.act(np.reshape(state, [1, state_size]))
    assert action in env.actions, "Invalid action chosen"

    # Test the remember() method
    next_state, reward, done, _ = env.step(action)
    agent.remember(state, action, reward, next_state, done)
    assert len(agent.memory) == 1, "Memory not updated correctly"

    # Test the replay() method
    agent.replay(batch_size=1)

    # Perform more actions and check if the agent learns
    for _ in range(100):
        state = next_state
        action = agent.act(np.reshape(state, [1, state_size]))
        next_state, reward, done, _ = env.step(action)
        agent.remember(state, action, reward, next_state, done)
        agent.replay(batch_size=32)

    # Test if the agent learns to take the optimal action
    state = env.reset()
    optimal_action = np.argmax(state)
    action = agent.act(np.reshape(state, [1, state_size]))
    assert action == optimal_action, "Agent did not learn the optimal action"

    print("All tests passed!")

if __name__ == "__main__":
    test_dqn_agent()