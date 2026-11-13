#!/usr/bin/env python3
"""下载或更新本项目使用的万象简体 LTS 模型（仅依赖 Python 3 标准库）。"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import urllib.error
import urllib.request

NAME = "wanxiang-lts-zh-hans.gram"
RELEASE_URL = "https://api.github.com/repos/amzxyz/rime-wanxiang-data/releases/tags/LTS"
DESTINATION = Path(__file__).resolve().parent / NAME


def open_url(url):
    request = urllib.request.Request(url, headers={"User-Agent": "rime-gram-updater"})
    return urllib.request.urlopen(request, timeout=60)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    print("检查万象 LTS 发布信息……", flush=True)
    with open_url(RELEASE_URL) as response:
        release = json.load(response)
    asset = next((item for item in release["assets"] if item["name"] == NAME), None)
    if asset is None:
        raise ValueError(f"发布中未找到 {NAME}")
    digest = asset.get("digest") or ""
    if not re.fullmatch(r"sha256:[0-9a-fA-F]{64}", digest):
        raise ValueError("官方发布缺少有效的 SHA-256，停止更新")
    expected_hash = digest.split(":", 1)[1].lower()
    size = asset["size"]
    if not isinstance(size, int) or size <= 0:
        raise ValueError("官方发布的文件大小无效")

    if (DESTINATION.is_file() and DESTINATION.stat().st_size == size
            and sha256(DESTINATION) == expected_hash):
        print(f"已是最新模型，无需下载：{DESTINATION}")
        return

    print(f"下载 {NAME}（{size / 1024 / 1024:.1f} MiB）……", flush=True)
    temporary = None
    try:
        # 与目标文件处于同一目录，保证校验后可原子替换；失败时保留旧模型。
        with tempfile.NamedTemporaryFile(
            dir=DESTINATION.parent, prefix=NAME + ".", suffix=".part", delete=False
        ) as output:
            temporary = Path(output.name)
            downloaded = 0
            checksum = hashlib.sha256()
            with open_url(asset["browser_download_url"]) as response:
                for chunk in iter(lambda: response.read(1024 * 1024), b""):
                    downloaded += len(chunk)
                    if downloaded > size:
                        raise ValueError("下载文件超出预期大小")
                    checksum.update(chunk)
                    output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        if downloaded != size or checksum.hexdigest() != expected_hash:
            raise ValueError("模型大小或 SHA-256 校验失败")
        os.replace(temporary, DESTINATION)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    print(f"校验通过，模型已安装：{DESTINATION}")
    print("请在 Fcitx5 菜单执行“重新部署”；若旧模型仍在使用，请重启输入法。")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, urllib.error.URLError) as error:
        print(f"更新失败：{error}；现有模型未替换。", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n已取消；现有模型未替换。", file=sys.stderr)
        sys.exit(130)
