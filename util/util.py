def string_trim(message, max_size=30):
    if len(message) > max_size:
        return message[:max_size] + "..."
    else:
        return message


def merge_array_of_arrays(array_of_arrays):
    merged_array = []

    for array in array_of_arrays:
        merged_array.extend(array)

    return merged_array
