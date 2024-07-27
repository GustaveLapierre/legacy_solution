import itertools
from src.models import Entries, db


def concat_summaries(record_id: str) -> list[dict]:
    # get entries
    entries = Entries.query.filter_by(record_id=record_id).with_entities(Entries.title, Entries.summary).all()
    # sort
    entries = sorted(entries, key=lambda entry: entry[0])
    # group
    entries = itertools.groupby(entries, key=lambda entry: entry[0])
    # make new list with expected entries
    entries = [{"key": key, "value": list(value)} for key, value in entries]
    # join all text in value, triple new lines as hint for LLM
    entries = [{"key": entry["key"], "value": "\n\n\n".join([v[1] for v in entry["value"]])} for entry in entries]
    return entries