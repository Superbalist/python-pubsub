import json
from pathlib import Path

TEST_TOPIC = "test"
TEST_PATTERN = "test*"

EXAMPLES_DIR = Path("tests/example_payloads")

PERSON_PAYLOAD = (EXAMPLES_DIR / "person.json").read_text()
NOT_PERSON_PAYLOAD = (EXAMPLES_DIR / "not_a_person.json").read_text()
EVENT_PAYLOAD = (EXAMPLES_DIR / "event.json").read_text()
BROKEN_PAYLOAD = (EXAMPLES_DIR / "broken.json").read_text()
TEST_PAYLOAD = (EXAMPLES_DIR / "test.json").read_text()
SCHEMA_PAYLOAD = (EXAMPLES_DIR / "schema.json").read_text()

PERSON_OBJ = json.loads(PERSON_PAYLOAD)
NOT_PERSON_OBJ = json.loads(NOT_PERSON_PAYLOAD)
SCHEMA_OBJ = json.loads(SCHEMA_PAYLOAD)
EVENT_OBJ = json.loads(EVENT_PAYLOAD)

SCHEMA_URI = "https://example.com/person.schema.json"

TEST_OBJ = {
    "name": "Zaphod Beeblebrox",
    "tags": ["two-heads", "betelgeusian"],
    "relatives": [
        {"name": "Ford Prefect", "relation": "semi-half cousin"},
        {"name": "Zaphod Beeblebrox II", "relation": "father"},
        {"name": "Zaphod Beeblebrox III", "relation": "grandfather"},
        {"name": "Zaphod Beeblebrox IV", "relation": "great-grandfather"},
        {"name": "Mrs Alice Beeblebrox", "relation": "favorite mother"},
    ],
}

MULTIPLE_EVENT_PAYLOADS = (
    (EXAMPLES_DIR / "multiple_events.jsonl").read_text().splitlines()
)

MULTIPLE_EVENT_PAYLOADS_GCP = [
    {"data": p, "channel": TEST_TOPIC, "pattern": TEST_PATTERN}
    for p in MULTIPLE_EVENT_PAYLOADS
]

HTTP_BASE_URL = "http://127.0.0.1:3001/messages/"

GCP_PROJECT_ID = "pubsub-test-project"
