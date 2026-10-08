import sys
import os
import importlib
import subprocess

# 巨大な整数を文字列へ変換するときの制限を解除
sys.set_int_max_str_digits(0)

PLUGIN_DIR = "plugins"


def load_plugins():
    """pluginsフォルダからプラグインを読み込む"""

    plugins = []

    for filename in os.listdir(PLUGIN_DIR):

        if not filename.endswith(".py"):
            continue

        if filename == "__init__.py":
            continue

        module_name = filename[:-3]

        try:
            module = importlib.import_module(
                f"{PLUGIN_DIR}.{module_name}"
            )

            if (
                hasattr(module, "PLUGIN_NAME")
                and hasattr(module, "calculate")
            ):
                plugins.append(module)

        except Exception as e:
            print(f"プラグイン読み込み失敗: {filename}")
            print(e)

    return plugins


def select_plugin(plugins):
    """プラグインを選択する"""

    print()
    print("=== 計算プラグイン ===")
    print()

    for i, plugin in enumerate(plugins, 1):
        print(f"{i}. {plugin.PLUGIN_NAME}")

    print()

    while True:

        try:
            choice = int(
                input("プラグインを選択してください > ")
            )

            if 1 <= choice <= len(plugins):
                return plugins[choice - 1]

            print("その番号はありません。")

        except ValueError:
            print("数字を入力してください。")


def copy_to_clipboard(text):
    """Windowsのクリップボードへコピー"""

    process = subprocess.Popen(
        ["clip"],
        stdin=subprocess.PIPE,
        text=True
    )

    process.communicate(text)


def main():

    plugins = load_plugins()

    if not plugins:
        print("利用できるプラグインがありません。")
        return

    plugin = select_plugin(plugins)

    print()
    print(f"選択: {plugin.PLUGIN_NAME}")
    print()

    value = input("数値を入力してください > ")

    try:

        result = plugin.calculate(value)

        print()
        print("=== 結果 ===")
        print(result)

        print()
        print("c : 結果をコピー")
        print("Enter : 終了")

        command = input("> ").strip().lower()

        if command == "c":

            copy_to_clipboard(str(result))

            print(
                "結果をクリップボードにコピーしました。"
            )

    except Exception as e:

        print()
        print("計算エラー:")
        print(e)


if __name__ == "__main__":
    main()