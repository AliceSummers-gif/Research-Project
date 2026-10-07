"""Re-evaluate fixed Week 8 scenarios; never overwrite historical results."""
import hashlib
import json
import platform
from pathlib import Path
import joblib
from src.agent.agent import run_agent
from src.agent.final_agent import run_final_agent
from src.common.schemas import Member1Output, Member2Output, Member3Output

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    model_path = ROOT / 'models/student4_evidence_confidence_v1.joblib'
    model = joblib.load(model_path)
    report = {'scope': 'Reused synthetic Week 8 scenarios; not new independent test data or real-image accuracy.',
              'python': platform.python_version(), 'model_sha256': digest(model_path),
              'selection': 'ML 0.90 from Week 8 validation; rule corroboration 0.80 motivated by validation V08. Test cases were previously seen; this is a regression comparison.',
              'splits': {}}
    for split in ('validation', 'test'):
        inputs_path = ROOT / f'data/member4/week8/{split}_inputs.json'
        labels_path = ROOT / f'data/member4/week8/{split}_labels.json'
        cases = json.loads(inputs_path.read_text())
        label_rows = json.loads(labels_path.read_text())
        labels = {r['case_id']: r['expected_decision'] for r in label_rows}
        ids = [c['case_id'] for c in cases]
        if not cases or len(set(ids)) != len(ids) or len(labels) != len(label_rows) or set(ids) != set(labels):
            raise ValueError('Inputs and labels must have matching unique case IDs.')
        methods = {}
        for profile, agent in (('baseline', run_agent), ('final', run_final_agent)):
            for method in ('rule', 'ml'):
                rows = []
                for case in cases:
                    outputs = (Member1Output(**case['member1']), Member2Output(**case['member2']), Member3Output(**case['member3']))
                    if any(o.case_id != case['case_id'] for o in outputs):
                        raise ValueError('Mismatched case ID')
                    result = agent(*outputs, confidence_method=method, model=model if method == 'ml' else None)
                    expected = labels[case['case_id']]
                    rows.append({'case_id': case['case_id'], 'expected': expected,
                                 'predicted': result.decision, 'reason': result.reason,
                                 'confidence': result.evidence_confidence})
                summary = {'total': len(rows), 'correct': sum(r['expected'] == r['predicted'] for r in rows)}
                for name, decision in (('incorrect_auto_refunds','AUTO_REFUND'), ('unnecessary_reviews','HUMAN_REVIEW'), ('unnecessary_evidence_requests','REQUEST_MORE_EVIDENCE')):
                    summary[name] = sum(r['predicted'] == decision and r['expected'] != decision for r in rows)
                methods[f'{profile}_{method}'] = {'summary': summary, 'cases': rows}
                print(split, profile, method, summary)
        report['splits'][split] = {'input_sha256': digest(inputs_path), 'labels_sha256': digest(labels_path), 'methods': methods}
    source_paths = ('src/agent/agent.py', 'src/agent/final_agent.py', 'src/decision/decision.py', 'src/decision/confidence.py')
    report['source_sha256'] = {p: digest(ROOT / p) for p in source_paths}
    output = ROOT / 'data/results/student4_week9/final_comparison.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')

if __name__ == '__main__':
    main()
