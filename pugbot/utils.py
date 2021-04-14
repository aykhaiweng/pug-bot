from discord import Embed
from .consts import PugStatus, PREFIX

async def create_embed(pug, title=None, description=None, status=None):
    """
    Creates that neat Discord embed
    """
    if not status:
        status = pug.status
    
    color = status.value['color']
    footer_text = status.value['footer_message']

    # Create the initial embed
    embed = Embed(
        title=title or pug.name,
        description=f"Type `{PREFIX}join \"{pug.name}\"` to join this lobby",
        type="rich",
        color=color,
        footer_text=footer_text
    )

    # Set the author of the embed
    embed.set_author(
        name=pug.owner.name,
        icon_url=pug.owner.avatar_url
    )

    # Player count
    embed.add_field(
        name="Player Count",
        value=f"{len(pug.players)}/{pug.max_size}"
    )


    # Team list

    # Player list

    return embed