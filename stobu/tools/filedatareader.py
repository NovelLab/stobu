"""File data read module."""

# Official Libraries
import copy
import yaml


# My Modules


__all__ = (
        'dump_yaml_data',
        'read_markdown_data_as_yaml',
        'read_yaml_data',
        )


# Main
def dump_yaml_data(data: dict) -> str:
    assert isinstance(data, dict)

    return yaml.safe_dump(data, default_flow_style=False)


def read_markdown_data_as_yaml(data: str) -> dict:
    assert isinstance(data, str)

    is_frontmatter = False
    tmp = {}
    yamldata = []
    mddata = []

    for line in data.split('\n'):
        _line = line.rstrip('\r\n')
        if _line == '---':
            if is_frontmatter:
                is_frontmatter = False
                if yamldata:
                    tmp.update(yaml.safe_load('\n'.join(yamldata)))
                    yamldata = []
                continue
            else:
                is_frontmatter = True
                if mddata:
                    tmp.update({'markdown': copy.deepcopy(mddata)})
                    mddata = []
                continue
        if is_frontmatter:
            yamldata.append(_line)
        elif _line:
            mddata.append(_line)
        else:
            continue
    if yamldata:
        tmp.update(yaml.safe_load('\n'.join(yamldata)))
    if mddata:
        tmp.update({'markdown': copy.deepcopy(mddata)})
    else:
        tmp.update({'markdown': []})

    return tmp


def read_yaml_data(data: str) -> dict:
    assert isinstance(data, str)

    return yaml.safe_load(data)


# Private Functions
def _rid_null_status(text: str) -> str:
    assert isinstance(text, str)

    return text.replace('null', '')
