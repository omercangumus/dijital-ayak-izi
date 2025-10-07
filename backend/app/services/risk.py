from typing import List, Literal


def score_results(items: List[dict]) -> int:
    score = 0
    for it in items:
        t = it.get('type')
        if t == 'breach':
            score += 40
        elif t == 'social':
            score += 15
        elif t == 'image':
            score += 12
        elif t == 'web':
            score += 8
    return max(0, min(100, score))


def classify(score: int) -> Literal['dusuk', 'orta', 'yuksek']:
    if score < 30:
        return 'dusuk'
    if score < 70:
        return 'orta'
    return 'yuksek'


