from curl_cffi import requests
import tqdm
import re


def send(url, headers={}, params=None, data=None, method=["GET"]):
    """
    发送HTTP请求的通用函数

    Args:
        url: 请求URL
        headers: 请求头字典
        params: URL参数
        data: 请求体数据
        method: HTTP方法（默认GET）

    Returns:
        响应内容的字符串
    """
    ua = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    headers.update(ua)
    response = requests.request(method, url, headers=headers, params=params, data=data)
    response.raise_for_status()  # 抛出HTTP错误
    return response.text


def download(url, name, headers={}, params=None, data=None, method=["GET"]):
    """
    下载文件并保存到本地

    Args:
        url: 请求URL
        name: 文件名
        headers: 请求头字典
        params: URL参数
        data: 请求体数据
        method: HTTP方法（默认GET）
    """
    ua = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }
    headers.update(ua)
    response = requests.request(
        method,
        url,
        headers=headers,
        params=params,
        data=data,
        stream=True,
    )
    response.raise_for_status()  # 抛出HTTP错误

    # 获取文件总大小
    total_size = int(response.headers.get("content-length", 0))

    # 使用tqdm显示下载进度
    progress_bar = tqdm.tqdm(
        total=total_size, unit="B", unit_scale=True, desc="下载文件"
    )

    file_data = bytes()
    for chunk in response.iter_content(chunk_size=65536):
        if chunk:
            file_data += chunk
            progress_bar.update(len(chunk))

    progress_bar.close()
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    name = re.sub(rstr, "_", name)
    with open(name + ".exe", "wb") as f:
        f.write(file_data)
