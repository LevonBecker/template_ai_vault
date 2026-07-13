from invoke import Collection

from . import claude, cline, combos, debug, hermes, ollama, opencode, ruff, tests, upgrade, versioning

namespace = Collection()
namespace.configure({"auto_dash_names": False})

namespace.add_collection(claude, name="claude")
namespace.add_collection(cline, name="cline")
namespace.add_collection(debug, name="debug")
namespace.add_collection(hermes, name="hermes")
namespace.add_collection(ollama, name="ollama")
namespace.add_collection(opencode, name="opencode")
namespace.add_collection(ruff, name="ruff")
namespace.add_collection(tests, name="tests")
namespace.add_collection(upgrade, name="upgrade")
namespace.add_collection(versioning, name="versioning")

# Combo Tasks
ai_collection = Collection("ai")
ai_collection.add_task(combos.ai_sync, name="sync")
namespace.add_collection(ai_collection)

namespace.add_task(combos.fix, name="fix")
namespace.add_task(combos.test, name="test")
