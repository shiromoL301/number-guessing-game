def into_speech_bubble(msg: str) -> str:
    length = 2 * len(msg)
    buffer = ["＿人"]
    for _ in range(length // 2):
        buffer.append("人")
    buffer.append(f"人＿\n＞  {msg}  ＜\n￣^Y")
    for _ in range(length // 2):
        buffer.append("^Y")
    buffer.append("^Y￣")

    return "".join(buffer)