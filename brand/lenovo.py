from util.request import send, download
import json
from typing import Dict, List
from util.prompt import list


def search_model(model: str):
    model_data = json.loads(
        send(f"https://newsupport.lenovo.com.cn/api/drive/like/{model}?limit=1000")
    )
    model_data = model_data["data"]
    if model_data == {"\x00*\x00items": []}:
        return 1
    choices: Dict[str, str] = {}
    for i in model_data:
        choices[i] = i
    model = list("选择型号", choices)
    search_id(model)


def search_id(model: str):
    data = json.loads(
        send(
            f"https://newsupport.lenovo.com.cn/api/drive/drive_query?searchKey={model}"
        )
    )
    id = data["data"][0]["categoryid"]
    download_driver(id)


def download_driver(id: str):
    osid = list("选择操作系统", {"Windows 10": 42, "Windows 11": 248})
    data = json.loads(
        send(
            f"https://newsupport.lenovo.com.cn/api/drive/drive_listnew?searchKey={id}&sysid={osid}"
        )
    )
    data = data["data"]["partList"]
    driver_list: Dict[str, List[List[str]]] = {}
    for i in data:
        driver_list_temp: List[List[str]] = []
        for j in i["drivelist"]:
            name = f"{j["DriverName"]} V{j["Version"]}"
            url = j["FilePath"]
            driver: List[str] = [name, url]
            driver_list_temp.append(driver)
        driver_list[i["PartName"]] = driver_list_temp
    driver = list("选择驱动类型", driver_list)
    choices: Dict[str, str] = {}
    for i in driver:
        choices[i[0]] = i[1]
    url = list("选择驱动", choices, True)
    download(url[1], url[0])
