import os
import json
import sys


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

PLUGIN_DIR = os.path.join(
    ROOT_DIR,
    "plugins"
)

DOCS_DIR = os.path.join(
    ROOT_DIR,
    "docs"
)


def load_plugins():

    plugins = []

    if not os.path.exists(PLUGIN_DIR):
        return plugins

    for filename in sorted(os.listdir(PLUGIN_DIR)):

        if not filename.endswith(".py"):
            continue

        if filename == "__init__.py":
            continue

        path = os.path.join(
            PLUGIN_DIR,
            filename
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            source = f.read()

        plugins.append({
            "filename": filename,
            "source": source
        })

    return plugins


def create_docs():

    os.makedirs(
        DOCS_DIR,
        exist_ok=True
    )

    plugins = load_plugins()

    print(
        f"{len(plugins)}個のプラグインを検出しました。"
    )

    for plugin in plugins:

        print(
            f"  - {plugin['filename']}"
        )

    create_html(plugins)
    create_css()
    create_js(plugins)

    print()
    print("Web版を生成しました。")
    print()
    print(
        f"出力先: {DOCS_DIR}"
    )


def create_html(plugins):

    html = """<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>計算プラグイン</title>

    <link
        rel="stylesheet"
        href="style.css"
    >
</head>

<body>

<div class="container">

    <h1>計算プラグイン</h1>

    <div id="status">
        Pythonを読み込んでいます...
    </div>

    <section>

        <label for="plugin">
            プラグイン
        </label>

        <select id="plugin">
        </select>

    </section>

    <section>

        <label for="input">
            数値
        </label>

        <input
            id="input"
            type="text"
            inputmode="numeric"
            placeholder="数値を入力"
        >

    </section>

    <button
        id="calculate"
        disabled
    >
        計算
    </button>

    <section>

        <label>
            結果
        </label>

        <textarea
            id="result"
            readonly
            placeholder="ここに結果が表示されます"
        ></textarea>

    </section>

    <button
        id="copy"
        disabled
    >
        コピー
    </button>

    <div id="message"></div>

</div>

<script src="https://cdn.jsdelivr.net/pyodide/v0.28.2/full/pyodide.js"></script>

<script src="app.js"></script>

</body>
</html>
"""

    path = os.path.join(
        DOCS_DIR,
        "index.html"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)


def create_css():

    css = r"""
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 20px;

    background: #f5f5f5;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

.container {
    width: 100%;
    max-width: 600px;

    margin: 0 auto;

    background: white;

    padding: 24px;

    border-radius: 16px;

    box-shadow:
        0 4px 20px rgba(0, 0, 0, 0.08);
}

h1 {
    margin-top: 0;

    text-align: center;

    font-size: 28px;
}

#status {
    padding: 12px;

    margin-bottom: 20px;

    border-radius: 8px;

    background: #eeeeee;

    text-align: center;

    font-size: 14px;
}

section {
    margin-bottom: 18px;
}

label {
    display: block;

    margin-bottom: 8px;

    font-weight: bold;
}

select,
input,
textarea {
    width: 100%;

    padding: 14px;

    border: 1px solid #cccccc;

    border-radius: 10px;

    font-size: 16px;

    background: white;
}

textarea {
    min-height: 160px;

    resize: vertical;

    font-family: monospace;
}

button {
    width: 100%;

    padding: 14px;

    margin-bottom: 12px;

    border: none;

    border-radius: 10px;

    background: #222;

    color: white;

    font-size: 17px;

    font-weight: bold;

    cursor: pointer;
}

button:disabled {
    opacity: 0.45;

    cursor: not-allowed;
}

#message {
    min-height: 24px;

    margin-top: 8px;

    text-align: center;

    font-size: 14px;
}

@media (max-width: 480px) {

    body {
        padding: 10px;
    }

    .container {
        padding: 18px;

        border-radius: 12px;
    }

    h1 {
        font-size: 24px;
    }

    textarea {
        min-height: 130px;
    }
}
"""

    path = os.path.join(
        DOCS_DIR,
        "style.css"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(css)


def create_js(plugins):

    plugin_data = json.dumps(
        plugins,
        ensure_ascii=False
    )

    js = f"""
const PLUGINS = {plugin_data};

let pyodide = null;
let ready = false;


const statusElement =
    document.getElementById("status");

const pluginElement =
    document.getElementById("plugin");

const inputElement =
    document.getElementById("input");

const resultElement =
    document.getElementById("result");

const calculateButton =
    document.getElementById("calculate");

const copyButton =
    document.getElementById("copy");

const messageElement =
    document.getElementById("message");


function showMessage(text) {{

    messageElement.textContent = text;

}}


function setupPlugins() {{

    pluginElement.innerHTML = "";

    for (
        let i = 0;
        i < PLUGINS.length;
        i++
    ) {{

        const option =
            document.createElement("option");

        option.value = i;

        option.textContent =
            PLUGINS[i].filename;

        pluginElement.appendChild(option);
    }}

}}


async function loadPython() {{

    try {{

        statusElement.textContent =
            "Pythonを読み込んでいます...";

        pyodide = await loadPyodide();

        // 巨大整数の文字列変換制限を解除
        await pyodide.runPythonAsync(`
import sys
sys.set_int_max_str_digits(0)
`);

        setupPlugins();

        ready = true;

        calculateButton.disabled = false;

        statusElement.textContent =
            "Python準備完了";

    }} catch (error) {{

        console.error(error);

        statusElement.textContent =
            "Pythonの読み込みに失敗しました";

        showMessage(
            error.toString()
        );
    }}

}}


async function calculate() {{

    if (!ready) {{
        return;
    }}

    const input =
        inputElement.value.trim();

    if (input === "") {{

        showMessage(
            "数値を入力してください。"
        );

        return;
    }}

    const index =
        Number(pluginElement.value);

    const plugin =
        PLUGINS[index];

    if (!plugin) {{

        showMessage(
            "プラグインが見つかりません。"
        );

        return;
    }}

    calculateButton.disabled = true;

    copyButton.disabled = true;

    resultElement.value = "";

    showMessage(
        "計算しています..."
    );

    try {{

        // Pythonプラグインを読み込む
        await pyodide.runPythonAsync(
            plugin.source
        );

        // Pythonのcalculate()を呼び出す
        pyodide.globals.set(
            "web_input",
            input
        );

        const result =
            await pyodide.runPythonAsync(`
result = calculate(web_input)
str(result)
`);

        resultElement.value =
            result;

        copyButton.disabled = false;

        showMessage(
            "計算完了"
        );

    }} catch (error) {{

        console.error(error);

        showMessage(
            "計算エラー: " +
            error.toString()
        );

    }} finally {{

        calculateButton.disabled = false;

    }}

}}


async function copyResult() {{

    const text =
        resultElement.value;

    if (!text) {{
        return;
    }}

    try {{

        await navigator.clipboard.writeText(
            text
        );

        showMessage(
            "結果をコピーしました。"
        );

    }} catch (error) {{

        // 古いブラウザ向け
        resultElement.focus();

        resultElement.select();

        document.execCommand("copy");

        showMessage(
            "結果をコピーしました。"
        );
    }}

}}


calculateButton.addEventListener(
    "click",
    calculate
);


copyButton.addEventListener(
    "click",
    copyResult
);


inputElement.addEventListener(
    "keydown",
    function(event) {{

        if (
            event.key === "Enter"
        ) {{
            calculate();
        }}

    }}
);


loadPython();
"""

    path = os.path.join(
        DOCS_DIR,
        "app.js"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(js)


if __name__ == "__main__":

    create_docs()