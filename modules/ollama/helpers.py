"""Shared helpers for Ollama module operations."""

import json
import sys
import termios
import time
import tty
import urllib.error
import urllib.request

from ..common.utils import error, success

_OLLAMA_API = "http://localhost:11434"


def dbg(message: str, debug: bool) -> None:
    """Print a debug line immediately to stderr."""
    if debug:
        sys.stderr.write(f"[debug] {message}\n")
        sys.stderr.flush()


def read_char_choice(max_choice: int, debug: bool = False) -> int:
    """Prompt for a menu choice and return the integer selection.

    Uses single-keypress input when stdin is a TTY; falls back to regular
    line input (with Enter) when running through invoke or a piped context.
    """
    fd = sys.stdin.fileno()
    dbg(f"read_char_choice: fd={fd} max_choice={max_choice}", debug)
    dbg(f"read_char_choice: stdin.isatty()={sys.stdin.isatty()}", debug)

    try:
        old = termios.tcgetattr(fd)
        dbg("read_char_choice: termios.tcgetattr succeeded — real TTY path", debug)
    except termios.error as exc:
        dbg(f"read_char_choice: termios.error={exc!r} — fallback line-input path", debug)
        # Not a real TTY — use regular line input
        while True:
            sys.stdout.write(f"Enter choice [1-{max_choice}]: ")
            sys.stdout.flush()
            dbg("read_char_choice: waiting on sys.stdin.readline()...", debug)
            raw = sys.stdin.readline().strip()
            dbg(f"read_char_choice: readline() returned {raw!r}", debug)
            if raw.isdigit() and 1 <= int(raw) <= max_choice:
                dbg(f"read_char_choice: valid choice {int(raw)}", debug)
                return int(raw)
            sys.stdout.write(f"Invalid choice. Enter a number between 1 and {max_choice}.\n")
            sys.stdout.flush()
        return -1  # unreachable, satisfies type checker

    # Real TTY — single keypress, no Enter needed
    sys.stdout.write(f"Press a key [1-{max_choice}]: ")
    sys.stdout.flush()
    dbg("read_char_choice: entering tty.setraw loop", debug)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            dbg(f"read_char_choice: got char {ch!r} (ord={ord(ch) if ch else 'N/A'})", debug)
            if ch == "\x03":
                raise KeyboardInterrupt
            if ch.isdigit() and 1 <= int(ch) <= max_choice:
                sys.stdout.write(ch + "\n")
                sys.stdout.flush()
                dbg(f"read_char_choice: returning {int(ch)}", debug)
                return int(ch)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        dbg("read_char_choice: terminal settings restored", debug)


def _pull_progress_line(status: str, total: int, completed: int, elapsed_secs: int) -> str:
    """Format a single progress line for pull_model output."""
    mins, secs = divmod(elapsed_secs, 60)
    prefix = f"   ⏳ {mins}m{secs:02d}s — {status}"
    if total and completed:
        pct = completed / total * 100
        gb_done = completed / (1024**3)
        gb_total = total / (1024**3)
        return f"{prefix}: {gb_done:.1f}/{gb_total:.1f}GB ({pct:.0f}%)"
    return prefix


def pull_model(model: str, debug: bool = False) -> None:
    """Pull a model via the Ollama REST API, streaming real-time progress."""
    dbg(f"pull_model: start model={model!r}", debug)

    sys.stdout.write(f"\n📥 Pulling {model} — this may take several minutes...\n")
    sys.stdout.flush()

    req = urllib.request.Request(
        f"{_OLLAMA_API}/api/pull",
        data=json.dumps({"model": model, "stream": True}).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    start = time.time()
    last_status = ""
    last_print_time = start

    try:
        with urllib.request.urlopen(req, timeout=None) as resp:  # no socket timeout — downloads can be slow
            dbg("pull_model: connected to Ollama API, streaming events...", debug)
            for raw_line in resp:
                line = raw_line.decode().strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    dbg(f"pull_model: unparseable line: {line!r}", debug)
                    continue

                dbg(f"pull_model: event={event}", debug)

                if event.get("error"):
                    error(f"Ollama error: {event['error']}")

                status = event.get("status", "")
                now = time.time()
                should_print = status != last_status or (event.get("total") and now - last_print_time >= 5)

                if should_print:
                    line_out = _pull_progress_line(
                        status, event.get("total", 0), event.get("completed", 0), int(now - start)
                    )
                    sys.stdout.write(line_out + "\n")
                    sys.stdout.flush()
                    last_status = status
                    last_print_time = now

    except urllib.error.URLError as exc:
        error(f"Cannot reach Ollama at {_OLLAMA_API} — is the service running? ({exc})")

    elapsed = int(time.time() - start)
    mins, secs = divmod(elapsed, 60)
    success(f"{model} ready — took {mins}m{secs:02d}s")
    dbg("pull_model: done", debug)
