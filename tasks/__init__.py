from invoke import Collection

from .ai import docs, hermes, ollama, opencode, repo, template
from .ai_vault import chat, topic
from .common import debug, ruff, setup, upgrade, uv, versioning
from .common import main as common_main
from .tests import namespace as tests_namespace

namespace = Collection(auto_dash_names=False)

namespace.add_collection(debug, name="debug")
namespace.add_collection(ruff, name="ruff")
namespace.add_collection(setup, name="setup")
namespace.add_collection(tests_namespace, name="tests")
namespace.add_collection(upgrade, name="upgrade")
namespace.add_collection(uv, name="uv")
namespace.add_collection(versioning, name="ver")

# `ai/` groups tooling this repo uses to operate on itself, or to integrate with a specific AI
# tool — git/PR workflow (`repo`), parent-template sync (`template`), per-tool command sync
# (`hermes`, `opencode`) / local-LLM management (`ollama`), and changelog sync (`docs`).
# `repo`/`template` modules already existed but had no `invoke` task exposing them until now — see
# tasks/ai/repo.py and tasks/ai/template.py's own docstrings.
namespace.add_collection(docs, name="docs")
namespace.add_collection(hermes, name="hermes")
namespace.add_collection(ollama, name="ollama")
namespace.add_collection(opencode, name="opencode")
namespace.add_collection(repo, name="repo")
namespace.add_collection(template, name="template")

# `ai_vault/` is this repo's own reason for existing — dated planning-chat logging (`chat`) and
# topic workspace management (`topic`). Same story as `ai/` above: real modules, newly exposed as
# tasks. Kept at their original-shape top-level names (`chat.*`, `topic.*`), matching every other
# grouped-but-not-renamed folder here.
namespace.add_collection(chat, name="chat")
namespace.add_collection(topic, name="topic")

# Combo Tasks
ai_collection = Collection("ai")
ai_collection.add_task(common_main.ai_sync, name="sync")
namespace.add_collection(ai_collection)

namespace.add_task(common_main.fix, name="fix")
namespace.add_task(common_main.test, name="test")
namespace.add_task(versioning.update, name="update")
