# tests/test_files.py
from src.compute_complexity import get_python_files
def test_python_file_filter():

    files = "main.py;test.js;model.py"

    result = get_python_files(files)

    assert result == [
        "main.py",
        "model.py"
    ]