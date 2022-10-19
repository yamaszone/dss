import json
from typing import Dict, Optional

from implicitdict import ImplicitDict
from monitoring.mock_uss.geoawareness.parsers.ed269 import ED269Schema
from monitoring.monitorlib.geoawareness_automated_testing.api import (
    GeozoneSourceState,
    GeozoneSourceDefinition,
)
from monitoring.monitorlib.multiprocessing import SynchronizedValue


class ExistingRecordException(ValueError):
    pass


class SourceRecord(ImplicitDict):
    definition: GeozoneSourceDefinition
    state: GeozoneSourceState
    message: Optional[str]
    geozone_ed269: Optional[ED269Schema]


class Database(ImplicitDict):
    """Simple pseudo-database structure tracking the state of the mock system"""

    sources: Dict[str, SourceRecord] = {}

    @staticmethod
    def get_source(db: SynchronizedValue, id: str) -> SourceRecord:
        return db.value.sources.get(id, None)

    @staticmethod
    def insert_source(
        db: SynchronizedValue,
        id: str,
        definition: GeozoneSourceDefinition,
        state: GeozoneSourceState,
        message: Optional[str] = None,
    ) -> SourceRecord:
        with db as tx:
            if id in tx.sources.keys():
                raise ExistingRecordException()
            tx.sources[id] = SourceRecord(
                definition=definition, state=state, message=message
            )
            result = tx.sources[id]
        return result

    @staticmethod
    def update_source_state(
        db: SynchronizedValue,
        id: str,
        state: GeozoneSourceState,
        message: Optional[str] = None,
    ):
        with db as tx:
            tx.sources[id]["state"] = state
            tx.sources[id]["message"] = message
            result = tx.sources[id]
        return result

    @staticmethod
    def update_source_geozone_ed269(
        db: SynchronizedValue, id: str, geozone: ED269Schema
    ):
        with db as tx:
            tx.sources[id]["geozone_ed269"] = geozone
            result = tx.sources[id]
        return result

    @staticmethod
    def delete_source(db: SynchronizedValue, id: str):
        with db as tx:
            return tx.sources.pop(id, None)


db = SynchronizedValue(
    Database(),
    decoder=lambda b: ImplicitDict.parse(json.loads(b.decode("utf-8")), Database),
)