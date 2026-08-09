from mp_research.adapters import GPTResearcherAdapter, OpenDeepResearchAdapter, StormAdapter
from mp_research.models import EngineName

_ADAPTERS = {
    EngineName.GPT_RESEARCHER: GPTResearcherAdapter,
    EngineName.OPEN_DEEP_RESEARCH: OpenDeepResearchAdapter,
    EngineName.STORM: StormAdapter,
    EngineName.COSTORM: StormAdapter,
}


def get_adapter(engine: EngineName):
    return _ADAPTERS[engine]()
