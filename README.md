<h1 align="center">Agent amass</h1>

<p align="center">
<img src="https://img.shields.io/badge/License-Apache_2.0-brightgreen.svg">
<img src="https://img.shields.io/github/languages/top/ostorlab/agent_amass">
<img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
</p>

_Amass performs network mapping of attack surfaces and external asset discovery using open source information gathering and active reconnaissance techniques.._

<p align="center">
<img src="https://github.com/Ostorlab/agent_amass/blob/main/images/cover.png" alt="agent-amass" />
</p>

This repository is an implementation of [Ostorlab Agent](https://pypi.org/project/ostorlab/) for [amass](https://github.com/OWASP/Amass) by OWASP.
  ## Getting Started
  The Amass Agent works collectively with other agents. It's job is to reverse a subdomain name and send all the identified records to the other agents responsible for scanning those records.
  To perform your first scan, simply run the following command:
  ```shell
  ostorlab scan run --install --agent agent/ostorlab/amass --agent agent/ostorlab/subfinder domain-name your-domain.com
  ```
  This command will download and install agents  `agent/ostorlab/amass` & `agent/ostorlab/subfinder` and target the domain  `your-domain`.
  Subfinder Agent will scan for <your-domain>, and sends all identified subdomains, then Amass will reverse those subdomains and send the records.
  You can use any Agent expecting <v3.asset.domain_name> as an in-selector, like Nmap, OpenVas, etc.
  For more information, please refer to the [Ostorlab Documentation](https://github.com/Ostorlab/ostorlab/blob/main/README.md)
  ## Usage
  Agent Amass can be installed directly from the ostorlab agent store or built from this repository.
  ### Install directly from ostorlab agent store
  ```shell
  ostorlab agent install agent/ostorlab/amass
  ```
  ### Build directly from the repository
  1. To build the Amass agent you need to have [ostorlab](https://pypi.org/project/ostorlab/) installed in your machine. If you have already installed ostorlab, you can skip this step.
  ```shell
  pip3 install ostorlab
  ```
  2. Clone this repository.
  ```shell
  git clone https://github.com/Ostorlab/agent_amass.git && cd agent_amass
  ```
  3. Build the agent image using ostorlab cli.
  ```shell
  ostortlab agent build --file=ostorlab.yaml
  ```
  You can pass the optional flag `--organization` to specify your organisation. The organization is empty by default.
  4. Run the agent using on of the following commands:
    * If you did not specify an organization when building the image:
      ```shell
      ostorlab scan run --agent agent//amass --agent agent//subfinder domain-name your-domain.com
      ```
    * If you specified an organization when building the image:
      ```shell
      ostorlab scan run --agent agent/[ORGANIZATION]/subfinder --agent agent/[ORGANIZATION]/amass  domain-name your-domain.com

  ## License

  License: [Apache-2.0](./LICENSE)