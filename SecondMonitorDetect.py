from screeninfo import get_monitors

# Find the right-most monitor (biggest X)
monitor = max(get_monitors(), key=lambda m: m.x)
region = (monitor.x, monitor.y, monitor.width, monitor.height)

print("Capturing region:", region)
