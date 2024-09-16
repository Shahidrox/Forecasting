import pytz

def convert_to_ist(timestamp: str):
    """
    Convert a timestamp to JST timezone.

    Args:
        timestamp: The timestamp to convert.

    Returns:
        The converted timestamp.

    """
    jst = pytz.timezone('Asia/Tokyo')

    return timestamp.astimezone(jst)
  