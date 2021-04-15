"""
Create a Pug
"""
from discord.ext.commands import command

from .. import conf
from ..exceptions import PugNotFound
from ..pugs import Team, PugListHandler, create_pug_embed


@command()
async def createteam(ctx, *args):
    f"""
    If you are the lobby owner, this disbands the pug

    Checks: 

    Syntax: {conf.PREFIX}
    """
    # Check if any args were given
    if not args:
        await ctx.send(f"ERROR: {ctx.command} `<name>`, dimwit.")
        return

    # Change the tuple to a list
    args = list(args)

    # Combine the args to create a team name
    team_name = " ".join(args)

    # Get the pug by the lobby
    try:
        pug = PugListHandler.get_pug_by_channel(ctx.guild.id, ctx.channel)
    except PugNotFound:
        # If no pugs could be found, send an error message and exit the function
        await ctx.send(f"There are no on-going pugs in {ctx.channel}. Use `{conf.PREFIX}create` to create one.")
        return

    # Check existing teams
    team_exists = bool(list(filter(lambda x: x.name == team_name, pug.teams)))
    if team_exists:
        await ctx.send(f"The team name `{team_name}` has already been taken. Pick another one.")
        return

    # Create a new team
    new_team = Team(name=team_name)

    # Add the person who created the team
    new_team.add_player(ctx.author)

    # Add the team to the pug
    pug.add_team(new_team)

    # Send an embed for the new pug
    await ctx.send(embed=await create_pug_embed(pug, footer=f"Team {new_team.name} has been established!"))