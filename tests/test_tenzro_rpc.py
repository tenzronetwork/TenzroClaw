"""Tests for TenzroClaw RPC helper functions."""

import json
import sys
import pytest
from unittest.mock import patch, MagicMock

import requests

import tools.tenzro_rpc as rpc


# ── Wallet & Balance ─────────────────────────────────────────────────


class TestCreateWallet:
    def test_create_wallet_returns_keypair(self, mock_rpc_response):
        expected = {
            "address": "0xabc123",
            "public_key": "0xpub456",
            "key_type": "ed25519",
        }
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(expected)):
            result = rpc.create_wallet()
        assert result["address"] == "0xabc123"
        assert result["public_key"] == "0xpub456"
        assert result["key_type"] == "ed25519"

    def test_create_wallet_custom_key_type(self, mock_rpc_response):
        expected = {"address": "0xdef", "public_key": "0xpub", "key_type": "secp256k1"}
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(expected)):
            result = rpc.create_wallet("secp256k1")
        assert result["key_type"] == "secp256k1"


class TestGetBalance:
    def test_get_balance_hex_to_decimal(self, mock_rpc_response):
        """Verify hex wei string is converted to decimal TNZO."""
        hex_balance = "0xde0b6b3a7640000"  # 1e18 wei = 1 TNZO
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(hex_balance)):
            result = rpc.get_balance("0xaddr1")
        assert result["address"] == "0xaddr1"
        assert result["balance_wei"] == hex_balance
        assert result["balance_tnzo"] == "1.000000"

    def test_get_balance_zero(self, mock_rpc_response):
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response("0x0")):
            result = rpc.get_balance("0xaddr2")
        assert result["balance_tnzo"] == "0.000000"

    def test_get_balance_dict_result(self, mock_rpc_response):
        """When RPC returns a dict instead of hex string, pass through."""
        expected = {"address": "0xaddr3", "balance": "100"}
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(expected)):
            result = rpc.get_balance("0xaddr3")
        assert result == expected


# ── Node Status ──────────────────────────────────────────────────────


class TestGetStatus:
    def test_get_status_fields(self, mock_api_response):
        status_data = {
            "status": "healthy",
            "block_height": 12345,
            "peers": 42,
            "uptime": "3d 12h",
            "version": "0.9.0",
        }
        with patch("tools.tenzro_rpc.requests.get", return_value=mock_api_response(status_data)):
            result = rpc.get_status()
        assert result["status"] == "healthy"
        assert result["block_height"] == 12345
        assert result["peers"] == 42
        assert "uptime" in result


# ── Identity ─────────────────────────────────────────────────────────


class TestRegisterIdentity:
    def test_register_identity_did_format(self, mock_rpc_response):
        expected = {
            "did": "did:tenzro:human:abc123",
            "display_name": "Alice",
        }
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(expected)):
            result = rpc.register_identity("Alice")
        assert result["did"].startswith("did:tenzro:")
        assert result["display_name"] == "Alice"

    def test_register_identity_with_public_key(self, mock_rpc_response):
        expected = {
            "did": "did:tenzro:human:def456",
            "display_name": "Bob",
            "public_key": "0xpubkey",
        }
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(expected)):
            result = rpc.register_identity("Bob", public_key="0xpubkey")
        assert result["did"].startswith("did:tenzro:")


# ── Transactions ─────────────────────────────────────────────────────


class TestSendTransaction:
    def test_send_transaction_returns_hash(self, mock_rpc_response):
        tx_hash = "0xtxhash789abc"
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(tx_hash)):
            result = rpc.send_transaction("0xfrom", "0xto", 1000000000000000000)
        assert result == tx_hash


# ── Models ───────────────────────────────────────────────────────────


class TestListModels:
    def test_list_models_returns_list(self, mock_rpc_response):
        models = [
            {"id": "gemma3-270m", "name": "Gemma 3 270M", "status": "available"},
            {"id": "llama-7b", "name": "Llama 7B", "status": "available"},
        ]
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(models)):
            result = rpc.list_models()
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == "gemma3-270m"


class TestChat:
    def test_chat_response_format(self, mock_rpc_response):
        expected = {
            "model": "gemma3-270m",
            "response": "Tenzro is a decentralized AI network.",
            "tokens_used": 42,
        }
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(expected)):
            result = rpc.chat("gemma3-270m", "What is Tenzro?")
        assert result["model"] == "gemma3-270m"
        assert "response" in result
        assert "tokens_used" in result


# ── Bridge ───────────────────────────────────────────────────────────


class TestBridgeTokens:
    def test_bridge_tokens_result(self, mock_rpc_response):
        expected = {
            "bridge_id": "br_12345",
            "status": "pending",
            "source_chain": "tenzro",
            "destination_chain": "ethereum",
            "amount": 1000000000000000000,
        }
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(expected)):
            result = rpc.bridge_tokens(
                "tenzro", "ethereum", "TNZO",
                1000000000000000000, "0xsender", "0xrecipient",
            )
        assert result["bridge_id"] == "br_12345"
        assert result["status"] == "pending"
        assert result["source_chain"] == "tenzro"
        assert result["destination_chain"] == "ethereum"


# ── Payments ─────────────────────────────────────────────────────────


class TestCreatePaymentChallenge:
    def test_create_payment_challenge_format(self, mock_rpc_response):
        expected = {
            "challenge_id": "ch_abc123",
            "protocol": "x402",
            "resource": "/api/inference",
            "amount": 100,
            "asset": "USDC",
            "expires_at": "2026-04-04T00:00:00Z",
        }
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_rpc_response(expected)):
            result = rpc.create_payment_challenge(
                "x402", "/api/inference", 100, "USDC", "0xrecipient",
            )
        assert result["challenge_id"].startswith("ch_")
        assert result["protocol"] == "x402"
        assert result["resource"] == "/api/inference"
        assert result["amount"] == 100


# ── Error Handling ───────────────────────────────────────────────────


class TestErrorHandling:
    def test_rpc_timeout(self):
        """RPC call that times out raises ConnectionError."""
        with patch(
            "tools.tenzro_rpc.requests.post",
            side_effect=requests.exceptions.ConnectTimeout("Connection timed out"),
        ):
            with pytest.raises(requests.exceptions.ConnectTimeout):
                rpc.create_wallet()

    def test_api_500_error(self):
        """API returning 500 raises HTTPError."""
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "500 Server Error"
        )
        with patch("tools.tenzro_rpc.requests.get", return_value=mock_resp):
            with pytest.raises(requests.exceptions.HTTPError):
                rpc.get_status()

    def test_invalid_json_response(self):
        """RPC returning invalid JSON raises ValueError."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        with patch("tools.tenzro_rpc.requests.post", return_value=mock_resp):
            with pytest.raises(json.JSONDecodeError):
                rpc.create_wallet()

    def test_rpc_error_response(self, mock_rpc_error):
        """RPC returning an error object propagates it."""
        with patch(
            "tools.tenzro_rpc.requests.post",
            return_value=mock_rpc_error("Method not found"),
        ):
            result = rpc.create_wallet()
        assert "error" in result
        assert result["error"]["message"] == "Method not found"

    def test_connection_refused(self):
        """RPC connection refused raises ConnectionError."""
        with patch(
            "tools.tenzro_rpc.requests.post",
            side_effect=requests.exceptions.ConnectionError("Connection refused"),
        ):
            with pytest.raises(requests.exceptions.ConnectionError):
                rpc.get_balance("0xaddr")


# ── CLI Argument Parsing ─────────────────────────────────────────────


class TestCLI:
    def test_unknown_command(self, capsys):
        """Unknown command prints error and exits with code 1."""
        with patch.object(sys, "argv", ["tenzro_rpc.py", "nonexistent_cmd"]):
            with pytest.raises(SystemExit) as exc_info:
                rpc.main()
            assert exc_info.value.code == 1
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "error" in output
        assert "Unknown command" in output["error"]

    def test_help_flag(self, capsys):
        """--help flag prints usage and exits with code 0."""
        with patch.object(sys, "argv", ["tenzro_rpc.py", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                rpc.main()
            assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Available commands" in captured.out

    def test_create_wallet_dispatch(self, mock_rpc_response):
        """CLI dispatches create_wallet correctly."""
        expected = {"address": "0xnew", "public_key": "0xpk", "key_type": "ed25519"}
        with patch.object(sys, "argv", ["tenzro_rpc.py", "create_wallet"]):
            with patch(
                "tools.tenzro_rpc.requests.post",
                return_value=mock_rpc_response(expected),
            ):
                rpc.main()

    def test_status_dispatch(self, mock_api_response, capsys):
        """CLI dispatches status correctly."""
        status = {"status": "healthy", "block_height": 100}
        with patch.object(sys, "argv", ["tenzro_rpc.py", "status"]):
            with patch(
                "tools.tenzro_rpc.requests.get",
                return_value=mock_api_response(status),
            ):
                rpc.main()
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["status"] == "healthy"

    def test_missing_args(self, capsys):
        """Command with missing required args exits with code 1."""
        with patch.object(sys, "argv", ["tenzro_rpc.py", "get_balance"]):
            with pytest.raises(SystemExit) as exc_info:
                rpc.main()
            assert exc_info.value.code == 1
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "Missing arguments" in output["error"]

    def test_connection_error_cli(self, capsys):
        """CLI handles connection errors gracefully."""
        with patch.object(sys, "argv", ["tenzro_rpc.py", "status"]):
            with patch(
                "tools.tenzro_rpc.requests.get",
                side_effect=requests.exceptions.ConnectionError("refused"),
            ):
                with pytest.raises(SystemExit) as exc_info:
                    rpc.main()
                assert exc_info.value.code == 1
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert "Cannot connect" in output["error"]
