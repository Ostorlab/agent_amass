"""Amass network reconnaissance agent implementation."""
import logging

import tld
from ostorlab.agent import agent
from ostorlab.agent import definitions as agent_definitions
from ostorlab.agent import message as m
from ostorlab.agent.mixins import agent_persist_mixin
from ostorlab.runtimes import definitions as runtime_definitions
from rich import logging as rich_logging
from agent import amass

logging.basicConfig(
    format='%(message)s',
    datefmt='[%X]',
    level='INFO',
    force=True,
    handlers=[rich_logging.RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)
STORAGE_NAME = 'agent_amass_storage'
DEFAULT_TIMEOUT_MINUTES = 10


class AmassAgent(agent.Agent, agent_persist_mixin.AgentPersistMixin):
    """Amass agent with reverse whois lookup and subdomain enumeration."""

    def __init__(self,
                 agent_definition: agent_definitions.AgentDefinition,
                 agent_settings: runtime_definitions.AgentSettings) -> None:

        agent.Agent.__init__(self, agent_definition, agent_settings)
        agent_persist_mixin.AgentPersistMixin.__init__(self, agent_settings)

    def process(self, message: m.Message) -> None:
        """Process messages of type  v3.asset.domain_name
        Runs amass on the domain name and emits back the findings.

        Args:
            message: The received message.
        """
        logger.info('processing message of selector : %s', message.selector)
        domain_name = message.data['name']
        canonalized_domain = tld.get_tld(domain_name, as_object=True, fix_protocol=True, fail_silently=True)
        if canonalized_domain is None:
            return

        canonalized_domain = canonalized_domain.fld

        if self.set_add(STORAGE_NAME, canonalized_domain) is True:
            subdomains = amass.intel_whois(domain_name, timeout=DEFAULT_TIMEOUT_MINUTES)
            for sub in subdomains:
                self.emit(selector='v3.asset.domain_name', data={'name': sub})

            subdomains = amass.enum_subdomain(domain_name, timeout=DEFAULT_TIMEOUT_MINUTES)
            for sub in subdomains:
                self.emit(selector='v3.asset.domain_name', data={'name': sub})
        else:
            logger.info('%s has already been processed. skipping for now.', domain_name)


if __name__ == '__main__':
    logger.info('starting agent ...')
    AmassAgent.main()
