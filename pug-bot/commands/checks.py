"""
This module creates a decorator called `check` which takes a list of functions to run
If any of these checks fail, the decorated function will not run and an error message
is sent to the Discord channel instead
"""


from ..config import *
from ..utils import find_in_list

# The first parameters of commands should be
#    message, pugs
# in that order.

def check(*args):
    """
    `args` should be a list of functions
    """
    def wrapper(function):
        # This is the function to replace the decorated function
        async def wrapped(message, pugs, user_input, client=None):
            for check in args:
                error = check(message, pugs, user_input)
                if not error == None:
                    return await message.channel.send(error)
            await function(message, pugs, user_input, client)
        return wrapped
    return wrapper


def input_too_long(message, pugs, user_input):
    if len(message.content) > 100:
        return INPUT_TOO_LONG

def already_have_pug(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    if owned_pug:
        return ALREADY_HAVE_PUG

def have_no_pug(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    if not owned_pug:
        return HAVE_NO_PUG

# You need to check `have_no_pug` before checking this
def pug_already_started(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    if owned_pug.active == PUG_STARTED:
        return PUG_ALREADY_STARTED

# You need to check `have_no_pug` before checking this
def pug_already_stopped(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    if owned_pug.active == PUG_STOPPED:
        return PUG_ALREADY_STOPPED

def already_in_pug(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if existing_pug:
        return ALREADY_IN_PUG

def not_in_pug(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if not existing_pug:
        return NOT_IN_PUG

def pug_doesnt_exist(message, pugs, user_input):
    pug_name = user_input["arguments"]
    existing_pug = find_in_list(lambda pug: pug.name == pug_name, pugs)
    if not existing_pug:
        return PUG_DOESNT_EXIST

def pug_has_no_teams(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    if not owned_pug.teams:
        return PUG_HAS_NO_TEAMS

def channels_not_picked(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    if not all(team.channel for team in owned_pug.teams):
        return CHANNELS_NOT_PICKED

def invalid_number(message, pugs, user_input):
    arguments = user_input["arguments"].split()
    # Attempt to cast the input as an int
    try:
        int(arguments[-1])
    except:
        return INVALID_NUMBER

def invalid_number_multiple(message, pugs, user_input):
    arguments = user_input["arguments"].split()
    for argument in arguments:
        try:
            int(argument)
        except:
            return INVALID_NUMBER

def invalid_range(message, pugs, user_input):
    arguments = user_input["arguments"].split()
    # Attempt to cast the input as an int
    try:
        int(arguments[0])
        int(arguments[1])
    except:
        return INVALID_NUMBER

    if int(arguments[0]) > int(arguments[1]):
        return INVALID_RANGE


# You need to check `invalid_number` before checking this
def not_enough_players(message, pugs, user_input):
    owned_pug = find_in_list(lambda pug: pug.owner == message.author, pugs)
    arguments = user_input["arguments"].split()

    # If there would be more teams than players
    if int(arguments[-1]) > len(owned_pug.players):
        return NOT_ENOUGH_PLAYERS

# You need to check `invalid_number` before checking this
def non_negative_number(message, pugs, user_input):
    arguments = user_input["arguments"].split()

    # If there would be more teams than players
    if int(arguments[-1]) <= 0:
        return NON_NEGATIVE_NUMBER

# You need to check `not_in_pug` before checking this
def team_already_exists(message, pugs, user_input):
    team_name = user_input["arguments"]
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if team_name in map(lambda team: team.name, existing_pug.teams):
        return TEAM_ALREADY_EXISTS

# You need to check `not_in_pug` before checking this
def already_in_team(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if existing_pug.find_team(message.author):
        return ALREADY_IN_TEAM

# You need to check `not_in_pug` before checking this
def not_a_captain(message, pugs, user_input):
    existing_pug = find_in_list(lambda pug: message.author in pug.players, pugs)
    if not existing_pug.is_captain(message.author):
        return NOT_A_CAPTAIN