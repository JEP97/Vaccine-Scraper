import sys
from cx_Freeze import setup, Executable

# setup files required to run cx_Freeze

base = None

if sys.platform == 'Win32':
    base = 'Win32Gui'

exe = Executable("Scraper.py", base=base)

setup(
    name="Vaccine Scraper",
    options={"build.exe": {"packages": [""]}},
    version="1.1",
    description="A program to scrape vaccine appointment availability in York region",
    executables=[exe],
    requires=['beautifulsoup4', 'schedule', 'requests']
)
