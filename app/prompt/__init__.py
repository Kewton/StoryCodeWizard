from app.util.codeopen import fetch_libraryfiles_and_contents, fetch_files_and_contents
from app.prompt.nextjstemplate1 import nextjstemplate1
from app.prompt.nextjstemplate2 import nextjstemplate2
from app.prompt.fastAPItemplate import fastAPItemplate
from app.prompt.streamlitTemplate import streamlitTemplate
from app.prompt.default import default


def createPromt(_systemrole_content, _input):
    _prerequisites = _systemrole_content["prerequisites"]

    _libraryFileList = []
    for a in _systemrole_content["libraryFileList"]:
        _libraryFileList.append(_systemrole_content["pjdir"] + "/" + a)
    _src_root_path = _systemrole_content["pjdir"]

    _ignorelist = _systemrole_content["ignorelist"]

    if "nextjstemplate1" == _systemrole_content["prompt"]:
        return nextjstemplate1(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    elif "nextjstemplate2" == _systemrole_content["prompt"]:
        return nextjstemplate2(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    elif "fastAPItemplate" == _systemrole_content["prompt"]:
        return fastAPItemplate(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    if "streamlitTemplate" == _systemrole_content["prompt"]:
        return streamlitTemplate(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)
    else:
        return default(_prerequisites, _input, _libraryFileList, _src_root_path, _ignorelist)