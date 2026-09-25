import gymnasium as gym
import numpy as np
from gymnasium import spaces

class CITestEnvironment(gym.Env):
    """
    Custom Environment that follows gym interface for CI/CD Test Selection.
    """
    metadata = {"render_modes": ["human"]}

    def __init__(self, features: dict, true_outcomes: dict, failure_bonus: float = 10.0, alpha: float = 1.0):
        super(CITestEnvironment, self).__init__()
        
        self.features = features
        self.true_outcomes = true_outcomes
        self.test_names = list(features.keys())
        self.num_tests = len(self.test_names)
        
        self.failure_bonus = failure_bonus
        self.alpha = alpha # Penalty multiplier for execution time
        
        # Action Space: Discrete, choose exactly one test (0 to num_tests - 1)
        self.action_space = spaces.Discrete(self.num_tests)
        
        # Observation Space: For each test -> [is_dependent, fail_rate, avg_duration, is_executed]
        # Shape: (num_tests, 4)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, 
            shape=(self.num_tests, 4), 
            dtype=np.float32
        )
        
        self.executed_tests = set()
        self.failures_found = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.executed_tests = set()
        self.failures_found = 0
        
        return self._get_obs(), self._get_info()

    def _get_obs(self):
        """Constructs the current state matrix."""
        obs = np.zeros((self.num_tests, 4), dtype=np.float32)
        for i, test in enumerate(self.test_names):
            feat = self.features[test]
            is_executed = 1.0 if i in self.executed_tests else 0.0
            obs[i] = [
                feat['is_dependent'],
                feat['fail_rate'],
                feat['avg_duration'],
                is_executed
            ]
        return obs

    def _get_info(self):
        """Returns extra info, like which actions are valid (remaining tests)."""
        valid_actions = [i for i in range(self.num_tests) if i not in self.executed_tests]
        return {
            "valid_actions": valid_actions,
            "failures_found": self.failures_found
        }

    def step(self, action: int):
        # 1. Check if action is valid (test hasn't been run yet)
        if action in self.executed_tests:
            # Invalid action penalty to teach the agent not to pick already executed tests
            return self._get_obs(), -5.0, False, False, self._get_info()
            
        # 2. Mark test as executed
        self.executed_tests.add(action)
        test_name = self.test_names[action]
        
        # 3. Observe the outcome and duration
        outcome = self.true_outcomes.get(test_name, "PASS")
        duration = self.features[test_name]['avg_duration']
        
        # 4. Calculate Reward: R = (Failure Detected ? B : 0) - (alpha * Execution Time)
        reward = -(self.alpha * duration)
        if outcome == "FAIL":
            reward += self.failure_bonus
            self.failures_found += 1
            
        # 5. Check Termination (Exhaustive Completion - all tests executed)
        terminated = len(self.executed_tests) == self.num_tests
        truncated = False # We don't artificially truncate episodes here
        
        return self._get_obs(), float(reward), terminated, truncated, self._get_info()

    def render(self):
        print(f"Executed: {len(self.executed_tests)}/{self.num_tests} | Failures Found: {self.failures_found}")


# ============================================================
# TEST THE ENVIRONMENT (RANDOM AGENT)
# ============================================================
if __name__ == "__main__":
    # Mock data based on your exact Feature Engine output
    mock_features = {
      "tests/test_calculator.py::test_add": {"is_dependent": 1, "fail_rate": 0.0, "avg_duration": 0.1},
      "tests/test_calculator.py::test_divide": {"is_dependent": 1, "fail_rate": 0.0, "avg_duration": 0.1},
      "tests/test_calculator.py::test_multiply": {"is_dependent": 1, "fail_rate": 0.0, "avg_duration": 0.1},
      "tests/test_calculator.py::test_subtract": {"is_dependent": 1, "fail_rate": 0.5, "avg_duration": 0.1}
    }
    
    # We pretend for this specific episode/commit that 'test_subtract' will actually fail
    mock_true_outcomes = {
        "tests/test_calculator.py::test_subtract": "FAIL"
    }
    
    env = CITestEnvironment(features=mock_features, true_outcomes=mock_true_outcomes)
    
    obs, info = env.reset()
    print("--- Starting Random Episode ---")
    
    terminated = False
    step_count = 1
    
    while not terminated:
        # Instead of the RL agent, we just pick a random valid test
        action = np.random.choice(info['valid_actions'])
        test_picked = env.test_names[action]
        
        obs, reward, terminated, truncated, info = env.step(action)
        
        print(f"Step {step_count}: Selected '{test_picked}'")
        print(f"  -> Reward: {reward} | Failures Found: {info['failures_found']}")
        step_count += 1
        
    print("--- Episode Complete (Exhaustive Full-Suite Run) ---")