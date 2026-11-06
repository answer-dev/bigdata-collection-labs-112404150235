from pathlib import Path
from urllib.parse import urlsplit

import requests


def get_image(url):
    """获取图片的二进制数据。"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if not content_type.lower().startswith("image/"):
        raise ValueError("返回的内容不是图片")

    if not response.content:
        raise ValueError("图片数据为空")

    return response.content


def save_image(path, content):
    """将图片数据保存到文件。"""
    with open(path, "wb") as file:
        file.write(content)


if __name__ == "__main__":
    url_list = [
        "https://www.bspider.top/static/yh31/images/202103302056530751.gif",
        "https://www.bspider.top/static/yh31/images/202008242134566465.gif",
    ]

    save_dir = Path(__file__).resolve().parent / "images"
    save_dir.mkdir(exist_ok=True)
    success_count = 0

    for index, url in enumerate(url_list, start=1):
        try:
            content = get_image(url)
            file_name = Path(urlsplit(url).path).name or f"image_{index}.gif"
            image_path = save_dir / file_name

            save_image(image_path, content)
            success_count += 1
            print("下载成功：", image_path)

        except (requests.RequestException, OSError, ValueError) as error:
            print("下载失败：", url)
            print("原因：", error)

    print(f"完成：成功 {success_count} 张，失败 {len(url_list) - success_count} 张")