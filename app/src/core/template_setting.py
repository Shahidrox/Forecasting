from pathlib import Path
from fastapi.templating import Jinja2Templates

templates_directory = Path(__file__).parent.parent / "admin/views"
templates = Jinja2Templates(directory=templates_directory)
