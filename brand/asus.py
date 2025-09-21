from util.request import send
import json
import unicodedata
from typing import Dict, List
from util.prompt import list


def search_model(model: str):
    model_data = json.loads(
        send(
            f"https://odinapi.asus.com.cn/apiv2/SearchSuggestion?SystemCode=asus&WebsiteCode=cn&SearchKey={model}&SearchType=ProductsAll&RowLimit=1000"
        )
    )
    model_data = model_data["Result"][0]["Content"]
    choices: Dict[str, str] = {}
    for i in model_data:
        if i["DataId"] != "99999":
            choices[i["Title"]] = i["DataId"]

    model = list("选择型号", choices)
    select_driver(model)


def select_driver(model_id: str):
    osid = list("选择操作系统", {"Windows 10": 45, "Windows 11": 52})
    data = json.loads(
        send(
            f"https://www.asus.com.cn/support/webapi/ProductV2/GetPDDrivers?website=cn&osid={osid}&pdid={model_id}"
        )
    )
    data = data["Result"]["Obj"]
    driver_list: Dict[str, List[List[str]]] = {}
    for i in data:
        driver_list_temp: List[List[str]] = []
        for j in i["Files"]:
            url = j["DownloadUrl"]["China"]
            name = f"{j['Title']} {j['Version']}"
            name = unicodedata.normalize("NFKC", name)
            driver: List[str] = [name, url]
            if "microsoft" not in url:
                driver_list_temp.append(driver)
        driver_list[i["Name"]] = driver_list_temp
    driver = list("选择驱动类型", driver_list)
    choices: Dict[str, str] = {}
    for i in driver:
        choices[i[0]] = i[1]
    url = list("选择驱动", choices, True)
    download_driver(url[1], url[0])


def download_driver(url: str, name: str):
    token = send(
        f"https://cdnta.asus.com.cn/api/v1/Token?filePath={url}&systemCode=asus",
        method="POST",
        headers={"origin": "https://www.asus.com.cn"},
    )
    token = json.loads(token)["result"]
    st = token["st"]
    e = token["e"]

    with open(name + ".exe", "wb") as f:
        f.write(send(f"https://dlcdnta.asus.com.cn/{url}?st={st}&e={e}", is_file=True))# type: ignore
