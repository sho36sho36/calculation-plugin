import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(ROOT_DIR, "plugins")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")


def load_plugins():
    plugins = []

    for filename in sorted(os.listdir(PLUGIN_DIR)):
        if not filename.endswith(".py"):
            continue

        if filename == "__init__.py":
            continue

        path = os.path.join(PLUGIN_DIR, filename)

        with open(path, "r", encoding="utf-8") as f:
            source = f.read()

        name = filename
        description = "このプラグインの説明はありません。"

        # PLUGIN_NAME を取得
        for line in source.splitlines():
            line = line.strip()

            if line.startswith("PLUGIN_NAME"):
                try:
                    name = line.split("=", 1)[1].strip().strip('"\'')
                except Exception:
                    pass

            if line.startswith("PLUGIN_DESCRIPTION"):
                try:
                    description = line.split("=", 1)[1].strip().strip('"\'')
                except Exception:
                    pass

        plugins.append({
            "filename": filename,
            "name": name,
            "description": description,
            "source": source
        })

    return plugins


def create_html():
    return """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Calculation Plugin</title>

    <link rel="stylesheet" href="style.css">
</head>

<body>

<div class="container">

    <h1>🧮 Calculation Plugin</h1>

    <div class="card">

        <label for="pluginSelect">計算プラグイン</label>

        <select id="pluginSelect"></select>

        <div id="description" class="description"></div>

        <label for="inputValue">数値</label>

        <input
            id="inputValue"
            type="text"
            inputmode="numeric"
            placeholder="数値を入力"
        >

        <button id="calculateButton">
            計算する
        </button>

        <div id="progressArea" class="progress-area">

            <div class="progress-text">
                <span id="progressMessage">計算中...</span>
                <span id="progressPercent">0%</span>
            </div>

            <div class="progress-bar">
                <div id="progressBar"></div>
            </div>

        </div>

        <div id="errorArea" class="error-area">
        </div>

        <label for="result">結果</label>

        <textarea
            id="result"
            readonly
            placeholder="ここに結果が表示されます"
        ></textarea>

        <button id="copyButton" class="copy-button">
            結果をコピー
        </button>

        <div id="status" class="status">
            Pythonを準備しています...
        </div>

    </div>

</div>

<script src="https://cdn.jsdelivr.net/pyodide/v0.28.2/full/pyodide.js"></script>
<script src="app.js"></script>

</body>
</html>
"""


def create_css():
    return """
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 20px;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background: #f4f6f8;
    color: #222;
}

.container {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
}

h1 {
    text-align: center;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;

    box-shadow:
        0 5px 20px rgba(0, 0, 0, 0.08);
}

label {
    display: block;
    font-weight: bold;
    margin-top: 18px;
    margin-bottom: 8px;
}

select,
input,
textarea {
    width: 100%;

    padding: 13px;

    border: 1px solid #ccc;
    border-radius: 10px;

    font-size: 16px;

    background: white;
}

select,
input {
    min-height: 48px;
}

.description {
    margin-top: 10px;
    padding: 12px;

    border-radius: 10px;

    background: #f0f4f8;

    color: #555;

    line-height: 1.6;
}

button {
    width: 100%;

    min-height: 50px;

    margin-top: 18px;

    border: none;
    border-radius: 10px;

    font-size: 17px;
    font-weight: bold;

    cursor: pointer;

    background: #222;
    color: white;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.copy-button {
    background: #555;
}

textarea {
    min-height: 160px;
    resize: vertical;

    font-family: monospace;
}

.progress-area {
    display: none;

    margin-top: 20px;
}

.progress-text {
    display: flex;
    justify-content: space-between;

    margin-bottom: 7px;

    font-size: 14px;
}

.progress-bar {
    width: 100%;
    height: 18px;

    background: #ddd;

    border-radius: 999px;

    overflow: hidden;
}

#progressBar {
    width: 0%;
    height: 100%;

    background: #222;

    transition: width 0.15s;
}

.error-area {
    display: none;

    margin-top: 18px;

    padding: 14px;

    border-radius: 10px;

    background: #fff0f0;

    border: 1px solid #ffb0b0;

    color: #c00000;

    white-space: pre-wrap;
}

.status {
    margin-top: 15px;

    text-align: center;

    color: #777;

    font-size: 14px;
}

@media (max-width: 600px) {

    body {
        padding: 10px;
    }

    .card {
        padding: 18px;
        border-radius: 14px;
    }

    h1 {
        font-size: 24px;
    }

    textarea {
        min-height: 180px;
    }
}
"""


def create_js(plugins):
    plugin_json = json.dumps(
        plugins,
        ensure_ascii=False
    )

    return f"""
const PLUGINS = {plugin_json};

let pyodide = null;

const pluginSelect =
    document.getElementById("pluginSelect");

const description =
    document.getElementById("description");

const inputValue =
    document.getElementById("inputValue");

const calculateButton =
    document.getElementById("calculateButton");

const result =
    document.getElementById("result");

const copyButton =
    document.getElementById("copyButton");

const status =
    document.getElementById("status");

const progressArea =
    document.getElementById("progressArea");

const progressBar =
    document.getElementById("progressBar");

const progressPercent =
    document.getElementById("progressPercent");

const progressMessage =
    document.getElementById("progressMessage");

const errorArea =
    document.getElementById("errorArea");


function setupPlugins() {{

    pluginSelect.innerHTML = "";

    PLUGINS.forEach((plugin, index) => {{

        const option =
            document.createElement("option");

        option.value = index;

        option.textContent = plugin.name;

        pluginSelect.appendChild(option);
    }});

    updateDescription();
}}


function updateDescription() {{

    const plugin =
        PLUGINS[pluginSelect.value];

    if (!plugin) {{
        description.textContent = "";
        return;
    }}

    description.textContent =
        plugin.description;
}}


function setProgress(percent, message) {{

    percent = Math.max(0, Math.min(100, percent));

    progressBar.style.width =
        percent + "%";

    progressPercent.textContent =
        Math.round(percent) + "%";

    progressMessage.textContent =
        message;
}}


function showError(message) {{

    errorArea.textContent =
        "⚠ " + message;

    errorArea.style.display =
        "block";
}}


function hideError() {{

    errorArea.textContent = "";

    errorArea.style.display =
        "none";
}}


async function loadPython() {{

    try {{

        setProgress(10, "Pythonを読み込んでいます...");

        pyodide =
            await loadPyodide();

        setProgress(70, "Pythonを準備しています...");

        await pyodide.runPythonAsync(`
import sys
sys.set_int_max_str_digits(0)
`);

        setProgress(100, "準備完了");

        status.textContent =
            "Python準備完了";

        progressArea.style.display =
            "none";

        calculateButton.disabled =
            false;

    }} catch (error) {{

        showError(
            "Pythonの読み込みに失敗しました。\\n"
            + error
        );

        status.textContent =
            "Pythonの準備に失敗しました。";

    }}
}}


async function calculate() {{

    hideError();

    result.value = "";

    const plugin =
        PLUGINS[pluginSelect.value];

    const value =
        inputValue.value.trim();

    if (!value) {{

        showError("数値を入力してください。");

        return;
    }}

    if (!plugin) {{

        showError("プラグインが選択されていません。");

        return;
    }}

    if (!pyodide) {{

        showError("Pythonをまだ準備中です。");

        return;
    }}

    calculateButton.disabled =
        true;

    copyButton.disabled =
        true;

    progressArea.style.display =
        "block";

    setProgress(
        5,
        "計算を開始しています..."
    );

    try {{

        await new Promise(
            resolve => setTimeout(resolve, 50)
        );

        setProgress(
            25,
            plugin.name + "を実行しています..."
        );

        await pyodide.runPythonAsync(
            plugin.source
        );

        setProgress(
            55,
            "計算しています..."
        );

        pyodide.globals.set(
            "web_input",
            value
        );

        const output =
            await pyodide.runPythonAsync(`
result = calculate(web_input)
str(result)
`);

        setProgress(
            90,
            "結果を表示しています..."
        );

        result.value =
            output;

        setProgress(
            100,
            "計算完了"
        );

        await new Promise(
            resolve => setTimeout(resolve, 250)
        );

        progressArea.style.display =
            "none";

        copyButton.disabled =
            false;

    }} catch (error) {{

        progressArea.style.display =
            "none";

        let message =
            error?.message || String(error);

        // Pyodideのエラー表示を少し整理
        message =
            message
                .replace(/^PythonError:\\s*/i, "")
                .replace(/Traceback[\\\\s\\\\S]*?ValueError:\\s*/i, "");

        showError(message);

    }} finally {{

        calculateButton.disabled =
            false;
    }}
}}


async function copyResult() {{

    if (!result.value) {{
        return;
    }}

    try {{

        await navigator.clipboard.writeText(
            result.value
        );

        status.textContent =
            "結果をコピーしました！";

    }} catch {{

        result.select();

        document.execCommand("copy");

        status.textContent =
            "結果をコピーしました！";
    }}
}}


pluginSelect.addEventListener(
    "change",
    updateDescription
);

calculateButton.addEventListener(
    "click",
    calculate
);

copyButton.addEventListener(
    "click",
    copyResult
);

inputValue.addEventListener(
    "keydown",
    event => {{

        if (event.key === "Enter") {{
            calculate();
        }}
    }}
);


setupPlugins();

calculateButton.disabled =
    true;

copyButton.disabled =
    true;

loadPython();
"""


def create_docs():
    os.makedirs(DOCS_DIR, exist_ok=True)

    plugins = load_plugins()

    with open(
        os.path.join(DOCS_DIR, "index.html"),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(create_html())

    with open(
        os.path.join(DOCS_DIR, "style.css"),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(create_css())

    with open(
        os.path.join(DOCS_DIR, "app.js"),
        "w",
        encoding="utf-8"
    ) as f:
        f.write(create_js(plugins))

    print("Web版を生成しました。")
    print(f"プラグイン数: {{len(plugins)}}")

    for plugin in plugins:
        print(
            f"- {{plugin['name']}}: "
            f"{{plugin['description']}}"
        )


if __name__ == "__main__":
    create_docs()