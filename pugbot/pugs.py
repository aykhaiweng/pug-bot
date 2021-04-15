import uuid
from collections import OrderedDict

import discord

from . import conf
from .consts import PugStatus
from .exceptions import (
    PugNameAlreadyExists,
    PugNotFound
)


"""
An example of how the PUG_LIST is supposed to look like:

PUG_LIST = {
    "<guild_id>" : {
        "<pug_name>": PugObject
    }
}
"""

PUG_LIST=OrderedDict()
class PugListHandler(object):
    """
    A handler used for the PUG_LIST

    The PUG_LIST acts as a temporary store for the pugs.
    """

    @classmethod
    def get_or_create_guild(cls, guild_id):
        """
        GET or CREATE the guild key, this can double up as a guildlist
        """
        if guild_id not in PUG_LIST.keys():
            PUG_LIST[guild_id] = {}
        return PUG_LIST[guild_id]

    @classmethod
    def add_pug(cls,  pug):
        """
        ADD a pug to the pug list for the guild
        """
        guild_id = pug.guild.id
        pugs = cls.get_or_create_guild(guild_id)
        if pug.name in pugs.keys():
            raise PugNameAlreadyExists(f'Pug {pug.name} already exists')
        pugs[pug.name] = pug

    @classmethod
    def remove_pug(cls, pug):
        """
        REMOVES a pug to the pug list for the guild
        """
        guild_id = pug.guild.id
        pugs = cls.get_or_create_guild(guild_id)
        del pugs[pug.name]

    @classmethod
    def get_pug_by_name(cls, guild_id, pug_name):
        """
        GET a pug using the pug's ID
        """
        pugs = cls.get_or_create_guild(guild_id)
        return pugs.get(pug_name)

    @classmethod
    def get_pug_by_channel(cls, guild_id, channel):
        """
        GET a pug using the pug's ID
        """
        pugs = cls.get_or_create_guild(guild_id)
        for pug_name, pug in reversed(pugs.items()):
            if pug.lobby_channel == channel:
                return pug
        raise PugNotFound(f"No on-going Pug in {channel}")


class Pug(object):
    """
    Holds the information of a single Pug in a python object

    @INPUT  name: Name of the pug
            owner: User object of the pug owner
            lobby_channel: which channel serves as the lobby
            guild: Which guild this pug resides in
            max_size: Max size of the pug
            teams: dictionary of teamnames and the players in them {'team 1': [('member 1', 'meta': {'is_captain': True})]}
            players: list of active players
            status: what status the pug is currently in
    """

    def __init__(
        self,
        name,
        owner,
        lobby_channel,
        guild,
        max_size,
        teams=[],
        players=[],
        status=PugStatus.OPEN.value,
    ):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.owner = owner
        self.lobby_channel = lobby_channel
        self.guild = guild
        self.max_size = max_size
        self.teams = teams
        self.players = players
        self.status = status
        super().__init__()

    def __str__(self):
        return self.name

    # Management methods -----
    def add_player(self, user):
        """
        Adds a User to the list of players
        """
        if len(self.players) < self.max_size:
            self.players.append(user)
            return True
        else:
            return False
    
    def remove_player(self, user):
        """
        Removes a User from the list of players
        """
        self.players.remove(user)
    
    def add_team(self, team):
        """
        Adds a Team object to the list of teams
        """
        self.teams.append(team)

    def remove_team(self, team):
        """
        Delete the team objects
        """
        if team in self.teams:
            self.teams.remove(team)

    # Status methods -----
    def remaining_players(self):
        """
        Checks for players that do not have a team yet.
        """
        return self.players

    def get_players_in_teams(self):
        """
        Get the players who are in teams.
        """
        players_in_teams = []
        for team in self.teams:
            team
        return players_in_teams

    @classmethod
    def get_category_channels(cls, channel=None):
        """
        Retrieves the category channels based on the lobby that it's being typed in
        """
        channel = channel or cls.lobby_channel
        return channel.category.voice_channels


class Team(object):
    """
    This object holds a name, who's the captain and who are the team-members
    
    Store in pug.teams = {'<team_name>': <Team Object>}
    """

    def __init__(self, name, captain=None, players=[]):
        self.name = name
        self.captain = captain
        self.players = players

    # Management methods -----
    def add_player(self, user):
        """
        Adds a User to the list of players
        """
        self.players.append(user)
        if len(self.players) >= 1 and self.captain is None:
            self.set_captain(user)
    
    def remove_player(self, user):
        """
        Removes a User from the list of players
        """
        self.players.remove(user)
        if user == self.captain and len(self.players) > 1:
            self.captain(self.players[0])

    def set_captain(self, user):
        """
        Set a player as the captain
        """
        self.captain = user


async def create_pug_embed(pug, title=None, description=None, status=None, footer=None, color=None):
    """
    Creates an embed for the pug
    """
    if not status:
        status = pug.status

    status_mapping = {
        PugStatus.OPEN.value: ('blue', "The PUG is now OPEN!"),
        PugStatus.STARTED.value: ('green', "The PUG is now IN PROGRESS!"),
        PugStatus.ENDED.value: ('gold', "The PUG has now ENDED"),
    }

    # defaults
    if color:
        color = color
    else:
        color = status_mapping[status][0]
        if status == PugStatus.OPEN.value:
            # If the lobby is open, turn it red when it's full
            if len(pug.players) == pug.max_size:
                color = 'red'
    color = getattr(discord.Color, color)()
    footer_text = footer or status_mapping[status][1]

    # Create the initial embed
    embed = discord.Embed(
        title=title or f"{pug.name}",  # ({len(pug.players)}/{pug.max_size})",
        description=description or f"Type `{conf.PREFIX}join` in this channel to join this lobby",
        type="rich",
        color=color,
    )

    # Set the footer
    embed.set_footer(text=footer_text)

    # Set the author of the embed
    embed.set_author(
        name=pug.owner.name,
        icon_url=pug.owner.avatar_url
    )

    # Player count
    embed.add_field(
        name="Player Count",
        value=f"{len(pug.players)}/{pug.max_size}",
        inline=False
    )

    # Team list
    team_list = [x for i, x in enumerate(pug.teams)]
    for i, team in enumerate(team_list):
        team_string = f"Channel: {None}\n"
        for i, tp in enumerate(team.players):
            if tp == team.captain:
                team_string += f"`[{i + 1}]` **{tp.name} (captain)**\n"
            else:
                team_string += f"`[{i + 1}]` {tp.name}\n"

        embed.add_field(
            name=f"Team {i+1}: {team.name}",
            value=team_string,
            inline=False
        )

    # Player list
    player_list = pug.players
    if player_list:
        player_list_string = [f"`[{i+1}]` {x.name}" for i, x in enumerate(pug.players)]
        player_list_string = "\n".join(player_list_string)
    else:
        player_list_string = "-"
    embed.add_field(
        name="Players",
        value=player_list_string,
        inline=True
    )

    # Channel list
    channel_list = pug.get_category_channels(pug.lobby_channel)
    if channel_list:
        channel_list_string = [f"`[{i+1}]` {x.name}" for i, x in enumerate(pug.get_category_channels(pug.lobby_channel))]
        channel_list_string = "\n".join(channel_list_string)
    else:
        channel_list_string = "-"
    embed.add_field(
        name="Channels",
        value=channel_list_string,
        inline=True
    )

    return embed