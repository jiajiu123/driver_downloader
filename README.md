# ASUS
## 搜索型号
https://odinapi.asus.com.cn/apiv2/SearchSuggestion?SystemCode=asus&WebsiteCode=cn&SearchKey={型号}&SearchType=ProductsAll&RowLimit=1000

所有参数都是必须的，SearchKey 代表搜索关键字，其他参数均为固定值，在返回的 json 文件中解析的 DataId 即为产品 id
## 获取驱动
https://www.asus.com.cn/support/webapi/ProductV2/GetPDDrivers?website=cn&osid={osid}&pdid={pdid}

osid=52 为 win11，osid=45 为 win10，pdid 对应之前的 DataId

Result→Obj→Name 为驱动类型

Result→Obj→Files→{}→DownloadUrl→China 为下载链接

# Lenovo
## 搜索型号
https://newsupport.lenovo.com.cn/api/drive/like/{型号}?limit=50

data 数组内含所有型号
## 获取 id
https://newsupport.lenovo.com.cn/api/drive/drive_query?searchKey={完整型号}

完整型号在上方返回中获取
## 获取驱动
https://newsupport.lenovo.com.cn/api/drive/drive_listnew?searchKey={id}{&sysid=42}

id 上方返回中获取，sysid=42 代表 win10 系统，不加默认 win10，sysid=248 代表 win11 系统

data→partList→drivelist→DriverName 为驱动名称

data→partList→drivelist→FilePath 为驱动下载链接
# DELL
## 搜索型号
https://www.dell.com/support/search/njs/SearchAutosuggestProductDetails_cn_zh.js

下载此 js，删掉前 37 个字符和最后一个，解析为 json，提取出 PC 值，用 PC 值替换下方型号
## 获取驱动
https://www.dell.com/support/driver/zh-cn/ips/api/driverlist/packdriversbyproduct?productcode={型号}&oscode={系统版本}
```
import requests
params = {
    'productcode': 'latitude-5420-laptop',
    #'oscode': 'W2021'#win11
    #'oscode': 'WT64A'#win10
}
response = requests.get(
    'https://www.dell.com/support/driver/zh-cn/ips/api/driverlist/packdriversbyproduct',
    params=params,
    headers={'x-requested-with': 'XMLHttpRequest'}
)
str=response.text
str_encrypt=""
for letter in str:
    if "a"<=letter<="z":
        str_encrypt +=chr((ord(letter)-ord("a") -3) %26 +ord("a"))
    elif "A"<=letter<="Z":
        str_encrypt +=chr((ord(letter)-ord("A") -3) %26 +ord("A"))
    else:
        str_encrypt += letter
print("密文为：",str_encrypt)
```
使用此脚本获取 driverlist

DriverListData→{}→CatName 为驱动类型

DriverListData→{}→FileFormats 内含有 LW64 为 64 位

DriverListData→{}→FileFrmtInfo→HttpFileLocation 为下载链接
# HP
## 搜索型号
https://support.hp.com/typeahead?q={机型}&filters=class:(pm_name_value)

productname 为产品型号，productId 对应下文 productSeriesOid

### 使用服务编号搜索
如型号未搜索到
`{"message": "Error 404, no such match found"}`，则使用服务编号搜索
```
import requests

params = {
    'q': '{服务编号}',
    'context': 'swd'
}
response = requests.get('https://support.hp.com/wcc-services/searchresult/cn-zh', params=params, headers={'referer': 'https://support.hp.com/cn-zh/drivers/desktops'})
print(response.text)
```
data→verifyResponse→data→productSeriesOID

## 获取驱动
```
import requests

json_data = {
    'productLineCode': 'DG',
    'lc': 'zh',
    'cc': 'cn',
    #'osTMSId': '792898937266030878164166465223921', #win10
    #'osTMSId': "1117042031711110499111149613201312551119131", #win11
    'osName': "Windows",
    'productSeriesOid': {productSeriesOid},
}

response = requests.post(
    'https://support.hp.com/wcc-services/swd-v2/driverDetails',
    json=json_data,
)
print(response.text)
```
data→softwareTypes→{}→accordionName 驱动类型

data→softwareTypes→{}→softwareDriversList→{}→title 驱动名

data→softwareTypes→{}→softwareDriversList→{}→fileUrl 驱动链接