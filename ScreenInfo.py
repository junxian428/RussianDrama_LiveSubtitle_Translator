from screeninfo import get_monitors

for m in get_monitors():
    print(f"Monitor: {m.name}, Width: {m.width}, Height: {m.height}, X: {m.x}, Y: {m.y}")
