from cx_Freeze import *

# On appelle la fonction setup
setup(
    name = "sport",
    version = "1",
    description = "test",
    executables = [Executable("main.py")],
)
