"""Unittests for Amass agent."""


def testAgentAmass_withWhoisReverseLookup_returnsDomainList(
        scan_message, test_agent, agent_mock, agent_persist_mock, fp):
    """Tests running the agent and emitting extra subdomains."""
    fp.register(
        ['amass', 'intel', '-whois', '-d', 'ostorlab.co', '-timeout', '10'],
        stdout=b'os.io\nostorlab.co')
    fp.register(
        ['amass', 'enum', '-brute', '-min-for-recursive', '2', '-d', 'ostorlab.co', '-timeout', '10'],
        stdout=b'test.ostorlab.co\nwww.ostorlab.co')

    test_agent.process(scan_message)
    assert len(agent_mock) > 0
    assert agent_mock[0].selector == 'v3.asset.domain_name'
