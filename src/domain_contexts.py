from typing import Dict, Any

class DomainContext:
    @staticmethod
    def apply_scientific_lens(original_output: str, input_query: str) -> str:
        return f"[Scientific Lens] {original_output}\nRigorously analyzed through empirical, measurable parameters."

    @staticmethod
    def apply_philosophical_lens(original_output: str, input_query: str) -> str:
        return f"[Philosophical Lens] {original_output}\nReframed through existential and epistemological considerations."

    @staticmethod
    def apply_poetic_lens(original_output: str, input_query: str) -> str:
        return f"[Poetic Lens] {original_output}\nTransformed into a metaphorical, emotionally resonant interpretation."

    DOMAIN_LENSES: Dict[str, Any] = {
        'science': apply_scientific_lens,
        'philosophy': apply_philosophical_lens,
        'poetry': apply_poetic_lens
    }