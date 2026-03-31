# TenzroClaw

OpenClaw skill for the [Tenzro Network](https://tenzro.com) — a purpose-built settlement layer for the AI age.

TenzroClaw provides Python tools for interacting with the Tenzro Ledger via JSON-RPC and Web API: create wallets, send transactions, check balances, register identities, run AI inference, bridge tokens cross-chain, verify proofs, post tasks to the decentralized AI task marketplace, spawn sub-agents, and create agent swarms.

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.10+ and the `requests` library (>=2.32.0).

## Quick Start

```bash
# Join the network (auto-provisions DID + MPC wallet)
python tools/tenzro_rpc.py join_network "Alice"

# Create a standalone wallet
python tools/tenzro_rpc.py create_wallet

# Request testnet tokens (100 TNZO, 24h cooldown)
python tools/tenzro_rpc.py faucet 0x<your_address>

# Check balance
python tools/tenzro_rpc.py get_balance 0x<your_address>

# Send TNZO (value in wei: 1 TNZO = 10^18 wei)
python tools/tenzro_rpc.py send 0x<from> 0x<to> 1000000000000000000

# Check network status
python tools/tenzro_rpc.py status

# Get current block height
python tools/tenzro_rpc.py block_height

# Get chain ID
python tools/tenzro_rpc.py chain_id
```

## Identity

```bash
# Register a human identity (returns a DID)
python tools/tenzro_rpc.py register_identity "Alice"

# Resolve a DID to identity info
python tools/tenzro_rpc.py resolve_did "did:tenzro:human:<uuid>"
```

## AI Models & Inference

```bash
# List available models
python tools/tenzro_rpc.py list_models

# Chat with a served model
python tools/tenzro_rpc.py chat gemma3-270m "What is zero-knowledge proof?"

# List model service endpoints
python tools/tenzro_rpc.py list_model_endpoints
```

## Payments

```bash
# Create a payment challenge (MPP, x402, or native)
python tools/tenzro_rpc.py create_payment mpp "did:tenzro:human:<uuid>" 1000000000000000000

# Verify a payment credential
python tools/tenzro_rpc.py verify_payment <challenge_id> <credential> <payer_did> <payer_address> <amount_wei> TNZO mpp
```

## Task Marketplace

```bash
# Post a task to the decentralized marketplace
python tools/tenzro_rpc.py post_task inference "Summarize this document" "did:tenzro:human:<uuid>" 5000000000000000000

# List available tasks
python tools/tenzro_rpc.py list_tasks

# Submit a quote for a task
python tools/tenzro_rpc.py submit_quote <task_id> 3000000000000000000
```

## Agent Spawning & Swarms

```bash
# Register an agent
python tools/tenzro_rpc.py register_agent "MyAgent" "did:tenzro:human:<uuid>" nlp,reasoning

# Spawn a sub-agent from a parent
python tools/tenzro_rpc.py spawn_agent <parent_id> "SubAgent" research,data

# Run an autonomous agent task
python tools/tenzro_rpc.py run_agent_task <agent_id> "Analyze market trends"

# Create an agent swarm
python tools/tenzro_rpc.py create_swarm <orchestrator_id> researcher:nlp,data analyst:reasoning

# Check swarm status
python tools/tenzro_rpc.py get_swarm_status <swarm_id>

# Terminate a swarm
python tools/tenzro_rpc.py terminate_swarm <swarm_id>
```

## Staking & Providers

```bash
# Stake TNZO tokens as a Validator
python tools/tenzro_rpc.py stake 100000000000000000000 Validator

# Unstake tokens
python tools/tenzro_rpc.py unstake 50000000000000000000

# Register as a provider
python tools/tenzro_rpc.py register_provider ModelProvider

# Get provider stats
python tools/tenzro_rpc.py provider_stats
```

## Available Commands

### Wallet & Balance

| Command | Arguments | Description |
|---------|-----------|-------------|
| `join_network` | `[name] [origin]` | Join as MicroNode (auto-provisions DID + wallet) |
| `create_wallet` | `[key_type]` | Generate new Ed25519/Secp256k1 keypair |
| `create_mpc_wallet` | | Generate 2-of-3 MPC threshold wallet |
| `get_balance` | `<address>` | Get TNZO balance |
| `balance` | `<address>` | Alias for get_balance |
| `send` | `<from> <to> <value_wei>` | Send TNZO transfer |
| `faucet` | `<address>` | Request 100 testnet TNZO |

### Node Status

| Command | Arguments | Description |
|---------|-----------|-------------|
| `status` | | Node health and info |
| `health` | | Health check |
| `block_height` | | Current block height |
| `get_block` | `<height>` | Get block by height |
| `chain_id` | | Get chain ID (default: 1337) |
| `node_info` | | Full node info |

### Identity

| Command | Arguments | Description |
|---------|-----------|-------------|
| `register_identity` | `<name>` | Register human identity |
| `resolve_did` | `<did>` | Resolve DID to identity |
| `resolve_did_document` | `<did>` | Resolve DID to W3C DID Document |
| `set_delegation` | `<did> <max_tx> <max_daily> <ops...>` | Set delegation scope for machine DID |

### Verification

| Command | Arguments | Description |
|---------|-----------|-------------|
| `verify_zk_proof` | `<proof> [inputs...]` | Verify a ZK proof |
| `verify_transaction` | `<tx_hash> <signature> <pub_key>` | Verify transaction signature |
| `verify_settlement` | `<settlement_id> <proof>` | Verify settlement receipt |
| `verify_inference` | `<request_id> <result_hash> <proof>` | Verify inference result |

### Token & Models

| Command | Arguments | Description |
|---------|-----------|-------------|
| `total_supply` | | Get total TNZO supply |
| `token_balance` | `<address>` | Get token balance |
| `list_models` | | List registered AI models |
| `chat` | `<model> <message>` | Chat completion request |
| `list_model_endpoints` | | List running model endpoints |

### Payments

| Command | Arguments | Description |
|---------|-----------|-------------|
| `create_payment` | `<protocol> <payer_did> <amount> [asset] [resource]` | Create payment challenge (mpp/x402/native) |
| `verify_payment` | `<challenge_id> <credential> <payer_did> <payer_addr> <amount> <asset> <protocol>` | Verify payment credential |

### Task Marketplace

| Command | Arguments | Description |
|---------|-----------|-------------|
| `post_task` | `<type> <description> <poster_did> <budget_wei>` | Post task to marketplace |
| `list_tasks` | `[status] [type]` | List tasks (optional filters) |
| `get_task` | `<task_id>` | Get task details |
| `cancel_task` | `<task_id>` | Cancel a task |
| `submit_quote` | `<task_id> <price_wei> [agent_id] [eta_seconds]` | Submit quote for task |

### Agent Templates

| Command | Arguments | Description |
|---------|-----------|-------------|
| `list_templates` | `[category]` | List agent templates |
| `register_template` | `<name> <type> <description> [capabilities...]` | Register agent template |
| `get_template` | `<template_id>` | Get template details |

### Agent Spawning & Swarm

| Command | Arguments | Description |
|---------|-----------|-------------|
| `register_agent` | `<name> <controller_did> [capabilities]` | Register an agent |
| `spawn_agent` | `<parent_id> <name> [capabilities]` | Spawn a sub-agent |
| `run_agent_task` | `<agent_id> <task...>` | Run autonomous agent task |
| `create_swarm` | `<orchestrator_id> <member_specs...>` | Create agent swarm (e.g. `researcher:nlp,data`) |
| `get_swarm_status` | `<swarm_id>` | Get swarm status |
| `terminate_swarm` | `<swarm_id>` | Terminate swarm |

### Cross-Chain Bridge

| Command | Arguments | Description |
|---------|-----------|-------------|
| `bridge_tokens` | `<from_chain> <to_chain> <token> <amount> <sender> <recipient>` | Bridge tokens cross-chain |

### Staking & Providers

| Command | Arguments | Description |
|---------|-----------|-------------|
| `stake` | `<amount_wei> [role]` | Stake TNZO (Validator/ModelProvider/TeeProvider) |
| `unstake` | `<amount_wei>` | Unstake TNZO tokens |
| `register_provider` | `<role>` | Register as provider |
| `provider_stats` | | Get provider statistics |

## Python Library Usage

```python
from tools.tenzro_rpc import (
    join_as_micro_node,
    create_wallet,
    get_balance,
    send_transaction,
    request_faucet,
    register_identity,
    resolve_did,
    chat,
    list_models,
    block_height,
    post_task,
    list_tasks,
    register_agent,
    spawn_agent,
    create_swarm,
    get_swarm_status,
    create_payment_challenge,
    bridge_tokens,
    stake_tokens,
)

# Join the network
result = join_as_micro_node("Alice")
print(result["identity"]["did"])     # did:tenzro:human:<uuid>
print(result["wallet"]["address"])   # 0x<hex>

# Create wallet and get tokens
wallet = create_wallet()
request_faucet(wallet["address"])
balance = get_balance(wallet["address"])
print(f"Balance: {balance['balance_tnzo']} TNZO")

# Chat with AI model
response = chat("gemma3-270m", "Explain blockchain in one sentence.")
print(response["response"])

# Post a task to the marketplace
task = post_task("inference", "Summarize this paper", result["identity"]["did"], 5000000000000000000)
print(f"Task ID: {task['task_id']}")

# Spawn an agent and run a task
agent = register_agent("Researcher", result["identity"]["did"], ["nlp", "research"])
child = spawn_agent(agent["agent_id"], "Analyst", ["data_analysis"])
swarm = create_swarm(agent["agent_id"], [{"name": "worker", "capabilities": ["nlp"]}])
print(f"Swarm ID: {swarm['swarm_id']}")
```

## Endpoints

| Service | URL |
|---------|-----|
| JSON-RPC | `https://rpc.tenzro.network` |
| Web API | `https://api.tenzro.network` |
| Faucet | `https://api.tenzro.network/api/faucet` |
| MCP | `https://mcp.tenzro.network/mcp` |
| A2A | `https://a2a.tenzro.network` |

Override endpoints with environment variables:

```bash
export TENZRO_RPC_URL=http://localhost:8545
export TENZRO_API_URL=http://localhost:8080
```

## Token

**TNZO** is the native token with 18 decimal places. All RPC amounts are in wei (1 TNZO = 10^18 wei).

## OpenClaw Skill

This repository is an [OpenClaw](https://github.com/openclaw) skill. See [SKILL.md](SKILL.md) for the full API reference including:

- JSON-RPC API documentation (50+ methods)
- Identity protocol (TDIP DIDs)
- Payment protocols (MPP, x402, native)
- Cross-chain bridge (LayerZero, Chainlink CCIP, deBridge)
- Task marketplace
- Agent template marketplace
- Agent spawning & swarm orchestration
- MCP integration (24 tools)

## License

Apache License 2.0 - see [LICENSE](LICENSE).
