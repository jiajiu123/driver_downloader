import requests
from typing import Optional, Dict, Any, Union
import tqdm


def send(
    url: str,
    headers: Dict[str, Any] = {},
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    is_file: bool = False,
    method: str = "GET",
) -> Optional[Union[bytes, str]]:
    """
    发送HTTP请求的通用函数

    Args:
        url: 请求URL
        headers: 请求头字典
        params: URL参数
        data: 请求体数据
        is_file: 是否为文件下载
        method: HTTP方法（默认GET）

    Returns:
        响应内容的字节数据或None（如果失败）
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
        stream=True if is_file else False,
    )
    response.raise_for_status()  # 抛出HTTP错误
    if is_file:
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
        return file_data
    else:
        return response.text
