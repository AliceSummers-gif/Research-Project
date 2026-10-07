"""Week 9 conservative profile; Week 8 baseline remains reproducible."""
from src.agent.agent import run_agent
from src.decision.confidence import calculate_evidence_confidence

ML_AUTO_MIN = 0.90
RULE_AUTO_MIN = 0.80


def run_final_agent(member1, member2, member3, *, confidence_method='rule', model=None):
    result = run_agent(member1, member2, member3,
                       confidence_method=confidence_method, model=model)
    if confidence_method == 'ml' and result.decision == 'AUTO_REFUND':
        rule_score = calculate_evidence_confidence(member1, member2, member3)
        if result.evidence_confidence < ML_AUTO_MIN or rule_score < RULE_AUTO_MIN:
            return result.model_copy(update={
                'decision': 'REQUEST_MORE_EVIDENCE',
                'reason': ('Final ML safeguard: automatic refund requires ML confidence '
                           'at least 0.90 and rule-based evidence confidence at least 0.80. '
                           f'ML={result.evidence_confidence:.2f}, rule={rule_score:.2f}.')})
    return result
