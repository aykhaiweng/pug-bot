import uuid
from collections import OrderedDict

import discord

from pugbot import conf
from pugbot.consts import PugStatus
from pugbot.exceptions import (
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
    def get_or_create_guild(cls, guild: discord.Guild):
        """
        GET or CREATE the guild key, this can double up as a guildlist
        """
        if guild.id not in PUG_LIST.keys():
            PUG_LIST[guild.id] = {}
        return PUG_LIST[guild.id]

    @classmethod
    def add_pug(cls,  pug):
        """
        ADD a pug to the pug list for the guild
        """
        pugs = cls.get_or_create_guild(pug.guild)
        if pug.name in pugs.keys():
            raise PugNameAlreadyExists(f'Pug {pug.name} already exists')
        pugs[pug.name] = pug

    @classmethod
    def remove_pug(cls, pug):
        """
        REMOVES a pug to the pug list for the guild
        """
        pugs = cls.get_or_create_guild(pug.guild)
        del pugs[pug.name]

    @classmethod
    def get_pug_by_name(cls, guild: discord.Guild, pug_name):
        """
        GET a pug using the pug's ID
        """
        pugs = cls.get_or_create_guild(guild.id)
        return pugs.get(pug_name)

    @classmethod
    def get_pug_by_channel(
        cls, guild: discord.Guild, channel: discord.TextChannel
    ):
        """
        GET a pug using the pug's ID
        """
        pugs = cls.get_or_create_guild(guild)
        for pug_name, pug in reversed(pugs.items()):
            if pug.lobby_channel == channel:
                return pug


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
        teams=None,
        players=None,
        status=PugStatus.OPEN.value,
    ):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.owner = owner
        self.lobby_channel = lobby_channel
        self.guild = guild
        self.max_size = max_size
        self.teams = teams or list()
        self.players = players or list()
        self.status = status
        super().__init__()

    def __str__(self):
        return self.name

    # Management methods -----
    def add_player(self, user: discord.Member):
        """
        Adds a User to the list of players
        """
        if len(self.players) < self.max_size:
            self.players.append(user)
            return True
        else:
            return False
    
    def remove_player(self, user: discord.Member):
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
    def get_remaining_players(self):
        """
        Checks for players that do not have a team yet.
        """
        players_in_teams = self.get_players_in_teams()
        remaining_players = list(filter(lambda x: x not in players_in_teams, self.players))
        return remaining_players

    def get_players_in_teams(self):
        """
        Get the players who are in teams.
        """
        players_in_teams = list()
        for team in self.teams:
            players_in_teams.extend(team.players)
        return players_in_teams

    @classmethod
    def get_category_channels(cls, text_channel: discord.TextChannel):
        """
        Retrieves the voice channels based on the lobby_channel
        """
        text_channel = text_channel or cls.lobby_channel
        return text_channel.category.voice_channels


class Team(object):
    """
    This object holds a name, who's the captain and who are the team-members
    
    Store in pug.teams = {'<team_name>': <Team Object>}
    """

    def __init__(self, name, captain=None, players=None, voice_channel=None):
        self.name = name
        self.captain = captain
        self.players = players or list()
        self.voice_channel = voice_channel

    # Management methods -----
    def add_player(self, user: discord.Member):
        """
        Adds a User to the list of players
        """
        self.players.append(user)
        if len(self.players) >= 1 and self.captain is None:
            self.set_captain(user)
    
    def remove_player(self, user: discord.Member):
        """
        Removes a User from the list of players
        """
        self.players.remove(user)
        if user == self.captain and len(self.players) >= 1:
            # If the user leaving is the captain and there are still players in the team
            self.captain(self.players[0])

    def set_captain(self, user: discord.Member):
        """
        Set a player as the captain
        """
        self.captain = user

    def set_channel(self, voice_channel: discord.VoiceChannel):
        """
        Set the voice_channel for this team
        """
        self.voice_channel = voice_channel


async def create_pug_embed(
    pug, title=None, description=None, status=None, footer=None, color=None
):
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
    description = description or (
        f"Type `{conf.PREFIX}join` in this channel to join this lobby"
    )

    # Create the initial embed
    embed = discord.Embed(
        title=title or f"{pug.name}",
        description=description,
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
    players = pug.players
    players_in_teams = pug.get_players_in_teams()
    if players:
        player_list_string = str()
        for i, p in enumerate(players):
            if p in players_in_teams:
                # If the player is already in a team, cross them out
                player_list_string += f"~~`[{i+1}]` {p.name}~~\n"
            else:
                player_list_string += f"`[{i+1}]` {p.name}\n"
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