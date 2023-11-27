from aimstack.langchain_debugger.callback_handlers import GenericCallbackHandler
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI

aim_callback = GenericCallbackHandler(repo_path="aim://0.0.0.0:53800")

callbacks = [aim_callback]
llm = OpenAI(temperature=0, callbacks=callbacks)


tools = load_tools(["serpapi", "llm-math"], llm=llm, callbacks=callbacks)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    callbacks=callbacks,
)

agent.run(
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
)

aim_callback.flush()
