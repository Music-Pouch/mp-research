from mp_research.models import EngineName, ResearchBrief, RunMetadata


def test_run_metadata_gets_job_id():
    metadata = RunMetadata(engine=EngineName.GPT_RESEARCHER)
    assert metadata.job_id


def test_brief_preserves_constraints():
    brief = ResearchBrief(title="test", prompt="research this", constraints=["primary sources"])
    assert brief.constraints == ["primary sources"]
