from util.request import send
import json
from typing import Dict, List
from util.prompt import list


def search_model(model: str):
    model_data = json.loads(
        send(f"https://newsupport.lenovo.com.cn/api/drive/like/{model}?limit=1000")
    )
    model_data = model_data["data"]
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
    select_driver(id)


def select_driver(id: str):
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
    download_driver(url[1], url[0])


def download_driver(url: str, name: str):
    with open(name + ".exe", "wb") as f:
        f.write(send(url, is_file=True))  # type: ignore
