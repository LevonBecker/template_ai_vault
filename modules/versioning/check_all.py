"""Check and update both Python and library versions (combined view)."""

from ..common import cli
from ..common.properties import get_repo_local
from ..common.utils import info, success

# Import functions from other modules
from .libs import (
    apply_updates,
    display_updates_table,
    find_updates,
    get_installed_packages,
    get_outdated_packages,
    load_pyproject,
    save_pyproject,
)
from .python import (
    get_current_python_version,
    get_latest_stable_python,
    update_all_python_references,
)
from .python import (
    get_files_to_update as get_python_files,
)


@cli.command()
@cli.option("--dry-run", is_flag=True, help="Show updates without applying")
@cli.option("--yes", "-y", "no_confirm", is_flag=True, help="Skip confirmation")
def main(dry_run: bool, no_confirm: bool) -> None:  # pylint: disable=too-many-locals,too-many-statements
    """
    Check for Python and library updates, display unified view, update all configs.

    This checks both Python version and library dependencies, displays a
    combined summary, and prompts once to update all configuration files.

    IMPORTANT: This only updates config files. Run /upgrade to actually
    install the new versions.

    Examples:
        /version                  # Interactive mode
        /version --dry-run        # Preview changes
        /version --yes            # Auto-confirm all
    """
    info("Checking for Python and library updates...")

    repo_path = get_repo_local()

    # === Check Python ===
    current_major, current_minor = get_current_python_version(repo_path)
    latest_major, latest_minor, latest_patch = get_latest_stable_python()

    python_needs_update = current_minor < latest_minor
    python_current = f"{current_major}.{current_minor}"
    python_latest = f"{latest_major}.{latest_minor}.{latest_patch}"

    # === Check Libraries ===
    installed_packages = get_installed_packages()
    outdated_packages = get_outdated_packages()
    toml_doc, pyproject_path = load_pyproject(repo_path)
    lib_updates = find_updates(toml_doc, outdated_packages, installed_packages)

    # === Display Summary ===
    cli.echo("\n" + "=" * 60)
    cli.echo("📊 VERSION CHECK SUMMARY")
    cli.echo("=" * 60)

    # Python section
    cli.echo("\n🐍 Python:")
    if python_needs_update:
        cli.echo(f"   Current: {python_current}")
        cli.echo(f"   Latest:  {python_latest}")
        cli.echo("   Status:  ⚠️  Update available")
    else:
        cli.echo(f"   Current: {python_current}")
        cli.echo("   Status:  ✅ Up to date")

    # Libraries section
    cli.echo("\n📦 Libraries:")
    if lib_updates:
        cli.echo(f"   Outdated: {len(lib_updates)} packages in pyproject.toml")
        display_updates_table(lib_updates)
    else:
        cli.echo("   Status: ✅ All up to date")
        if outdated_packages:
            cli.echo(f"   Note: {len(outdated_packages)} outdated packages not in pyproject.toml")

    # === Check if anything needs updating ===
    if not python_needs_update and not lib_updates:
        cli.echo("\n" + "=" * 60)
        success("Everything is up to date!")
        raise SystemExit(3)

    # === Show what will be updated ===
    cli.echo("\n" + "=" * 60)
    cli.echo("📝 FILES THAT WILL BE UPDATED:")
    cli.echo("=" * 60)

    if python_needs_update:
        cli.echo("\n🐍 Python config files:")
        for config in get_python_files():
            cli.echo(f"   ✓ {config['file']}")

    if lib_updates:
        cli.echo("\n📦 Library config files:")
        cli.echo("   ✓ pyproject.toml")

    # === Dry run ===
    if dry_run:
        cli.echo("\n🔍 Dry-run mode: No changes made")
        cli.echo("\n💡 Run without --dry-run to update config files")
        return

    # === Confirmation ===
    if not no_confirm:
        cli.echo("\n" + "=" * 60)
        update_items = []
        if python_needs_update:
            update_items.append("Python")
        if lib_updates:
            update_items.append(f"{len(lib_updates)} libraries")

        update_summary = " and ".join(update_items)

        if not cli.confirm(f"💡 Update config files for {update_summary}?"):
            cli.echo("Cancelled.")
            raise SystemExit(2)

    # === Apply Updates ===
    cli.echo("\n" + "=" * 60)
    cli.echo("✏️  UPDATING CONFIG FILES...")
    cli.echo("=" * 60)

    updated_count = 0

    if python_needs_update:
        cli.echo("\n🐍 Updating Python config files...")
        count = update_all_python_references(repo_path, python_current, python_latest)
        updated_count += count
        success(f"Updated {count} Python config files")

    if lib_updates:
        cli.echo("\n📦 Updating library versions in pyproject.toml...")
        apply_updates(lib_updates)
        save_pyproject(toml_doc, pyproject_path)
        updated_count += len(lib_updates)
        success(f"Updated {len(lib_updates)} library versions")

    # === Final Message ===
    cli.echo("\n" + "=" * 60)
    success(f"Updated {updated_count} config file(s)")
    cli.echo("\n💡 Next steps:")
    cli.echo("   1. Review changes: git diff")
    cli.echo("   2. Install updates: /upgrade")
    cli.echo("   3. Or revert: git restore .")
    cli.echo()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
