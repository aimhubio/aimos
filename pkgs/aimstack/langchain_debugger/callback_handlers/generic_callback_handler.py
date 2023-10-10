"""
This module defines an Aim callback handler for logging generic LangChain executions.

It captures and logs various aspects of LangChain execution, such as:
- LLMs prompts and generations (outputs)
- Tools inputs and outputs
- The start and end of tools
- Agent actions

Logged information is stored in Aim Traces, which can be queried using Aim Query Language.

Classes:
    GenericCallbackHandler: The callback handler class that captures and
     logs LangChain execution events.
"""

from copy import deepcopy
from typing import Any, Dict, List
import time

from aim import Repo

try:
    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import AgentAction, AgentFinish, LLMResult
    from langchain.callbacks.utils import flatten_dict
except ImportError:
    # Raise an exception if LangChain is not installed.
    raise ImportError(
        "To use the GenericCallbackHandler for LangChain, "
        "you need to have the `langchain` python "
        "package installed. Please install it with `pip install langchain`."
    )

from aimstack.base import Metric
from aimstack.langchain_debugger.types.trace import Trace
from aimstack.langchain_debugger.types.step import Step, StepSequence
from aimstack.langchain_debugger.types.action import (
    LLMStartAction,
    LLMEndAction,
    ToolStartAction,
    ToolEndAction,
    ChainStartAction,
    ChainEndAction,
)


class GenericCallbackHandler(BaseCallbackHandler):
    """
    Aim callback handler that captures and logs events during LangChain executions.

    This class is responsible for tracking various LangChain activities and logging them into Aim
    for later analysis and querying. It handles events like the start and end of language models, tools, and
    agent actions.

    Attributes:
        repo (Repo): The Aim repository where logs are stored.
        trace (Trace): The Aim Trace Container that stores execution metadata and logs.
        steps (StepSequence): A StepSequence Sequence that logs Step Records.
        actions (List[Action]): Accumulates actions to be flushed into a Step Records.
        used_tools (Set[str]): Keeps track of tools used in the current LangChain execution.
        tokens_usage_input (Metric): Metric for tracking token usage for input.
        tokens_usage_output (Metric): Metric for tracking token usage for output.
        tokens_usage (Metric): Metric for tracking total token usage.
    """

    def __init__(self, repo_path='aim://0.0.0.0:53800') -> None:
        """
        Initialize the GenericCallbackHandler with the given Aim repository path.

        Args:
            repo_path (str): The Aim repository path or URI. Defaults to 'aim://0.0.0.0:53800'.
        """
        super().__init__()
        # Initialization of attributes
        self.repo = Repo.from_path(repo_path)
        self.trace = None
        self.steps = None
        self.steps_count = 0
        self.actions = []
        self.used_tools = set()
        self.executed_chains = set()
        self.chains_stack = []
        self.tokens_usage_input = None
        self.tokens_usage_output = None
        self.tokens_usage = None
        self.initial_prompts_stored = False
        # Setup logging
        self.setup()

    def setup(self) -> None:
        """
        Initialize Aim logging types and logger.

        Note:
            This function is separated from __init__ for better readability and maintainability.
            However, it could be included in __init__ if desired.
        """
        if self.trace is not None:
            return
        self.trace = Trace(repo=self.repo)
        self.trace['date'] = time.time()
        self.steps = StepSequence(self.trace, name='actions', context={})
        self.tokens_usage_input = Metric(self.trace, name='token-usage-input',
                                         context={})
        self.tokens_usage_output = Metric(self.trace, name='token-usage-output',
                                          context={})
        self.tokens_usage = Metric(self.trace, name='token-usage', context={})

    def flush(self):
        """
        Flush all captured actions into a single Step and log it into StepSequence.

        After flushing, it resets the actions and used_tools for the next set of operations.
        """
        self.steps.track(Step(self.actions))
        del self.trace['used_tools']
        self.trace['used_tools'] = list(self.used_tools)
        self.actions = []
        self.chains_stack = []
        self.initial_prompts_stored = False
        self.steps_count += 1
        self.trace['steps_count'] = self.steps_count
        self.trace['cost'] = 0

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str],
                     invocation_params: Dict[str, Any], **kwargs: Any) -> None:
        """
        Handle the event when a Language Model (LLM) starts.

        Args:
            serialized (Dict[str, Any]): Serialized data for the LLM.
            prompts (List[str]): List of prompts used for the LLM.
            invocation_params (Dict[str, Any]): Parameters used for invoking the LLM.
            kwargs (Any): Additional keyword arguments.
        """
        model_name = invocation_params.get('model_name', 'Unknown')
        temperature = invocation_params.get('temperature')
        prompts = deepcopy(prompts)

        action = LLMStartAction(model_name, temperature, prompts)
        self.actions.append(action)

        if self.initial_prompts_stored is False:
            del self.trace['initial_prompts']
            self.trace['initial_prompts'] = prompts
            self.initial_prompts_stored = True

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """
        Handle the event when a Language Model (LLM) ends.

        Args:
            response (LLMResult): The result object from the LLM.
            kwargs (Any): Additional keyword arguments.
        """
        # Collect and serialize LLM outputs/generations
        generations_log = []
        for generations in response.generations:
            for generation in generations:
                generations_log.append(flatten_dict(generation.dict()))

        llm_output = response.llm_output
        token_usage = llm_output.get('token_usage', {})
        model_name = llm_output.get('model_name', 'Unknown')

        action = LLMEndAction(model_name, token_usage.to_dict(),
                              generations_log)
        self.actions.append(action)

        del self.trace['final_generations']
        self.trace['final_generations'] = generations_log

        # Track token usage as Aim metrics
        self.tokens_usage_input.track(token_usage.get('prompt_tokens', 0))
        self.tokens_usage_output.track(token_usage.get('completion_tokens', 0))
        self.tokens_usage.track(token_usage.get('total_tokens', 0))

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str,
                      **kwargs: Any) -> None:
        """
        Handle the event when a tool starts.

        Args:
            serialized (Dict[str, Any]): Serialized data for the tool.
            input_str (str): Input string for the tool.
            kwargs (Any): Additional keyword arguments.
        """
        tool_name = serialized.get('name', 'Unknown')
        tool_description = serialized.get('description', '')

        action = ToolStartAction(tool_name, tool_description, input_str)
        self.actions.append(action)

    def on_tool_end(self, output: str, name: str, **kwargs: Any) -> None:
        """
        Handle the event when a tool ends.

        Args:
            output (str): Output string from the tool.
            name (str): Name of the tool.
            kwargs (Any): Additional keyword arguments.
        """
        action = ToolEndAction(name, output)
        self.actions.append(action)
        self.used_tools.add(name)

    def on_chain_start(
            self, serialized: Dict[str, Any], inputs: Dict[str, Any],
            **kwargs: Any
    ) -> None:
        """
        Handle the event when a chain starts.

        This function captures the details of a starting chain and stores via ChainStartAction.
        It also updates the state by tracking the current chain's ID.

        Args:
            serialized (Dict[str, Any]): Serialized data for the chain.
            inputs (Dict[str, Any]): Inputs provided to the chain.
            kwargs (Any): Additional keyword arguments.
        """
        chain_id = '.'.join(list(serialized.get('id', [])))

        input = inputs.get('input', '')

        # Create a new ChainStartAction and add it to the actions list
        action = ChainStartAction(chain_id, input)
        self.actions.append(action)

        # Update the chain stack and set of executed chains
        self.chains_stack.append(chain_id)
        self.executed_chains.add(chain_id)


    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """
        Handle the event when a chain ends.

        This function captures the details of an ending chain and logs via ChainEndAction.
        It also updates the state by removing the finished chain from the chain stack.

        Args:
            outputs (Dict[str, Any]): Outputs produced by the chain.
            kwargs (Any): Additional keyword arguments.
        """
        # Pop the last chain from the stack as the finished chain
        finished_chain = self.chains_stack.pop()

        # Extract text and output from the outputs
        text = outputs.get('text', '')
        output = outputs.get('output', '')

        # Create a new ChainEndAction and add it to the actions list
        action = ChainEndAction(finished_chain, text, output)
        self.actions.append(action)

        # Update the trace's executed chains
        del self.trace['executed_chains']
        self.trace['executed_chains'] = self.executed_chains
