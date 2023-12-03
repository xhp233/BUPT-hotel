@echo off

for %%A in (serverApp\__pycache__\*) do (
    del "%%A"
)
rd serverApp\__pycache__

for %%A in (serverApp\migrations\__pycache__\*) do (
    del "%%A"
)
rd serverApp\migrations\__pycache__

for %%A in (serverApp\migrations\*) do (
    if not "%%~nxA"=="__init__.py" (
        del "%%A"
    )
)

for %%A in (managerApp\__pycache__\*) do (
    del "%%A"
)
rd managerApp\__pycache__

for %%A in (managerApp\migrations\__pycache__\*) do (
    del "%%A"
)
rd managerApp\migrations\__pycache__

for %%A in (managerApp\migrations\*) do (
    if not "%%~nxA"=="__init__.py" (
        del "%%A"
    )
)

for %%A in (ACPanelApp\__pycache__\*) do (
    del "%%A"
)
rd ACPanelApp\__pycache__

for %%A in (ACPanelApp\migrations\__pycache__\*) do (
    del "%%A"
)
rd ACPanelApp\migrations\__pycache__

for %%A in (ACPanelApp\migrations\*) do (
    if not "%%~nxA"=="__init__.py" (
        del "%%A"
    )
)

for %%A in (BUPTHotelAC\__pycache__\*) do (
    del "%%A"
)
rd BUPTHotelAC\__pycache__

del software_engineering

python manage.py makemigrations
python manage.py migrate
python manage.py runserver