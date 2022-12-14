
def string_trim(message, max_size=40):
    if len(message) > max_size:
        return message[:max_size] + "..."
    else:
        return message
