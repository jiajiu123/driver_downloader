from util.prompt import list, input
from noneprompt import CancelledError
import importlib
import sys


def main():

    while True:
        try:
            # 品牌选择
            brand = list(
                "选择品牌",
                {
                    "华硕": "brand.asus",
                    "联想（未完成）": "brand.lenovo",
                    "戴尔（未完成）": "brand.dell",
                    "惠普（未完成）": "brand.hp",
                },
            )

            # 型号输入
            model = input("输入型号或服务编码（仅HP支持服务编码）")

            if not model.strip():
                print("错误：型号不能为空")
                continue
            if len(model) < 3:
                print("错误：型号长度不能小于3个字符")
                continue
            break
        except KeyboardInterrupt:
            print("已取消")

        except CancelledError:
            continue
        except Exception as e:
            print(f"发生错误：{e}")
            sys.exit(1)
    # 动态导入并执行
    module = importlib.import_module(brand)
    func = getattr(module, "search_model")
    func(model)


if __name__ == "__main__":
    main()
