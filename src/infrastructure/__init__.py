from colorama import init
from os import name

if name.lower() == "windows":
    init(convert=True)
