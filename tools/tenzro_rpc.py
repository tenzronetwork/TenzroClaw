#!/usr/bin/env python3
"""TenzroClaw — Tenzro blockchain RPC helper.

Part of the TenzroClaw OpenClaw skill for interacting with the Tenzro Network.
Wraps Tenzro JSON-RPC and Web API calls into simple functions.

Requires: pip install requests

Usage:
    python tenzro_rpc.py join_network "Alice"
    python tenzro_rpc.py get_balance 0x1234...
    python tenzro_rpc.py create_wallet
    python tenzro_rpc.py faucet 0x1234...
    python tenzro_rpc.py send 0xfrom 0xto 1000000000000000000
    python tenzro_rpc.py status
    python tenzro_rpc.py register_identity "Alice"
    python tenzro_rpc.py resolve_did "did:tenzro:human:..."
    python tenzro_rpc.py block_height
    python tenzro_rpc.py get_block 0
    python tenzro_rpc.py chain_id
    python tenzro_rpc.py chat gemma3-270m "What is Tenzro?"
    python tenzro_rpc.py list_model_endpoints
    python tenzro_rpc.py create_payment x402 /api/inference 100 USDC 0xrecipient
    python tenzro_rpc.py verify_payment <challenge_id> x402 <payer_did> 0xpayer 100 USDC 0xsig
    python tenzro_rpc.py set_delegation did:tenzro:machine:... 10000000 100000000
    python tenzro_rpc.py post_task "Review code" "Review this Rust code" code_review 50000000000000000000
    python tenzro_rpc.py list_tasks
    python tenzro_rpc.py get_task <task_id>
    python tenzro_rpc.py cancel_task <task_id>
    python tenzro_rpc.py submit_quote <task_id> 40000000000000000000 gemma3-270m 30
    python tenzro_rpc.py list_agent_templates
    python tenzro_rpc.py register_agent_template "Code Reviewer" "Reviews code" specialist "You are..."
    python tenzro_rpc.py get_agent_template <template_id>
    python tenzro_rpc.py register_agent "my-agent" 0xaddress nlp,code
    python tenzro_rpc.py spawn_agent <parent_id> "sub-agent" data,nlp
    python tenzro_rpc.py run_agent_task <agent_id> "Summarize network stats"
    python tenzro_rpc.py create_swarm <orchestrator_id> researcher:nlp,data coder:code
    python tenzro_rpc.py get_swarm_status <swarm_id>
    python tenzro_rpc.py terminate_swarm <swarm_id>
    python tenzro_rpc.py bridge_tokens tenzro ethereum TNZO 1000000000000000000 0xsender 0xrecipient
    python tenzro_rpc.py stake 1000000000000000000 Validator
    python tenzro_rpc.py unstake 1000000000000000000
    python tenzro_rpc.py register_provider model-provider
    python tenzro_rpc.py provider_stats
"""

import json
import sys
from typing import Any

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests library required: pip install requests"}))
    sys.exit(1)

# Default endpoints — override with environment variables
import os

RPC_URL = os.environ.get("TENZRO_RPC_URL", "https://rpc.tenzro.network")
API_URL = os.environ.get("TENZRO_API_URL", "https://api.tenzro.network")

_request_id = 0


def _rpc(method: str, params: Any = None) -> dict:
    """Send a JSON-RPC 2.0 request to Tenzro."""
    global _request_id
    _request_id += 1
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params if params is not None else {},
        "id": _request_id,
    }
    resp = requests.post(RPC_URL, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        return {"error": data["error"]}
    return data.get("result", {})


def _api_get(path: str) -> dict:
    """GET request to Web API."""
    resp = requests.get(f"{API_URL}{path}", timeout=30)
    resp.raise_for_status()
    return resp.json()


def _api_post(path: str, body: dict) -> dict:
    """POST request to Web API."""
    resp = requests.post(f"{API_URL}{path}", json=body, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ── Wallet & Balance ──────────────────────────────────────────────


def create_wallet(key_type: str = "ed25519") -> dict:
    """Generate a new keypair and address."""
    return _rpc("tenzro_createAccount", {"key_type": key_type})


def create_mpc_wallet() -> dict:
    """Generate a new 2-of-3 MPC threshold wallet."""
    return _rpc("tenzro_createWallet")


def get_balance(address: str) -> dict:
    """Get TNZO balance for an address (returns hex wei)."""
    result = _rpc("tenzro_getBalance", {"address": address})
    if isinstance(result, str):
        wei = int(result, 16)
        tnzo = wei / 1e18
        return {"address": address, "balance_wei": result, "balance_tnzo": f"{tnzo:.6f}"}
    return result


def send_transaction(from_addr: str, to_addr: str, value: int,
                     gas_limit: int = 21000, gas_price: int = 1_000_000_000,
                     nonce: int = 0) -> dict:
    """Send a TNZO transfer transaction."""
    return _rpc("eth_sendRawTransaction", {
        "from": from_addr,
        "to": to_addr,
        "value": value,
        "gas_limit": gas_limit,
        "gas_price": gas_price,
        "nonce": nonce,
    })


# ── Faucet ────────────────────────────────────────────────────────


def request_faucet(address: str) -> dict:
    """Request testnet TNZO from the faucet (100 TNZO, 24h cooldown)."""
    return _api_post("/api/faucet", {"address": address})


# ── Node Status ───────────────────────────────────────────────────


def get_status() -> dict:
    """Get node status (health, block height, peers, uptime)."""
    return _api_get("/api/status")


def get_health() -> dict:
    """Health check."""
    return _api_get("/api/health")


def block_height() -> dict:
    """Get the current block height."""
    result = _rpc("tenzro_blockNumber")
    if isinstance(result, str):
        return {"block_height": int(result, 16), "hex": result}
    return result


def get_block(height: int) -> dict:
    """Get a block by height."""
    return _rpc("tenzro_getBlock", {"height": height})


def chain_id() -> dict:
    """Get the chain ID."""
    result = _rpc("eth_chainId")
    if isinstance(result, str):
        return {"chain_id": int(result, 16), "hex": result}
    return result


def node_info() -> dict:
    """Get full node info via RPC."""
    return _rpc("tenzro_nodeInfo")


# ── Identity ──────────────────────────────────────────────────────


def register_identity(display_name: str, public_key: str = None,
                      key_type: str = "ed25519") -> dict:
    """Register a human identity and get a DID."""
    params = {"display_name": display_name}
    if public_key:
        params["public_key"] = public_key
        params["key_type"] = key_type
    return _rpc("tenzro_registerIdentity", params)


def resolve_did(did: str) -> dict:
    """Resolve a DID to identity information."""
    return _rpc("tenzro_resolveIdentity", {"did": did})


def resolve_did_document(did: str) -> dict:
    """Resolve a DID to a W3C DID Document."""
    return _rpc("tenzro_resolveDidDocument", {"did": did})


def join_as_micro_node(display_name: str = "Tenzro User",
                       origin: str = "cli",
                       participant_type: str = "human") -> dict:
    """Join the Tenzro Network as a MicroNode participant.

    Zero-install — auto-provisions a TDIP DID and MPC wallet.
    Returns full identity, wallet, capabilities, network endpoints, and chain ID.
    Falls back to tenzro_participate for older nodes.
    """
    params = {
        "display_name": display_name.lstrip("@"),
        "origin": origin,
        "participant_type": participant_type,
    }
    result = _rpc("tenzro_joinAsMicroNode", params)
    if "error" in result:
        # Fall back to legacy tenzro_participate
        result = _rpc("tenzro_participate", {"display_name": display_name.lstrip("@")})
    return result


# ── Verification ──────────────────────────────────────────────────


def verify_zk_proof(proof_bytes: str, public_inputs: list,
                    proof_type: str = "groth16") -> dict:
    """Verify a ZK proof via Web API."""
    return _api_post("/api/verify/zk-proof", {
        "proof_bytes": proof_bytes,
        "public_inputs": public_inputs,
        "proof_type": proof_type,
    })


def verify_tee_attestation(vendor: str, report_data: str,
                           measurement: str = None) -> dict:
    """Verify a TEE attestation via Web API."""
    body = {"vendor": vendor, "report_data": report_data}
    if measurement:
        body["measurement"] = measurement
    return _api_post("/api/verify/tee-attestation", body)


# ── Token ─────────────────────────────────────────────────────────


def total_supply() -> dict:
    """Get total TNZO token supply."""
    return _rpc("tenzro_totalSupply")


def token_balance(address: str) -> dict:
    """Get TNZO token balance for an address."""
    return _rpc("tenzro_tokenBalance", {"address": address})


# ── Models ────────────────────────────────────────────────────────


def list_models() -> dict:
    """List registered AI models."""
    return _rpc("tenzro_listModels")


def chat(model: str, message: str, temperature: float = 0.7,
         max_tokens: int = 512) -> dict:
    """Send a chat completion request to a served AI model."""
    return _rpc("tenzro_chat", {
        "model_id": model,
        "message": message,
        "temperature": temperature,
        "max_tokens": max_tokens,
    })


def list_model_endpoints() -> dict:
    """List running model service endpoints."""
    return _rpc("tenzro_listModelEndpoints")


# ── Payments ──────────────────────────────────────────────────────


def create_payment_challenge(protocol: str, resource: str, amount: int,
                             asset: str = "TNZO",
                             recipient: str = None) -> dict:
    """Create a payment challenge (MPP, x402, or native).

    protocol: mpp | x402 | native
    resource: the resource path being paid for (e.g. /api/inference)
    amount: payment amount in smallest unit
    asset: TNZO, USDC, etc.
    recipient: payee address (required for x402/native)
    """
    params = {
        "protocol": protocol,
        "resource": resource,
        "amount": amount,
        "asset": asset,
    }
    if recipient:
        params["recipient"] = recipient
    return _rpc("tenzro_createPaymentChallenge", params)


def verify_payment(challenge_id: str, protocol: str, payer_did: str,
                   payer_address: str, amount: int, asset: str,
                   signature: str) -> dict:
    """Verify a payment credential and settle on-chain."""
    return _rpc("tenzro_verifyPayment", {
        "challenge_id": challenge_id,
        "protocol": protocol,
        "payer_did": payer_did,
        "payer_address": payer_address,
        "amount": amount,
        "asset": asset,
        "signature": signature,
    })


# ── Delegation ───────────────────────────────────────────────────


def set_delegation_scope(machine_did: str, max_transaction_value: int,
                         max_daily_spend: int,
                         allowed_operations: list = None,
                         allowed_chains: list = None) -> dict:
    """Set delegation scope for a machine DID."""
    params = {
        "machine_did": machine_did,
        "max_transaction_value": max_transaction_value,
        "max_daily_spend": max_daily_spend,
    }
    if allowed_operations:
        params["allowed_operations"] = allowed_operations
    if allowed_chains:
        params["allowed_chains"] = allowed_chains
    return _rpc("tenzro_setDelegationScope", params)


# ── Task Marketplace ─────────────────────────────────────────────


def post_task(title: str, description: str, task_type: str,
              budget_wei: int, required_capabilities: list = None) -> dict:
    """Post a task to the decentralized AI task marketplace.

    task_type: inference | code_review | data_analysis | content_generation |
               agent_execution | translation | research | custom:<name>
    budget_wei: maximum budget in wei
    """
    params = {
        "title": title,
        "description": description,
        "task_type": task_type,
        "budget": budget_wei,
    }
    if required_capabilities:
        params["required_capabilities"] = required_capabilities
    return _rpc("tenzro_postTask", params)


def list_tasks(status: str = None, task_type: str = None) -> dict:
    """List tasks on the marketplace, optionally filtered."""
    params = {}
    if status:
        params["status"] = status
    if task_type:
        params["task_type"] = task_type
    return _rpc("tenzro_listTasks", params)


def get_task(task_id: str) -> dict:
    """Get details of a specific task."""
    return _rpc("tenzro_getTask", {"task_id": task_id})


def cancel_task(task_id: str) -> dict:
    """Cancel a task (poster only)."""
    return _rpc("tenzro_cancelTask", {"task_id": task_id})


def submit_quote(task_id: str, price_wei: int, model_id: str = None,
                 estimated_time_secs: int = None) -> dict:
    """Submit a quote for a task as a provider/agent."""
    params = {
        "task_id": task_id,
        "price": price_wei,
    }
    if model_id:
        params["model_id"] = model_id
    if estimated_time_secs is not None:
        params["estimated_time"] = estimated_time_secs
    return _rpc("tenzro_submitQuote", params)


# ── Agent Template Marketplace ───────────────────────────────────


def list_agent_templates(agent_type: str = None) -> dict:
    """List available agent templates.

    agent_type: autonomous | tool_agent | orchestrator | specialist | multi_modal
    """
    params = {}
    if agent_type:
        params["agent_type"] = agent_type
    return _rpc("tenzro_listAgentTemplates", params)


def register_agent_template(name: str, description: str,
                            agent_type: str,
                            system_prompt: str = None,
                            capabilities: list = None) -> dict:
    """Register a new agent template on the marketplace."""
    params = {
        "name": name,
        "description": description,
        "agent_type": agent_type,
    }
    if system_prompt:
        params["system_prompt"] = system_prompt
    if capabilities:
        params["capabilities"] = capabilities
    return _rpc("tenzro_registerAgentTemplate", params)


def get_agent_template(template_id: str) -> dict:
    """Get details of a specific agent template."""
    return _rpc("tenzro_getAgentTemplate", {"template_id": template_id})


# ── Agent Spawning & Swarm ───────────────────────────────────────


def register_agent(name: str, address: str,
                   capabilities: list = None) -> dict:
    """Register a new AI agent with identity and wallet."""
    params = {
        "name": name,
        "address": address,
    }
    if capabilities:
        params["capabilities"] = capabilities
    return _rpc("tenzro_registerAgent", params)


def spawn_agent(parent_id: str, name: str,
                capabilities: list = None) -> dict:
    """Spawn a sub-agent from a parent agent."""
    params = {
        "parent_id": parent_id,
        "name": name,
    }
    if capabilities:
        params["capabilities"] = capabilities
    return _rpc("tenzro_spawnAgent", params)


def run_agent_task(agent_id: str, task: str,
                   max_steps: int = 10) -> dict:
    """Run an autonomous task via the agentic execution loop."""
    return _rpc("tenzro_runAgentTask", {
        "agent_id": agent_id,
        "task": task,
        "max_steps": max_steps,
    })


def create_swarm(orchestrator_id: str,
                 members: list) -> dict:
    """Create a swarm of agents coordinated by an orchestrator.

    members: list of dicts with 'name' and 'capabilities' keys,
             or strings like 'researcher:nlp,data'
    """
    parsed = []
    for m in members:
        if isinstance(m, dict):
            parsed.append(m)
        elif isinstance(m, str) and ":" in m:
            name, caps = m.split(":", 1)
            parsed.append({
                "name": name,
                "capabilities": caps.split(","),
            })
        else:
            parsed.append({"name": str(m), "capabilities": []})
    return _rpc("tenzro_createSwarm", {
        "orchestrator_id": orchestrator_id,
        "members": parsed,
    })


def get_swarm_status(swarm_id: str) -> dict:
    """Get the status of a swarm and its members."""
    return _rpc("tenzro_getSwarmStatus", {"swarm_id": swarm_id})


def terminate_swarm(swarm_id: str) -> dict:
    """Terminate a swarm and all its member agents."""
    return _rpc("tenzro_terminateSwarm", {"swarm_id": swarm_id})


# ── Cross-Chain Bridge ───────────────────────────────────────────


def bridge_tokens(source_chain: str, dest_chain: str, asset: str,
                  amount_wei: int, sender: str,
                  recipient: str) -> dict:
    """Bridge tokens between chains.

    source_chain/dest_chain: tenzro | ethereum | solana | base
    asset: TNZO, USDC, etc.
    """
    return _rpc("tenzro_bridgeTokens", {
        "source_chain": source_chain,
        "destination_chain": dest_chain,
        "asset": asset,
        "amount": amount_wei,
        "sender": sender,
        "recipient": recipient,
    })


# ── Staking & Providers ─────────────────────────────────────────


def stake_tokens(amount_wei: int,
                 role: str = "Validator") -> dict:
    """Stake TNZO tokens.

    role: Validator | ModelProvider | TeeProvider
    """
    return _rpc("tenzro_stake", {
        "amount": amount_wei,
        "role": role,
    })


def unstake_tokens(amount_wei: int) -> dict:
    """Unstake TNZO tokens (initiates unbonding period)."""
    return _rpc("tenzro_unstake", {"amount": amount_wei})


def register_provider(provider_type: str) -> dict:
    """Register as a provider (model-provider or tee-provider)."""
    return _rpc("tenzro_registerProvider", {
        "provider_type": provider_type,
    })


def provider_stats() -> dict:
    """Get provider statistics (served models, inferences, staking)."""
    return _rpc("tenzro_providerStats")


# ── Additional Verification ──────────────────────────────────────


def verify_transaction(tx_hash: str, sender_public_key: str,
                       signature: str) -> dict:
    """Verify a transaction signature via Web API."""
    return _api_post("/api/verify/transaction", {
        "tx_hash": tx_hash,
        "sender_public_key": sender_public_key,
        "signature": signature,
    })


def verify_settlement(settlement_id: str, proof_type: str,
                      proof_data: str) -> dict:
    """Verify a settlement receipt via Web API."""
    return _api_post("/api/verify/settlement", {
        "settlement_id": settlement_id,
        "proof_type": proof_type,
        "proof_data": proof_data,
    })


def verify_inference(request_id: str, model_id: str,
                     result_hash: str) -> dict:
    """Verify an inference result via Web API."""
    return _api_post("/api/verify/inference", {
        "request_id": request_id,
        "model_id": model_id,
        "result_hash": result_hash,
    })


# ── CLI ───────────────────────────────────────────────────────────

COMMANDS = {
    # Wallet & Balance
    "join_network": lambda args: join_as_micro_node(
        args[0] if args else "Tenzro User",
        args[1] if len(args) > 1 else "cli",
    ),
    "create_wallet": lambda args: create_wallet(args[0] if args else "ed25519"),
    "create_mpc_wallet": lambda args: create_mpc_wallet(),
    "get_balance": lambda args: get_balance(args[0]),
    "balance": lambda args: get_balance(args[0]),
    "send": lambda args: send_transaction(args[0], args[1], int(args[2])),
    "faucet": lambda args: request_faucet(args[0]),
    # Node Status
    "status": lambda args: get_status(),
    "health": lambda args: get_health(),
    "block_height": lambda args: block_height(),
    "get_block": lambda args: get_block(int(args[0])),
    "chain_id": lambda args: chain_id(),
    "node_info": lambda args: node_info(),
    # Identity
    "register_identity": lambda args: register_identity(args[0]),
    "resolve_did": lambda args: resolve_did(args[0]),
    "resolve_did_document": lambda args: resolve_did_document(args[0]),
    # Verification
    "verify_zk_proof": lambda args: verify_zk_proof(args[0], args[1:]),
    "verify_transaction": lambda args: verify_transaction(args[0], args[1], args[2]),
    "verify_settlement": lambda args: verify_settlement(args[0], args[1], args[2]),
    "verify_inference": lambda args: verify_inference(args[0], args[1], args[2]),
    # Token
    "total_supply": lambda args: total_supply(),
    "token_balance": lambda args: token_balance(args[0]),
    # Models
    "list_models": lambda args: list_models(),
    "chat": lambda args: chat(args[0], " ".join(args[1:]) if len(args) > 1 else args[1]),
    "list_model_endpoints": lambda args: list_model_endpoints(),
    # Payments
    "create_payment": lambda args: create_payment_challenge(
        args[0], args[1], int(args[2]),
        args[3] if len(args) > 3 else "TNZO",
        args[4] if len(args) > 4 else None,
    ),
    "verify_payment": lambda args: verify_payment(
        args[0], args[1], args[2], args[3], int(args[4]), args[5], args[6],
    ),
    # Delegation
    "set_delegation": lambda args: set_delegation_scope(
        args[0], int(args[1]), int(args[2]),
    ),
    # Task Marketplace
    "post_task": lambda args: post_task(
        args[0], args[1], args[2], int(args[3]),
    ),
    "list_tasks": lambda args: list_tasks(
        args[0] if args else None,
        args[1] if len(args) > 1 else None,
    ),
    "get_task": lambda args: get_task(args[0]),
    "cancel_task": lambda args: cancel_task(args[0]),
    "submit_quote": lambda args: submit_quote(
        args[0], int(args[1]),
        args[2] if len(args) > 2 else None,
        int(args[3]) if len(args) > 3 else None,
    ),
    # Agent Templates
    "list_agent_templates": lambda args: list_agent_templates(
        args[0] if args else None,
    ),
    "register_agent_template": lambda args: register_agent_template(
        args[0], args[1], args[2],
        args[3] if len(args) > 3 else None,
    ),
    "get_agent_template": lambda args: get_agent_template(args[0]),
    # Agent Spawning & Swarm
    "register_agent": lambda args: register_agent(
        args[0], args[1],
        args[2].split(",") if len(args) > 2 else None,
    ),
    "spawn_agent": lambda args: spawn_agent(
        args[0], args[1],
        args[2].split(",") if len(args) > 2 else None,
    ),
    "run_agent_task": lambda args: run_agent_task(args[0], " ".join(args[1:])),
    "create_swarm": lambda args: create_swarm(args[0], args[1:]),
    "get_swarm_status": lambda args: get_swarm_status(args[0]),
    "terminate_swarm": lambda args: terminate_swarm(args[0]),
    # Bridge
    "bridge_tokens": lambda args: bridge_tokens(
        args[0], args[1], args[2], int(args[3]), args[4], args[5],
    ),
    # Staking & Providers
    "stake": lambda args: stake_tokens(
        int(args[0]), args[1] if len(args) > 1 else "Validator",
    ),
    "unstake": lambda args: unstake_tokens(int(args[0])),
    "register_provider": lambda args: register_provider(args[0]),
    "provider_stats": lambda args: provider_stats(),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        print("Available commands:")
        for cmd in sorted(COMMANDS):
            print(f"  {cmd}")
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd not in COMMANDS:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)

    try:
        result = COMMANDS[cmd](args)
        print(json.dumps(result, indent=2, default=str))
    except requests.exceptions.ConnectionError:
        print(json.dumps({"error": f"Cannot connect to Tenzro node at {RPC_URL}"}))
        sys.exit(1)
    except IndexError:
        print(json.dumps({"error": f"Missing arguments for command: {cmd}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
