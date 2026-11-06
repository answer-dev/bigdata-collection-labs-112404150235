from pathlib import Path
import re

import requests


def get_html(url, params):
    """发送请求，返回网页源代码。"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/130.0.0.0 Safari/537.36"
        )
    }

    # ② 发送请求并获得响应
    response = requests.get(
        url, params=params, headers=headers, timeout=10
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return response.text


def save_html(path, html):
    """将网页源代码保存为 UTF-8 文件。"""
    # 将网页中的字符编码声明同步修改为 UTF-8
    html = re.sub(
        r"""(<meta\b[^>]*\bcharset\s*=\s*["']?)[\w-]+""",
        r"\g<1>utf-8",
        html,
        flags=re.IGNORECASE,
    )

    # ③ 将响应保存到本地 HTML
    with open(path, "w", encoding="utf-8") as file:
        file.write(html)


if __name__ == "__main__":
    try:
        phone = input("请输入自己的11位手机号：").strip()

        if not (
            len(phone) == 11
            and phone.isascii()
            and phone.isdigit()
            and phone.startswith("1")
        ):
            raise ValueError("请输入以1开头的11位数字手机号")

        # ① 定义请求信息
        url = "https://www.ip138.com/mobile.asp"
        params = {
            "mobile": phone,
            "action": "mobile",
        }

        html = get_html(url, params)
        print("返回的网页源代码：")
        print(html)

        html_path = Path(__file__).resolve().parent / "phone_result.html"
        save_html(html_path, html)

        print("网页已保存到：", html_path)
        print("请在浏览器中打开文件，核对手机号和归属地。")

    except (requests.RequestException, OSError, ValueError) as error:
        print("执行失败：", error)