"""Pytest fixture for the Amass agent."""

import json
import pathlib

import pytest
from ostorlab.agent import definitions as agent_definitions
from ostorlab.agent.message import message
from ostorlab.runtimes import definitions as runtime_definitions
from ostorlab.utils import defintions as utils_definitions

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
def no_test_agent():
    with (pathlib.Path(__file__).parent.parent / "ostorlab.yaml").open() as yaml_o:
        definition = agent_definitions.AgentDefinition.from_yaml(yaml_o)
        settings = runtime_definitions.AgentSettings(
            key="agent/ostorlab/amass",
            bus_url="NA",
            bus_exchange_topic="NA",
            redis_url="redis://redis",
            args=[
                utils_definitions.Arg(
                    name="reverse_whois",
                    type="boolean",
                    value=json.dumps(False).encode(),
                ),
                utils_definitions.Arg(
                    name="subdomain_enumeration",
                    type="boolean",
                    value=json.dumps(False).encode(),
                ),
            ],
            healthcheck_port=5301,
        )
        return amass_agent.AmassAgent(definition, settings)


@pytest.fixture
def test_agent():
    with (pathlib.Path(__file__).parent.parent / "ostorlab.yaml").open() as yaml_o:
        definition = agent_definitions.AgentDefinition.from_yaml(yaml_o)
        settings = runtime_definitions.AgentSettings(
            key="agent/ostorlab/amass",
            bus_url="NA",
            bus_exchange_topic="NA",
            redis_url="redis://redis",
            args=[
                utils_definitions.Arg(
                    name="reverse_whois",
                    value=json.dumps(True).encode(),
                    type="boolean",
                ),
            ],
            healthcheck_port=5302,
        )
        return amass_agent.AmassAgent(definition, settings)
