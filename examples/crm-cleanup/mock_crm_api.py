"""A tiny stand-in for a CRM REST API, backed by a local JSON file.

Same shape as the calls the real script makes: list, get, single update,
batch update with per-record errors. Every write appends to the property
history, like a real CRM does.
"""
import datetime
import json


class MockCRM:
    def __init__(self, path):
        self.path = path
        with open(path) as f:
            self.data = json.load(f)
        self.by_id = {c["id"]: c for c in self.data["contacts"]}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=1)

    def list_contacts(self):
        return list(self.data["contacts"])

    def get(self, cid):
        return self.by_id[cid]

    def update(self, cid, properties):
        contact = self.by_id[cid]
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        for key, value in properties.items():
            contact["properties"][key] = value
            contact["history"].setdefault(key, []).insert(0, {"value": value, "source": "api", "timestamp": now})
        self._save()

    def batch_update(self, inputs):
        updated, errors = 0, []
        for item in inputs:
            if item["id"] not in self.by_id:
                errors.append({"id": item["id"], "error": "not found"})
                continue
            self.update(item["id"], item["properties"])
            updated += 1
        return {"updated": updated, "errors": errors}
