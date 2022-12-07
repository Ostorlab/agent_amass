"""Pytest fixture for the Amass agent."""
import pathlib

import pytest
from ostorlab.agent import definitions as agent_definitions
from ostorlab.agent.message import message
from ostorlab.runtimes import definitions as runtime_definitions

from agent import amass_agent


@pytest.fixture
def scan_message():
    """Creates a dummy message of type v3.asset.domain_name to be used by the agent for testing purposes."""
    selector = "v3.asset.domain_name"
    msg_data = {
        "name": "ostorlab.co",
    }
    return message.Message.from_data(selector, data=msg_data)


@pytest.fixture
def test_agent():
    with (pathlib.Path(__file__).parent.parent / "ostorlab.yaml").open() as yaml_o:
        definition = agent_definitions.AgentDefinition.from_yaml(yaml_o)
        settings = runtime_definitions.AgentSettings(
            key="agent/ostorlab/amass",
            bus_url="NA",
            bus_exchange_topic="NA",
            redis_url="redis://redis",
            args=[],
            healthcheck_port=5301,
        )
        return amass_agent.AmassAgent(definition, settings)
