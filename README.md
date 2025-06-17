# SMT-based Multi-Robot Task Allocation

The **S**MT-based **M**ulti-**R**obot **T**ask **A**llocation ("S-MrTa") is an SMT-based approach used in allocating tasks for multi-agent systems and scenarios.

This is checked by Ubuntu 24.04.

## Setup

To install the command-line interface tool, we use [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
sudo snap install astral-uv
```

## Installation

After setup, run the following command:

```bash
$ uv venv
$ source .venv/bin/activate
(SMrTa)$ uv pip install .
```

## Example

To validate that the tool installed correctly and is working, run the following command:

```bash
smrta --file="benchmarks/single/config/t_20_a_10_d_5-0.json"
```
