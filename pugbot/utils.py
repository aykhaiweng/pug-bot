import re

tag_regex = re.compile(r'^\<\@\!(?P<user_id>[.0-9]+)\>$')


def tag_user_id(user_id):
    """
    Returns the user_id as a tag: <@!user_id>
    """
    return f'<@!{user_id}>'


def untag_user_id(tag):
    """
    Returns the tag as a user_id
    """
    match = tag_regex.search(tag)
    print(match)