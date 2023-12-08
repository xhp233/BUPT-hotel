@echo off

setlocal enabledelayedexpansion

for %%A in (serverApp managerApp ACPanelApp BUPTHotelAC) do (
    for %%B in (%%A\__pycache__\* %%A\migrations\__pycache__\* %%A\migrations\*) do (
        if not "%%~nxB"=="__init__.py" (
            del "%%B"
        )
    )
    rd %%A\__pycache__
    rd %%A\migrations\__pycache__
)

del BUPTHotelAC.db