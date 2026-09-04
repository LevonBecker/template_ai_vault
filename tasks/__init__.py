from fireball_sidecar_toolkit.tasks import collection as toolkit_tasks
from invoke import Collection

from .toolkit import chat, debug, docs, repo, screenshots, setup, topic, versioning
from .toolkit import main as common_main
from .toolkit import tests as toolkit_tests

namespace = Collection(auto_dash_names=False)

# `toolkit/` — vendored from fireball_sidecar_toolkit, shared with every family repo. Registered at
# their original top-level names so nothing that calls them needs to change.
namespace.add_collection(Collection.from_module(debug, auto_dash_names=False), name="debug")
namespace.add_collection(Collection.from_module(setup, auto_dash_names=False), name="setup")
namespace.add_collection(Collection.from_module(toolkit_tests, auto_dash_names=False), name="tests")
namespace.add_collection(Collection.from_module(versioning, auto_dash_names=False), name="versioning")
namespace.add_collection(Collection.from_module(versioning, auto_dash_names=False), name="ver")
namespace.add_collection(Collection.from_module(docs, auto_dash_names=False), name="docs")
namespace.add_collection(Collection.from_module(repo, auto_dash_names=False), name="repo")
namespace.add_collection(Collection.from_module(screenshots, auto_dash_names=False), name="screenshots")
namespace.add_collection(Collection.from_module(chat, auto_dash_names=False), name="chat")
namespace.add_collection(Collection.from_module(topic, auto_dash_names=False), name="topic")

# Shared AI-tooling propagation — `sidecar.toolkit.{download,check,sync,upload,release}` from the
# `fireball_sidecar_toolkit` package. Replaces the retired `/template` sync.
sidecar_ns = Collection("sidecar")
sidecar_ns.add_collection(toolkit_tasks, name="toolkit")
namespace.add_collection(sidecar_ns)

namespace.add_task(common_main.fix, name="fix")
namespace.add_task(common_main.test, name="test")
namespace.add_task(versioning.check, name="update")
namespace.add_task(versioning.upgrade, name="upgrade")
