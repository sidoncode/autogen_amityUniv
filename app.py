import os
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Load environment variables from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL          = os.getenv("OPENAI_MODEL", "gpt-4")

if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-your"):
    raise ValueError("Set your OPENAI_API_KEY in the .env file.")

# Shared llm_config used by all agents
llm_config = {
    "model":   MODEL,
    "api_key": OPENAI_API_KEY,
}

researcher = AssistantAgent(
    name="Researcher",
    system_message="You find key facts and statistics on any topic.",
    llm_config=llm_config,
)

writer = AssistantAgent(
    name="Writer",
    system_message="You write clear market research reports from facts.",
    llm_config=llm_config,
)

critic = AssistantAgent(
    name="Critic",
    system_message="""You review reports. If good, say APPROVED.
If not, list specific improvements needed.""",
    llm_config=llm_config,
)

user = UserProxyAgent(name="User", human_input_mode="NEVER", code_execution_config=False)

# Group all agents into one chat room
group_chat = GroupChat(
    agents=[user, researcher, writer, critic],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

user.initiate_chat(manager, message="Write a report on the Indian EV market in 2025")