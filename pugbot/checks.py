def check(*list_of_checks):
    """
    `args` should be a list of functions
    """
    def wrapper(function):
        # This is the function to replace the decorated function
        async def wrapped(message, pugs, user_input, client=None):
            for check in list_of_checks:
                error = check(message, pugs, user_input)
                if not error == None:
                    return await message.channel.send(error)
            await function(message, pugs, user_input, client)
        return wrapped
    return wrapper