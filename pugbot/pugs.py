import uuid

from .consts import PugStatus

"""
I imagine the pug list being sorted accordingly:

Guild 
    |- Pugs

So the PUG_LIST will be a pseudo Redis server that looks something like:
{
    "<guild_uuid>": {
        "<pug_uuid>": "{}",
        "<pug_uuid>": "{}"
    }
}
"""

PUG_LIST = {}  # acts as temporary store


class Pug:
    """
    Holds the information of a single Pug

    @INPUT  name: Name of the pug
            owner: User object of the pug owner
            guild: Which guild this pug resides in
            max_size: Max size of the pug
            teams: dictionary of teamnames and the players in them {'team 1': [('member 1', 'meta': {'is_captain': True})]}
            players: list of active players
            lobby_channel: which channel serves as the lobby
            status: what status the pug is currently in
    """

    def __init__(
        self,
        name,
        owner,
        guild,
        max_size,
        teams={},
        players=[],
        lobby_channel=None,
        status=PugStatus.OPEN
    ):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.owner = owner
        self.guild = guild
        self.max_size = max_size
        self.teams = teams
        self.players = players
        self.lobby_channel = lobby_channel
        self.status = status

        # Auto add the owner to the players
        self.players.append(self.owner)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def set_owner(self, user):
        """
        Set as User as the owner
        """
        self.owner = user

    def add_players(self, user):
        """
        Adds a User to the list of players
        """
        if len(self.players) < 10:
            self.players.append(user)
        else:
            pass


def get_pugs_for_guild(guild):
    """
    Returns all the pugs

    @INPUT  guild:  setting it to None will not run
                    the filter function
    """
    try:
        pug_list = PUG_LIST[guild.id]
    except KeyError:
        pug_list = {}

    return pug_list


def add_to_pug_list(pug):
    """
    Adds a Pug instance to the PUG_LIST
    """
    guild = pug.guild

    if guild.id not in PUG_LIST:
        PUG_LIST[guild.id] = {}

    PUG_LIST[guild.id].update(
        { pug.uuid: pug }
    )


def remove_from_pug_list(pug):
    """
    Removes a list of Pug instances from the PUG_LIST
    """
    guild = pug.guild

    del PUG_LIST[guild.id][pug.uuid]
