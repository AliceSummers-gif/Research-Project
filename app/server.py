"""Local web app for the risk-aware refund prototype."""

import json
import sys
from dataclasses import asdict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.common.schemas import CaseInput, Member1Output, Member2Output, Member3Output
from src.agent.agent import run_agent
from src.evidence.pipeline import build_evidence_chain
from src.evidence.rules import load_adopted_rules


class RefundAppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.path = "/app/risk_aware_refund_ui.html"
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/evidence":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = run_evidence_case(payload)
            self._send_json(200, result)
        except (KeyError, TypeError, ValueError) as error:
            self._send_json(400, {"error": str(error)})
        except Exception as error:
            self._send_json(500, {"error": f"Unable to process case: {error}"})

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_evidence_case(payload):
    case_id = payload.get("case_id", "UI-DEMO-001")
    detected_product = payload.get("detected_product") or "Black Jacket"
    damage_type = payload.get("damage_type") or "hole_or_tear"
    image_usable = bool(payload.get("image_usable", True))

    case = CaseInput(
        case_id=case_id,
        order_id=payload["order_id"],
        claim_text=payload["claim_text"],
        image_paths=["browser-upload.jpg"] if payload.get("image_present", True) else [],
    )
    member1 = Member1Output(
        case_id=case_id,
        product=detected_product,
        claimed_defect=damage_type,
        claimed_location=payload.get("damage_location", "left sleeve"),
        image_quality=float(payload.get("image_quality", 0.90)),
        blur_score=0.10,
        lighting_score=0.91,
        relevant_region_visible=image_usable,
        image_usable=image_usable,
    )
    member2 = Member2Output(
        case_id=case_id,
        detected_product=detected_product,
        damage_detected=bool(payload.get("damage_detected", True)),
        damage_type=damage_type,
        damage_location=payload.get("damage_location", "left sleeve"),
        damage_confidence=float(payload.get("damage_confidence", 0.88)),
        claim_image_consistency=float(payload.get("claim_image_consistency", 0.92)),
    )
    chain = build_evidence_chain(
        case,
        member1,
        member2,
        payload.get("request_date", "2026-08-15"),
    )
    decision = run_agent(member1, member2, Member3Output(**chain.member3_output))
    return {
        "order": asdict(chain.order_evidence) if chain.order_evidence else None,
        "policy": asdict(chain.policy_evidence) if chain.policy_evidence else None,
        "adopted_rules": load_adopted_rules(),
        "evidence": chain.member3_output,
        "reason": chain.verified_evidence.reason,
        "decision": decision.model_dump(),
    }


def main():
    address = ("127.0.0.1", 8765)
    print("Risk-Aware Refund App: http://127.0.0.1:8765")
    ThreadingHTTPServer(address, RefundAppHandler).serve_forever()


if __name__ == "__main__":
    main()
