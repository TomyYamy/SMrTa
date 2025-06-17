# SMT-based Multi-Robot Task Allocation

The **S**MT-based **M**ulti-**R**obot **T**ask **A**llocation ("S-MrTa") is an SMT-based approach used in allocating tasks for multi-agent systems and scenarios.

## Setup

To install the command-line interface tool, we use [uv](https://docs.astral.sh/uv/getting-started/installation/) by Astral as the package manager. To install uv, run the following command:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

After setup, run the following command to: (1) create a virtual environment, (2) activate it, and (3) install the S-MrTa tool:

```bash
uv venv && \
source .venv/bin/activate && \
uv pip install .
```

## Example

To validate that the tool installed correctly and is working, run the following command:

```bash
smrta --file="benchmarks/single/config/t_20_a_10_d_5-0.json"
```
