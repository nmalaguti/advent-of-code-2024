from pathlib import Path
from shutil import copyfile

from invoke import task


@task
def new_day(c):
    curr_dir = Path(__file__).parent
    last_day = next(reversed(sorted(list(curr_dir.glob("day_*")))), None)
    if last_day is None:
        next_day = 1
    else:
        next_day = int(last_day.name[4:]) + 1
    next_day_dir = curr_dir / f"day_{next_day:02d}"
    next_day_dir.mkdir()
    (next_day_dir / "__init__.py").touch()
    copyfile(curr_dir / "template.py", next_day_dir / f"day_{next_day:02d}.py")
    (next_day_dir / "input").touch()
    (next_day_dir / "example").touch()
