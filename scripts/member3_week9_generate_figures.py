"""Generate dependency-free SVG figures from the saved Week 9 results."""

import html
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS = PROJECT_ROOT / "data/results/member3_week9_final_results.json"
FIGURE_DIR = PROJECT_ROOT / "docs/figures"


def _write_retrieval_figure(results: dict) -> None:
    comparison = results["retrieval_comparison"]
    metrics = [
        (
            "Top-1 accuracy",
            comparison["baseline"]["top_1_accuracy"],
            comparison["refined"]["top_1_accuracy"],
        ),
        (
            "Hit Rate@3",
            comparison["baseline"]["hit_rate_at_3"],
            comparison["refined"]["hit_rate_at_3"],
        ),
        (
            "MRR",
            comparison["baseline"]["mean_reciprocal_rank"],
            comparison["refined"]["mean_reciprocal_rank"],
        ),
    ]
    rows = []
    for index, (label, baseline, refined) in enumerate(metrics):
        y = 105 + index * 105
        rows.extend(
            [
                f'<text x="30" y="{y}" class="label">{html.escape(label)}</text>',
                f'<rect x="190" y="{y - 24}" width="{baseline * 430:.1f}" height="24" rx="5" fill="#94A3B8"/>',
                f'<text x="{205 + baseline * 430:.1f}" y="{y - 6}" class="value">{baseline * 100:.1f}%</text>',
                f'<rect x="190" y="{y + 12}" width="{refined * 430:.1f}" height="24" rx="5" fill="#2563EB"/>',
                f'<text x="{205 + refined * 430:.1f}" y="{y + 30}" class="value">{refined * 100:.1f}%</text>',
            ]
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="430" viewBox="0 0 760 430" role="img" aria-labelledby="title desc">
<title id="title">Member 3 retrieval baseline comparison</title>
<desc id="desc">Comparison of lexical baseline and intent-aware retrieval across three metrics on 60 synthetic queries.</desc>
<style>.title{{font:700 24px Arial;fill:#0F172A}}.sub{{font:14px Arial;fill:#475569}}.label{{font:600 15px Arial;fill:#1E293B}}.value{{font:600 13px Arial;fill:#0F172A}}.legend{{font:13px Arial;fill:#334155}}</style>
<rect width="760" height="430" fill="#F8FAFC" rx="16"/>
<text x="30" y="42" class="title">Policy Retrieval Comparison</text>
<text x="30" y="66" class="sub">Frozen controlled set: 60 synthetic labelled queries</text>
{''.join(rows)}
<rect x="30" y="390" width="16" height="16" rx="3" fill="#94A3B8"/><text x="54" y="403" class="legend">Week 8 lexical baseline</text>
<rect x="250" y="390" width="16" height="16" rx="3" fill="#2563EB"/><text x="274" y="403" class="legend">Week 9 intent-aware</text>
</svg>'''
    (FIGURE_DIR / "member3_retrieval_comparison.svg").write_text(svg, encoding="utf-8")


def _write_evidence_figure(results: dict) -> None:
    rates = results["evidence_validation"]["scenario_pass_rates"]
    labels = list(rates)
    bars = []
    for index, label in enumerate(labels):
        y = 90 + index * 42
        rate = rates[label]
        readable = label.replace("_", " ").title()
        bars.extend(
            [
                f'<text x="26" y="{y + 17}" class="label">{html.escape(readable)}</text>',
                f'<rect x="190" y="{y}" width="430" height="24" rx="5" fill="#E2E8F0"/>',
                f'<rect x="190" y="{y}" width="{rate * 430:.1f}" height="24" rx="5" fill="#059669"/>',
                f'<text x="635" y="{y + 17}" class="value">{rate * 100:.0f}%</text>',
            ]
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="550" viewBox="0 0 720 550" role="img" aria-labelledby="title desc">
<title id="title">Member 3 evidence validation by scenario</title>
<desc id="desc">Pass rate for ten evidence scenarios, with twelve synthetic cases in each scenario.</desc>
<style>.title{{font:700 24px Arial;fill:#0F172A}}.sub{{font:14px Arial;fill:#475569}}.label{{font:600 13px Arial;fill:#1E293B}}.value{{font:700 13px Arial;fill:#065F46}}</style>
<rect width="720" height="550" fill="#F8FAFC" rx="16"/>
<text x="26" y="40" class="title">Evidence Validation by Scenario</text>
<text x="26" y="64" class="sub">120 controlled cases: 10 scenarios × 12 cases</text>
{''.join(bars)}
<text x="26" y="530" class="sub">Synthetic controlled validation; not real-world accuracy.</text>
</svg>'''
    (FIGURE_DIR / "member3_evidence_scenario_results.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    _write_retrieval_figure(results)
    _write_evidence_figure(results)
    print(f"Wrote Member 3 figures to {FIGURE_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
