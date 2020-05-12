from serpent.machine_learning.reinforcement_learning.agent import Agent

from serpent.game_frame import GameFrame
from serpent.game_frame_buffer import GameFrameBuffer

from serpent.enums import InputControlTypes

from serpent.utilities import SerpentError

import os

import numpy as np

try:
    from tensorforce.agents import PPOAgent as TFPPOAgent  # Currently matching the API of tensorforce 0.3.5.1
except ImportError:
    raise SerpentError("Setup has not been been performed for the ML module. Please run 'serpent setup ml'")


class PPOAgent(Agent):

    def __init__(
        self,
        name,
        game_inputs=None,
        callbacks=None,
        input_shape=None,
        input_type=None,
        use_tensorboard=True,
        tensorforce_kwargs=None
    ):
        super().__init__(name, game_inputs=game_inputs, callbacks=callbacks)

        if input_shape is None or not isinstance(input_shape, tuple):
            raise SerpentError("'input_shape' should be a tuple...")

        if input_type is None or input_type not in ["bool", "int", "float"]:
            raise SerpentError("'input_type' should be one of bool|int|float...")

        states_spec = {"type": input_type, "shape": input_shape}

        actions_spec = self._generate_actions_spec()

        summary_spec = None

        if use_tensorboard:
            summary_spec = {
                "directory": "./tensorboard/",
                "steps": 50,
                "labels": [
                    "configuration",
                    "gradients_scalar",
                    "regularization",
                    "inputs",
                    "losses",
                    "variables"
                ]
            }

        default_network_spec = [
            {"type": "conv2d", "size": 32, "window": 8, "stride": 4},
            {"type": "conv2d", "size": 64, "window": 4, "stride": 2},
            {"type": "conv2d", "size": 64, "window": 3, "stride": 1},
            {"type": "flatten"},
            {"type": "dense", "size": 1024}
        ]

        agent_kwargs = dict(
            batch_size=1024,
            batched_observe=1024,
            network_spec=default_network_spec,
            device=None,
            session_config=None,
            saver_spec=None,
            distributed_spec=None,
            discount=0.99,
            variable_noise=None,
            states_preprocessing_spec=None,
            explorations_spec=None,
            reward_preprocessing_spec=None,
            distributions_spec=None,
            entropy_regularization=0.01,
            keep_last_timestep=True,
            baseline_mode=None,
            baseline=None,
            baseline_optimizer=None,
            gae_lambda=None,
            likelihood_ratio_clipping=None,
            step_optimizer=None,
            optimization_steps=10
        )

        if isinstance(tensorforce_kwargs, dict):
            for key, value in tensorforce_kwargs.items():
                if key in agent_kwargs:
                    agent_kwargs[key] = value

        self.agent = TFPPOAgent(
            states_spec=states_spec,
            actions_spec=actions_spec,
            summary_spec=summary_spec,
            scope="ppo",
            **agent_kwargs
        )

        try:
            self.restore_model()
        except Exception:
            pass

    def generate_actions(self, state, **kwargs):
        if isinstance(state, GameFrame):
            self.current_state = state.frame
        elif isinstance(state, GameFrameBuffer):
            self.current_state = np.stack(
                [game_frame.frame for game_frame in state.frames],
                axis=2
            )
        else:
            self.current_state = state

        agent_actions = self.agent.act(self.current_state)
        actions = list()

        for index, game_inputs_item in enumerate(self.game_inputs):
            if game_inputs_item["control_type"] == InputControlTypes.DISCRETE:
                label = self.game_inputs_mappings[index][agent_actions[game_inputs_item["name"]]]
                action = game_inputs_item["inputs"][label]

                actions.append((label, action, None))
            elif game_inputs_item["control_type"] == InputControlTypes.CONTINUOUS:
                label = game_inputs_item["name"]
                action = game_inputs_item["inputs"]["events"]
                input_value = float(agent_actions[label])

            actions.append((label, action, input_value))

        return actions

    def observe(self, reward=0, terminal=False, **kwargs):
        if self.current_state is None:
            return None

        if self.callbacks.get("before_observe") is not None:
            self.callbacks["before_observe"]()

        will_update = self.agent.batch_count == self.agent.batch_size - 1

        if will_update:
            if self.callbacks.get("before_update") is not None:
                self.callbacks["before_update"]()

            self.agent.observe(reward=reward, terminal=terminal)
            self.save_model()

            if self.callbacks.get("after_update") is not None:
                self.callbacks["after_update"]()
        else:
            self.agent.observe(reward=reward, terminal=terminal)

        self.current_state = None

        self.current_reward = reward
        self.cumulative_reward += reward

        self.analytics_client.track(event_key="REWARD", data={"reward": self.current_reward})

        if terminal:
            self.analytics_client.track(event_key="TOTAL_REWARD", data={"reward": self.cumulative_reward})

        if self.callbacks.get("after_observe") is not None:
            self.callbacks["after_observe"]()

    def save_model(self):
        self.agent.save_model(directory=os.path.join(os.getcwd(), "datasets", self.name, self.name), append_timestep=False)

    def restore_model(self):
        self.agent.restore_model(directory=os.path.join(os.getcwd(), "datasets", self.name))

    def _generate_actions_spec(self):
        actions_spec = dict()

        for game_inputs_item in self.game_inputs:
            if game_inputs_item["control_type"] == InputControlTypes.DISCRETE:
                actions_spec[game_inputs_item["name"]] = dict(type="int", num_actions=len(game_inputs_item["inputs"]))
            elif game_inputs_item["control_type"] == InputControlTypes.CONTINUOUS:
                actions_spec[game_inputs_item["name"]] = dict(
                    type="float",
                    min_value=game_inputs_item["inputs"]["minimum"],
                    max_value=game_inputs_item["inputs"]["maximum"]
                )

        return actions_spec
