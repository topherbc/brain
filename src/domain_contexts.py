from typing import Dict, Callable

DOMAIN_CONTEXTS: Dict[str, Dict[str, str]] = {
    'philosophy': {
        'perspective': "Explore the metaphysical and phenomenological implications",
        'tone': "Contemplative, introspective, drawing connections to broader existential questions",
        'approach': "Seek deeper meaning beyond immediate scientific explanation"
    },
    'science': {
        'perspective': "Provide precise, empirical understanding",
        'tone': "Analytical, evidence-based, focused on mechanism and process",
        'approach': "Explain through observable, testable phenomena"
    },
    'poetry': {
        'perspective': "Interpret through metaphor and emotional resonance",
        'tone': "Lyrical, evocative, emphasizing subjective experience",
        'approach': "Explore symbolic and aesthetic dimensions"
    }
}

def get_domain_context(domain: str) -> Dict[str, str]:
    """
    Retrieve specialized context for a given domain
    """
    return DOMAIN_CONTEXTS.get(domain, DOMAIN_CONTEXTS['science'])