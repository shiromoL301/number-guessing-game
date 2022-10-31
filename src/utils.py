def into_speech_bubble(msg: str) -> str:
    """文字列を吹き出しで囲む

    Args:
        msg (str): 表示したい文字列

    Returns:
        str: 吹き出しで囲んだ文字列
    """
    length = 2 * len(msg)
    buffer = ["＿人"]
    for _ in range(length // 2):
        buffer.append("人")
    buffer.append(f"人＿\n＞  {msg}  ＜\n￣^Y")
    for _ in range(length // 2):
        buffer.append("^Y")
    buffer.append("^Y￣")

    return "".join(buffer)