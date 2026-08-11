from invoke import task


@task
def check_agents(context):
    """Verify .github/prompts/ is mirrored into every synced command/skill dir"""
    print("\n------------")
    print("Check Agents")
    print("------------\n")
    context.run('pytest -m "agents"')
