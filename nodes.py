# ──────────────────────────
# comfyui-sequential-prompt
# ──────────────────────────
import os
import glob
import json
import folder_paths
from pathlib import Path
from server import PromptServer
from aiohttp import web
from .protcol import log


@PromptServer.instance.routes.get("/YokoYokoTEC/LinRead/{name}")
async def GetFile(request):
    name = request.match_info["name"]
    log(name)
    path = folder_paths.get_input_directory()
    if name == "output":
        path = folder_paths.get_output_directory()
    # ──────────────────────────
    path = path + "/**/*.txt"
    recursive = "/**/" in path
    log(path)
    # ──────────────────────────
    pre = path
    pre = pre.replace("/**/", "/")
    pre = os.path.abspath(pre)
    pre = os.path.split(pre)[0]
    log(pre)
    # ──────────────────────────
    files = list(map(lambda t: os.path.relpath(t, pre),
                     glob.glob(path, recursive=recursive)))
    # ──────────────────────────
    if len(files) == 0:
        files = ["[none]"]
    return web.json_response(files)


def is_child_dir(parent_path, child_path):
    parent_path = os.path.abspath(parent_path)
    child_path = os.path.abspath(child_path)
    return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])


def get_file(dir, file):
    if file == "[none]" or not file or not file.strip():
        raise ValueError("No file")
    # ──────────────────────────
    root_dir = folder_paths.get_input_directory()
    if dir == "output":
        root_dir = folder_paths.get_output_directory()
    root_dir = root_dir+'/'
    # ──────────────────────────
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    full_path = os.path.join(root_dir, file)

    if not is_child_dir(root_dir, full_path):
        raise ReferenceError()

    return full_path


class BatchCounter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "count": ("INT", {"default": 1}),
                "seed": ("INT", {"default": 0, "min": 0})
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "main"
    CATEGORY = "YokoYoko.Tec"

    def main(self, count,  seed):
        return (seed % count,)


class LineRead:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "line": ("INT", {"default": 1}),
                "path": (["input", "output"], {}),
                "file": (["[none]"], {})
            },
        }

    @classmethod
    def VALIDATE_INPUTS(self, path, file, **kwargs):
        if file == "[none]" or not file or not file.strip():
            return True
        get_file(path, file)
        return True

    @classmethod
    def IS_CHANGED(self, **kwargs):
        self.file = get_file(kwargs["path"], kwargs["file"])
        return os.path.getmtime(self.file)

    RETURN_TYPES = ("STRING",)
    FUNCTION = "main"
    CATEGORY = "YokoYoko.Tec"

    def main(self, **kwargs):
        print("%s, %s, %d" % (kwargs["path"], kwargs["file"], kwargs["line"]))
        self.file = get_file(kwargs["path"], kwargs["file"])
        with open(self.file, "r") as f:
            lines = f.read().splitlines()
        # ──────────────────────────
        index = kwargs["line"]
        size = int(len(lines))
        while index >= size:
            index = index - size
        return (lines[index],)


# --------------------------------------------------------------------------------
NODE_CLASS_MAPPINGS = {
    "BatchCounter|YokoYokoTEC": BatchCounter,
    "LineRead|YokoYokoTEC": LineRead,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BatchCounter|YokoYokoTEC": "BatchCounter",
    "LineRead|YokoYokoTEC": "LineRead",
}
