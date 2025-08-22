import os

def get_inputFolder_path() -> str:
    base_dir = os.getcwd()
    inputFolder_path = os.path.abspath(os.path.join(base_dir, 'preprocessed_md'))
    return inputFolder_path

def get_md_list(inputFolder_path: str) -> list[str]:
    md_files = [f for f in os.listdir(inputFolder_path) if f.endswith('.md')]
    return md_files

def get_markdown_content(inputFolder_path: str, md_files: list[str]) -> list[dict]:
    md_contents = []
    i = 1
    for md_file in md_files:
        with open(os.path.join(inputFolder_path, md_file), 'r', encoding='utf-8') as f:
            content = f.read()
            md_contents.append(
                {
                    'Page': f'Page {i}',
                    'content': content
                }
            )
            i += 1
    return md_contents

def get_md_content() -> list[dict]:
    inputFolder_path = get_inputFolder_path()
    md_files = get_md_list(inputFolder_path=inputFolder_path)
    md_contents = get_markdown_content(inputFolder_path=inputFolder_path, md_files=md_files)
    return md_contents