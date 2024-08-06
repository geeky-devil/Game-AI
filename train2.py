import gym
from rl.agents import DQNAgent
from rl.policy import EpsGreedyQPolicy,BoltzmannQPolicy,MaxBoltzmannQPolicy,SoftmaxPolicy
from rl.memory import SequentialMemory
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from agent import CustomEnv
# Create the environment
env = CustomEnv()

# Define the number of actions and observation space dimensions
nb_actions = env.action_space.n
observation_shape = env.observation_space.shape

# Define the model
model = Sequential([
    Flatten(input_shape=(1,) + observation_shape),
    #Dense(input_shape=(1,observation_shape[0]),units=4),
    Dense(32, activation='relu'),
    Dense(32, activation='relu'),
    Dense(32, activation='relu'),
    Dense(32, activation='relu'),
    Dense(nb_actions, activation='softmax')
])

# Define the memory
memory = SequentialMemory(limit=50000, window_length=1)

# Define the policy
policy = EpsGreedyQPolicy(eps=0.1)
#policy =BoltzmannQPolicy()
#policy =MaxBoltzmannQPolicy()
#policy=SoftmaxPolicy()


# Create the DQN agent
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
               target_model_update=1e-2, policy=policy)

# Compile the model
dqn.compile(Adam(lr=1e-3), metrics=['mae',"accuracy"])

# Train the agent
dqn.fit(env, nb_steps=100000, visualize=True, verbose=1)

# Save the trained model
dqn.save_weights('dqn_weights.h5')

# Close the environment
env.close()
