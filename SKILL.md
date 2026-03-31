---
name: tenzroclaw
version: 0.1.0
author: Tenzro Network
description: TenzroClaw — OpenClaw skill for the Tenzro Network. Create wallets, send transactions, check balances, register identities, set delegation scopes, make payments, run AI inference, bridge tokens cross-chain, verify proofs, post tasks to the decentralized AI task marketplace, publish and discover agent templates, spawn sub-agents, create agent swarms, and request testnet tokens.
tags:
  - blockchain
  - ai
  - identity
  - payments
  - bridge
  - inference
  - web3
  - task_marketplace
  - agent_marketplace
  - swarm
  - autonomous_agents
---

# TenzroClaw

You can interact with the Tenzro blockchain network using its JSON-RPC, Web API, and MCP endpoints. Tenzro is an L1 blockchain designed for the AI age, providing identity, settlement, TEE security, and ZK proof verification.

## Endpoints

| Service | URL | Description |
|---------|-----|-------------|
| JSON-RPC | `https://rpc.tenzro.network` | EVM-compatible JSON-RPC (port 8545) |
| Web API | `https://api.tenzro.network` | REST verification and status API (port 8080) |
| Faucet | `https://api.tenzro.network/api/faucet` | Testnet TNZO token faucet |
| MCP | `https://mcp.tenzro.network/mcp` | Model Context Protocol server (port 3001) |
| A2A | `https://a2a.tenzro.network` | Agent-to-Agent protocol (port 3002) |

For local development, replace the hostnames with `localhost` and use the ports shown above.

## Token

**TNZO** is the native token with 18 decimal places. Amounts in the RPC are in wei (1 TNZO = 10^18 wei). The default gas price is 1 Gwei (10^9 wei).

## Authentication

No authentication is required for read operations. Write operations (transactions) require a valid Ed25519 or Secp256k1 signature.

---

## JSON-RPC API

All RPC calls use `POST` with `Content-Type: application/json`. The request body follows JSON-RPC 2.0:

```json
{
  "jsonrpc": "2.0",
  "method": "<method_name>",
  "params": { ... },
  "id": 1
}
```

### Create a Wallet

Generate a new Ed25519 keypair and derive an address.

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_createAccount",
    "params": {"key_type": "ed25519"},
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "address": "0x<hex>",
    "public_key": "<hex>",
    "private_key": "<hex>",
    "key_type": "ed25519"
  },
  "id": 1
}
```

Store the `private_key` securely. You need it to sign transactions.

### Create an MPC Wallet

Generate a 2-of-3 threshold MPC wallet (no seed phrase needed).

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_createWallet",
    "params": {},
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "wallet_id": "<uuid>",
    "address": "0x<hex>",
    "public_key": "<hex>",
    "key_type": "ed25519",
    "threshold": 2,
    "total_shares": 3
  },
  "id": 1
}
```

### Check Balance

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_getBalance",
    "params": {"address": "0x<address>"},
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": "0x56bc75e2d63100000",
  "id": 1
}
```

The result is a hex string in wei. `0x56bc75e2d63100000` = 100 TNZO.

Also available via EVM-compatible method:
```json
{"jsonrpc":"2.0","method":"eth_getBalance","params":{"address":"0x..."},"id":1}
```

### Send Transaction

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_sendRawTransaction",
    "params": {
      "from": "0x<sender>",
      "to": "0x<recipient>",
      "value": 1000000000000000000,
      "gas_limit": 21000,
      "gas_price": 1000000000,
      "nonce": 0
    },
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": "0x<transaction_hash>",
  "id": 1
}
```

### Get Block Height

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tenzro_blockNumber","params":{},"id":1}'
```

### Get Block by Number

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tenzro_getBlock","params":{"height":0},"id":1}'
```

Use `"params":["latest"]` for the most recent block.

### Get Chain ID

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":{},"id":1}'
```

Default chain ID is `0x539` (1337).

### Get Node Info

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tenzro_nodeInfo","params":{},"id":1}'
```

### Get Token Supply

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tenzro_totalSupply","params":{},"id":1}'
```

### List Registered Models

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tenzro_listModels","params":{"category":"text"},"id":1}'
```

Optionally filter by `category` (text, image, audio, video, text_image, text_audio, multimodal) or `name` (substring match).

---

## Identity (Tenzro Identity Protocol)

Tenzro uses decentralized identifiers (DIDs) for both humans and machines.

- Human DID format: `did:tenzro:human:<uuid>`
- Machine DID format: `did:tenzro:machine:<controller>:<uuid>` or `did:tenzro:machine:<uuid>` (autonomous)

### Register Human Identity

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_registerIdentity",
    "params": {
      "display_name": "Alice"
    },
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "did": "did:tenzro:human:<uuid>",
    "status": "registered",
    "private_key": "<hex>"
  },
  "id": 1
}
```

Optionally pass `"public_key": "<hex>"` and `"key_type": "ed25519"` to use an existing keypair.

### Resolve Identity

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_resolveIdentity",
    "params": {"did": "did:tenzro:human:<uuid>"},
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "did": "did:tenzro:human:<uuid>",
    "status": "active",
    "is_human": true,
    "is_machine": false,
    "display_name": "Alice",
    "key_count": 1,
    "credential_count": 0,
    "service_count": 0
  },
  "id": 1
}
```

### Resolve DID Document (W3C Standard)

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_resolveDidDocument",
    "params": {"did": "did:tenzro:human:<uuid>"},
    "id": 1
  }'
```

### Join as MicroNode

Join the Tenzro Network as a full participant — zero-install. Auto-provisions a TDIP DID,
MPC wallet, and all 10 network capabilities in a single RPC call.

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_joinAsMicroNode",
    "params": [{
      "display_name": "Alice",
      "origin": "cli",
      "participant_type": "human"
    }],
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "identity": { "did": "did:tenzro:human:<uuid>", "display_name": "Alice", "identity_type": "human", "status": "active" },
    "wallet": { "address": "0x<hex>", "wallet_type": "mpc", "balance": "0" },
    "capabilities": { "inference": true, "payments": true, "agent_collaboration": true, "mcp_tools": true, "task_execution": true, "chain_query": true, "smart_contracts": true, "tee_services": true, "bridge": true, "governance": true },
    "network": { "rpc": "https://rpc.tenzro.network", "mcp": "https://mcp.tenzro.network/mcp", "a2a": "https://a2a.tenzro.network" },
    "is_micro_node": true,
    "chain_id": 1337
  }
}
```

Falls back to `tenzro_participate` for nodes that don't yet support `tenzro_joinAsMicroNode`.

**Python (tenzro_rpc.py):**
```python
from tools.tenzro_rpc import join_as_micro_node
result = join_as_micro_node("Alice")
print(result["identity"]["did"])    # did:tenzro:human:<uuid>
print(result["wallet"]["address"])  # 0x<hex>
```

### Set Delegation Scope

Define spending limits, allowed operations, payment protocols, and chains for a machine identity.

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_setDelegationScope",
    "params": {
      "machine_did": "did:tenzro:machine:<controller>:<uuid>",
      "max_transaction_value": 10000000,
      "max_daily_spend": 100000000,
      "allowed_operations": ["InferenceRequest", "Transfer"],
      "allowed_payment_protocols": ["mpp", "x402", "native"],
      "allowed_chains": ["tenzro", "base", "ethereum"]
    },
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "machine_did": "did:tenzro:machine:<controller>:<uuid>",
    "delegation_scope": {
      "max_transaction_value": 10000000,
      "max_daily_spend": 100000000,
      "allowed_operations": ["InferenceRequest", "Transfer"],
      "allowed_payment_protocols": ["mpp", "x402", "native"],
      "allowed_chains": ["tenzro", "base", "ethereum"]
    },
    "status": "updated"
  },
  "id": 1
}
```

---

## Payments

Tenzro supports three payment protocols:
- **MPP** (Machine Payments Protocol) — session-based streaming payments, ideal for per-token AI inference billing
- **x402** (Coinbase HTTP 402) — stateless one-shot payments, ideal for API calls and data downloads
- **native** — direct TNZO transfer on the Tenzro ledger

### Create Payment Challenge

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_createPaymentChallenge",
    "params": {
      "protocol": "x402",
      "resource": "/api/inference",
      "amount": 100,
      "asset": "USDC",
      "recipient": "0x<recipient_address>"
    },
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "challenge_id": "<uuid>",
    "protocol": "x402",
    "resource": "/api/inference",
    "amount": 100,
    "asset": "USDC",
    "recipient": "0x<recipient_address>",
    "expires_at": "2025-01-01T01:00:00Z"
  },
  "id": 1
}
```

### Verify Payment

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_verifyPayment",
    "params": {
      "challenge_id": "<challenge_uuid>",
      "protocol": "x402",
      "payer_did": "did:tenzro:human:<uuid>",
      "payer_address": "0x<payer_address>",
      "amount": 100,
      "asset": "USDC",
      "signature": "0x<hex_signature>"
    },
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "verified": true,
    "receipt_id": "<uuid>",
    "settled": true
  },
  "id": 1
}
```

### List Payment Protocols

> **Note:** This is available as an MCP tool (`list_payment_protocols`) on the MCP server at `https://mcp.tenzro.network/mcp`, not as a JSON-RPC method.

Supported protocols: **MPP** (session-based streaming), **x402** (stateless one-shot), **native** (direct TNZO transfer).

---

## AI Models & Inference

### List Models

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_listModels",
    "params": {"category": "text"},
    "id": 1
  }'
```

Supported categories: `text`, `image`, `audio`, `video`, `text_image`, `text_audio`, `multimodal`. You can also filter by `name`.

**Response includes load information for serving models:**
```json
{
  "jsonrpc": "2.0",
  "result": [
    {
      "model_id": "qwen3.5_0.5b_q4",
      "name": "Qwen 3.5 0.5B Q4",
      "serving": true,
      "load": {
        "active_requests": 2,
        "max_concurrent": 4,
        "utilization_percent": 50,
        "load_level": "busy"
      }
    }
  ],
  "id": 1
}
```

Load levels: `idle` (0%), `available` (1-50%), `busy` (51-80%), `near_capacity` (81-99%), `at_capacity` (100%).

### Chat Completion

Send a chat completion request to a served AI model on the network.

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_chat",
    "params": {
      "model": "<model_id_or_instance_id>",
      "message": "Explain zero-knowledge proofs in one paragraph.",
      "temperature": 0.7,
      "max_tokens": 512
    },
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "model": "<model_id>",
    "response": "Zero-knowledge proofs are...",
    "tokens_used": 87,
    "finish_reason": "stop",
    "load": {
      "active_requests": 1,
      "max_concurrent": 4,
      "utilization_percent": 25,
      "load_level": "available"
    }
  },
  "id": 1
}
```

The `load` field shows the model's current load after processing your request. Load levels: `idle` (0%), `available` (1-50%), `busy` (51-80%), `near_capacity` (81-99%), `at_capacity` (100%).

Use `tenzro_listModels` or `tenzro_listModelEndpoints` to discover available models before calling `tenzro_chat`.

### List Model Endpoints

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_listModelEndpoints",
    "params": {},
    "id": 1
  }'
```

Returns all running model service endpoints with their API URLs, MCP URLs, model details, and status.

**Response includes load information for each serving model:**
```json
{
  "jsonrpc": "2.0",
  "result": [
    {
      "instance_id": "<uuid>",
      "model_id": "qwen3.5_0.5b_q4",
      "api_url": "http://127.0.0.1:8000/v1/chat/completions",
      "mcp_url": "http://127.0.0.1:8001/mcp",
      "status": "running",
      "load": {
        "active_requests": 0,
        "max_concurrent": 4,
        "utilization_percent": 0,
        "load_level": "idle"
      }
    }
  ],
  "id": 1
}
```

Load levels: `idle` (0%), `available` (1-50%), `busy` (51-80%), `near_capacity` (81-99%), `at_capacity` (100%).

---

## Cross-Chain Bridge

### Bridge Tokens

Bridge tokens between Tenzro, Ethereum, Solana, and Base via LayerZero, Chainlink CCIP, or deBridge.

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_bridgeTokens",
    "params": {
      "source_chain": "tenzro",
      "dest_chain": "ethereum",
      "asset": "TNZO",
      "amount": 1000000000000000000,
      "sender": "0x<sender_address>",
      "recipient": "0x<recipient_address>"
    },
    "id": 1
  }'
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "transfer_id": "<uuid>",
    "source_tx_hash": "0x<hash>",
    "adapter": "layerzero",
    "status": "pending",
    "estimated_time_secs": 300,
    "fee": "0.001 TNZO"
  },
  "id": 1
}
```

### Get Bridge Routes

> **Note:** This is available as an MCP tool (`get_bridge_routes`) on the MCP server at `https://mcp.tenzro.network/mcp`, not as a JSON-RPC method.

Returns available bridge routes between two chains, including estimated fees, time, and which adapter handles the route.

### List Bridge Adapters

> **Note:** This is available as an MCP tool (`list_bridge_adapters`) on the MCP server at `https://mcp.tenzro.network/mcp`, not as a JSON-RPC method.

Returns all registered bridge adapters: LayerZero, Chainlink CCIP, deBridge, Canton.

---

## Web API

### Node Status

```bash
curl https://api.tenzro.network/api/status
```

**Response:**
```json
{
  "node_state": "running",
  "role": "Validator",
  "health": "Healthy",
  "block_height": 0,
  "peer_count": 0,
  "uptime_secs": 3600
}
```

### Health Check

```bash
curl https://api.tenzro.network/api/health
```

### Request Testnet Tokens

Request 100 TNZO from the faucet (rate-limited to one request per address every 24 hours).

```bash
curl -X POST https://api.tenzro.network/api/faucet \
  -H "Content-Type: application/json" \
  -d '{"address": "0x<your_address>"}'
```

**Response:**
```json
{
  "success": true,
  "tx_hash": "0x<hash>",
  "amount": "100 TNZO",
  "message": "Tokens dispensed successfully"
}
```

### Verify ZK Proof

```bash
curl -X POST https://api.tenzro.network/api/verify/zk-proof \
  -H "Content-Type: application/json" \
  -d '{
    "proof_bytes": "<hex>",
    "public_inputs": ["<hex>"],
    "proof_type": "groth16"
  }'
```

Supported proof types: `groth16`, `plonk`, `halo2`, `stark`.

### Verify TEE Attestation

```bash
curl -X POST https://api.tenzro.network/api/verify/tee-attestation \
  -H "Content-Type: application/json" \
  -d '{
    "vendor": "intel_tdx",
    "report_data": "<hex>"
  }'
```

Supported vendors: `intel_tdx`, `amd_sev_snp`, `aws_nitro`.

### Verify Transaction Signature

```bash
curl -X POST https://api.tenzro.network/api/verify/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "tx_hash": "<hex>",
    "signature": "<hex>",
    "sender": "<hex>"
  }'
```

### Verify Settlement Receipt

```bash
curl -X POST https://api.tenzro.network/api/verify/settlement \
  -H "Content-Type: application/json" \
  -d '{
    "receipt_id": "<id>",
    "payer": "<address>",
    "payee": "<address>",
    "amount": "1000000",
    "asset": "TNZO"
  }'
```

### Verify Inference Result

```bash
curl -X POST https://api.tenzro.network/api/verify/inference \
  -H "Content-Type: application/json" \
  -d '{
    "model_id": "<model>",
    "input_hash": "<hex>",
    "output_hash": "<hex>",
    "provider": "<address>"
  }'
```

---

## Task Marketplace

The decentralized AI task marketplace lets agents and users post tasks for fulfillment, with TNZO escrow-based payment.

### Post a Task

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_postTask",
    "params": {
      "title": "Review this Rust code",
      "description": "Please review the following Rust code for correctness and safety issues...",
      "task_type": "code_review",
      "max_price": "50000000000000000000",
      "input": "fn main() { ... }",
      "priority": "normal"
    },
    "id": 1
  }'
```

**Task types:** `inference`, `code_review`, `data_analysis`, `content_generation`, `agent_execution`, `translation`, `research`, `custom:<name>`

**Response:**
```json
{
  "result": {
    "task_id": "uuid-...",
    "status": "open",
    "poster": "0x...",
    "max_price": "50000000000000000000",
    "created_at": 1234567890
  }
}
```

### List Tasks

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_listTasks",
    "params": {
      "status": "open",
      "task_type": "inference",
      "max_price": "100000000000000000000",
      "limit": 20,
      "offset": 0
    },
    "id": 1
  }'
```

### Get Task

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_getTask",
    "params": {"task_id": "uuid-..."},
    "id": 1
  }'
```

### Cancel Task

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_cancelTask",
    "params": {"task_id": "uuid-..."},
    "id": 1
  }'
```

### Submit a Quote

Providers submit quotes to fulfill a task.

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_submitQuote",
    "params": {
      "task_id": "uuid-...",
      "price": "40000000000000000000",
      "model_id": "gemma3-270m",
      "estimated_duration_secs": 30,
      "confidence": 95,
      "notes": "Can complete this in ~30 seconds"
    },
    "id": 1
  }'
```

---

## Agent Template Marketplace

The decentralized agent marketplace lets providers publish reusable AI agent templates for discovery, download, and deployment.

### List Agent Templates

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_listAgentTemplates",
    "params": {
      "free_only": true,
      "limit": 20,
      "offset": 0
    },
    "id": 1
  }'
```

**Filter options:** `template_type` (`autonomous`, `tool_agent`, `orchestrator`, `specialist`, `multi_modal`), `creator`, `tag`, `free_only`, `status`

### Register an Agent Template

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_registerAgentTemplate",
    "params": {
      "name": "Rust Code Reviewer",
      "description": "Reviews Rust code for safety, correctness, and idioms",
      "template_type": "specialist",
      "system_prompt": "You are an expert Rust developer. Review the provided code for...",
      "tags": ["rust", "code-review", "security"],
      "pricing": {"type": "free"}
    },
    "id": 1
  }'
```

**Pricing options:**
- `{"type": "free"}` — Free to use
- `{"type": "per_execution", "price": "1000000000000000000"}` — Fixed price per run
- `{"type": "per_token", "price_per_token": "1000000000"}` — Per token processed
- `{"type": "subscription", "monthly_rate": "10000000000000000000"}` — Monthly subscription

### Get Agent Template

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_getAgentTemplate",
    "params": {"template_id": "uuid-..."},
    "id": 1
  }'
```

---

## Agent Spawning & Swarm Orchestration

Tenzro agents can autonomously spawn child agents, form swarms, and run agentic execution loops with built-in LLM tool-calling.

### Register an Agent

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_registerAgent",
    "params": {
      "name": "orchestrator-1",
      "creator": "0x<address>",
      "capabilities": ["nlp", "code", "data"]
    },
    "id": 1
  }'
```

**Response:**
```json
{
  "result": {
    "agent_id": "<uuid>",
    "wallet_address": "0x<hex>",
    "status": "active"
  }
}
```

### Spawn a Child Agent

Spawn a sub-agent under a parent (max 50 children per parent):

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_spawnAgent",
    "params": [{
      "parent_id": "<parent-agent-uuid>",
      "name": "data-analyst",
      "capabilities": ["data", "nlp"]
    }],
    "id": 1
  }'
```

**Response:**
```json
{
  "result": {
    "agent_id": "<child-uuid>",
    "parent_id": "<parent-uuid>",
    "name": "data-analyst"
  }
}
```

### Run an Agentic Task Loop

The agent calls an LLM with built-in tools (`spawn_agent`, `delegate_task`, `collect_results`, `complete`) and executes them iteratively until the task is complete or the step limit is reached:

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_runAgentTask",
    "params": [{
      "agent_id": "<agent-uuid>",
      "task": "Analyze the latest network stats and summarize key metrics",
      "inference_url": "http://localhost:8080/v1/chat/completions"
    }],
    "id": 1
  }'
```

**Response:**
```json
{
  "result": {
    "agent_id": "<uuid>",
    "result": "Network stats summary: ..."
  }
}
```

### Create a Swarm

Create a pool of coordinated agents under an orchestrator:

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_createSwarm",
    "params": [{
      "orchestrator_id": "<orchestrator-uuid>",
      "members": [
        {"name": "researcher", "capabilities": ["nlp", "data"]},
        {"name": "coder", "capabilities": ["code"]},
        {"name": "reviewer", "capabilities": ["code", "nlp"]}
      ],
      "max_members": 10,
      "task_timeout_secs": 300,
      "parallel": true
    }],
    "id": 1
  }'
```

**Response:**
```json
{
  "result": {
    "swarm_id": "<swarm-uuid>",
    "orchestrator_id": "<orchestrator-uuid>"
  }
}
```

### Get Swarm Status

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_getSwarmStatus",
    "params": [{"swarm_id": "<swarm-uuid>"}],
    "id": 1
  }'
```

**Response:**
```json
{
  "result": {
    "swarm_id": "<uuid>",
    "orchestrator_id": "<uuid>",
    "status": "idle",
    "member_count": 3,
    "members": [
      {"agent_id": "<uuid>", "role": "researcher", "status": "Idle", "result": null},
      {"agent_id": "<uuid>", "role": "coder", "status": "Working", "result": null}
    ]
  }
}
```

Swarm lifecycle statuses: `idle`, `working`, `completed`. Member statuses: `Idle`, `Working`, `Completed`, `Failed`.

### Terminate a Swarm

```bash
curl -X POST https://rpc.tenzro.network \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tenzro_terminateSwarm",
    "params": [{"swarm_id": "<swarm-uuid>"}],
    "id": 1
  }'
```

**Response:**
```json
{
  "result": {
    "swarm_id": "<uuid>",
    "status": "terminated"
  }
}
```

---

## Common Workflows

### 0. Join as MicroNode (one-step setup)

The fastest way to get started on the Tenzro Network — no prior setup required:

1. Call `tenzro_joinAsMicroNode` with a display name
2. Receive a TDIP DID, MPC wallet address, 10 network capabilities, and chain ID
3. Optionally call `POST /api/faucet` to get 100 testnet TNZO
4. Start using all network features immediately

```python
from tools.tenzro_rpc import join_as_micro_node
result = join_as_micro_node("Alice")
# Returns: identity (DID), wallet (address), capabilities (10), network endpoints
```

CLI equivalent:
```bash
python tenzro_rpc.py join_network "Alice"
```

Falls back to `tenzro_participate` on older nodes.

---

### 1. Create wallet and get testnet tokens

1. Call `tenzro_createAccount` to get an address and keypair
2. Call `POST /api/faucet` with the address to get 100 TNZO
3. Call `tenzro_getBalance` to confirm the balance

### 2. Register identity and send payment

1. Call `tenzro_registerIdentity` with a display name
2. Call `tenzro_createAccount` for a keypair
3. Call `POST /api/faucet` for testnet tokens
4. Call `eth_sendRawTransaction` to send TNZO

### 3. Create agent with delegation scope

1. Register a human identity: `tenzro_registerIdentity` with `identity_type: "human"`
2. Register a machine identity: `tenzro_registerIdentity` with `identity_type: "machine"` and `controller_did`
3. Set delegation scope: `tenzro_setDelegationScope` with spending limits, allowed operations, protocols, and chains
4. Resolve the machine DID to verify: `tenzro_resolveIdentity`

### 4. Pay for a resource with x402

1. Create a payment challenge: `tenzro_createPaymentChallenge` with protocol `x402`, resource, amount, asset, and recipient
2. Sign the challenge and submit: `tenzro_verifyPayment` with challenge_id, signature, and payer info
3. Receive the receipt confirming settlement

### 5. Run AI inference

1. List available models: `tenzro_listModels` (optionally filter by category)
2. List endpoints: `tenzro_listModelEndpoints` to find running model services
3. Send a request: `tenzro_chat` with model ID and message

### 6. Bridge tokens cross-chain

1. Check available routes via MCP `get_bridge_routes` tool with source and destination chains
2. List adapters via MCP `list_bridge_adapters` tool to see available bridge providers
3. Execute bridge: `tenzro_bridgeTokens` with chain pair, asset, amount, sender, and recipient

### 7. Verify a proof

1. Call `POST /api/verify/zk-proof` with proof data
2. Check `valid` field in the response

### 8. Post a task and get it fulfilled

1. Call `tenzro_postTask` with title, description, task type, max price, and input
2. Check task status via `tenzro_getTask` — status starts as `open`
3. Providers submit quotes via `tenzro_submitQuote`; task transitions to `assigned` when accepted
4. Track completion via `tenzro_getTask` — status becomes `completed` with output populated
5. Cancel if needed via `tenzro_cancelTask` (only while `open` or `assigned`)

### 9. Publish and discover agent templates

1. Register an agent template: `tenzro_registerAgentTemplate` with name, description, template type, system prompt, and pricing
2. Browse available templates: `tenzro_listAgentTemplates` with optional filters (free_only, template_type, tag)
3. Get template details: `tenzro_getAgentTemplate` to retrieve the full template including system prompt and capabilities
4. Deploy a template: use the `system_prompt` field from the template as the AI agent's system instructions

---

## Error Handling

JSON-RPC errors follow standard format:
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found"
  },
  "id": 1
}
```

Common error codes:
- `-32700` — Parse error (invalid JSON)
- `-32600` — Invalid request
- `-32601` — Method not found
- `-32602` — Invalid params
- `-32603` — Internal error

Web API errors return HTTP status codes with JSON body:
```json
{
  "error": "description of error"
}
```

Faucet rate-limit errors return HTTP 429 with a `message` field indicating cooldown time.

---

## MCP Integration

If the Tenzro node has MCP enabled (port 3001), you can use the Model Context Protocol for richer tool-based integration. The MCP server exposes tools across 10 categories:

**Wallet & Ledger:**
- `get_balance` — Query TNZO balance by address
- `create_wallet` — Generate new Ed25519 or Secp256k1 keypair
- `send_transaction` — Send a TNZO transfer
- `request_faucet` — Request testnet tokens (100 TNZO, 24h cooldown)
- `get_block` — Get block by height from storage
- `get_transaction` — Look up transaction by hash
- `get_node_status` — Node health, block height, peer count, uptime

**Identity & Delegation:**
- `register_identity` — Register human or machine DID via TDIP
- `resolve_did` — Resolve DID to identity info, delegation scope
- `set_delegation_scope` — Set spending limits, allowed operations/protocols/chains for machine identities

**Payments:**
- `create_payment_challenge` — Create payment challenge (MPP, x402, or native)
- `verify_payment` — Verify payment credential and settle on-chain
- `list_payment_protocols` — List supported payment protocols and their features

**AI Models & Inference:**
- `list_models` — List available AI models, filter by category or name
- `chat_completion` — Send chat completion to a served model
- `list_model_endpoints` — List running model service endpoints with URLs and status

**Cross-Chain Bridge:**
- `bridge_tokens` — Bridge tokens between Tenzro, Ethereum, Solana, Base
- `get_bridge_routes` — Get available routes between two chains with fees
- `list_bridge_adapters` — List registered adapters (LayerZero, Chainlink CCIP, deBridge, Canton)

**Verification:**
- `verify_zk_proof` — Verify Groth16, PlonK, or STARK proof with public inputs

**Staking & Providers:**
- `stake_tokens` — Stake TNZO tokens as Validator, ModelProvider, or TeeProvider
- `unstake_tokens` — Unstake TNZO tokens (initiates unbonding period)
- `register_provider` — Register as a provider with optional staking
- `get_provider_stats` — Get provider statistics: served models, inferences, staking totals

**Task Marketplace:**
- `post_task` — Post a task to the decentralized AI task marketplace with TNZO escrow payment
- `list_tasks` — List marketplace tasks with optional filters (status, type, max_price, limit, offset)
- `get_task` — Get full details of a specific task by ID
- `cancel_task` — Cancel an open task posted by the caller
- `submit_quote` — Submit a fulfillment quote for an open task (price, model, estimated duration)

**Agent Marketplace:**
- `list_agent_templates` — Browse reusable AI agent templates, filter by type/tags/pricing/status
- `register_agent_template` — Publish a new agent template to the marketplace with pricing model
- `get_agent_template` — Get full details of an agent template by ID

Connect to MCP at `https://mcp.tenzro.network/mcp` using Streamable HTTP transport.
