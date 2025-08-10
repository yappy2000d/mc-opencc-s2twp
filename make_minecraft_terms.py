from time import time

t = time()
print("Starting conversion...")

import requests

url_zh_cn = "https://github.com/SkyEye-FAST/mc_lang/raw/refs/heads/master/full/zh_cn.json"
url_zh_tw = "https://github.com/SkyEye-FAST/mc_lang/raw/refs/heads/master/full/zh_tw.json"

zh_cn = requests.get(url_zh_cn).json()
zh_tw = requests.get(url_zh_tw).json()

# source: https://github.com/Blackrowtw/Masa-series-mods-translation-zh_tw/tree/master?tab=readme-ov-file#%E8%87%AA%E5%AE%9A%E7%BE%A9%E8%BE%AD%E5%85%B8
patch = [
    ["揹包", "背包"],
    ["臺", "台"],
    ["映象", "鏡像"],
    ["繫結", "綁定"],
    ["公用事業", "公共項目"],
    ["整型", "整數型"],
    ["型別", "類型"],
    ["坐標", "座標"],
    ["熱鍵", "快捷鍵"],
    ["介面", "界面"]
]

written_keys = set()
with open("minecraft_terms.txt", 'w', encoding="utf-8") as f:

    for old, new in patch:
        f.write(f"{old}\t{new}\n")

    for key, cn_value in zh_cn.items():
        tw_value = zh_tw.get(key)

        if tw_value is None:
            print(f"Warning: {cn_value} not found in zh_tw.json, skipping.")
            continue

        # Escape characters
        cn_value_escaped = cn_value.replace("\t", "\\t").replace("\n", "\\n")
        tw_value_escaped = tw_value.replace("\t", "\\t").replace("\n", "\\n")

        if cn_value_escaped in written_keys:
            print(f"Duplicate key detected: {cn_value_escaped}, skipping.")
            continue

        written_keys.add(cn_value_escaped)
        f.write(f"{cn_value_escaped}\t{tw_value_escaped}\n")

from pathlib import Path
import subprocess
import opencc

# Convert .TXT to .OCD2
opencc_dir = Path(opencc.__file__).parent
opencc_dict_exe = opencc_dir / "clib" / "bin" / "opencc_dict.exe"

subprocess.run([
    opencc_dict_exe,
    "-i", "minecraft_terms.txt",
    "-o", "minecraft_terms.ocd2",
    "-f", "text",
    "-t", "ocd2"
])


print(f"Conversion completed in {time() - t:.2f} seconds.")
