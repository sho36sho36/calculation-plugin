import os
import json


# ==========================================
# 設定
# ==========================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(ROOT_DIR, "plugins")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")


# ==========================================
# プラグイン読み込み
# ==========================================

def load_plugins():
    plugins = []

    if not os.path.exists(PLUGIN_DIR):
        return plugins

    for filename in sorted(os.listdir(PLUGIN_DIR)):

        # Pythonファイル以外は無視
        if not filename.endswith(".py"):
            continue

        # 初期化ファイルは無視
        if filename == "__init__.py":
            continue

        path = os.path.join(PLUGIN_DIR, filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                source = f.read()

        except Exception as e:
            print(f"読み込み失敗: {filename}")
            print(e)
            continue

        # デフォルト値
        name = filename
        description = "このプラグインの説明はありません。"

        # ------------------------------------------
        # PLUGIN_NAME / PLUGIN_DESCRIPTION を取得
        # ------------------------------------------

        for line in source.splitlines():

            line = line.strip()

            if line.startswith("PLUGIN_NAME"):

                try:
                    value = line.split("=", 1)[1].strip()

                    if (
                        len(value) >= 2
                        and value[0] in ("\"", "'")
                        and value[-1] == value[0]
                    ):
                        value = value[1:-1]

                    name = value

                except Exception:
                    pass

            elif line.startswith("PLUGIN_DESCRIPTION"):

                try:
                    value = line.split("=", 1)[1].strip()

                    if (
                        len(value) >= 2
                        and value[0] in ("\"", "'")
                        and value[-1] == value[0]
                    ):
                        value = value[1:-1]

                    description = value

                except Exception:
                    pass

        plugins.append({
            "filename": filename,
            "name": name,
            "description": description,
            "source": source
        })

    return plugins


# ==========================================
# HTML
# ==========================================

def create_html():

    return """<!DOCTYPE html>
<html lang="ja">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta
        name="description"
        content="Calculation Plugin - 数学計算プラグイン"
    >

    <title>Calculation Plugin</title>

    <link rel="stylesheet" href="style.css">

</head>


<body>

<div class="container">

    <h1>🧮 Calculation Plugin</h1>


    <div class="card">


        <!-- ============================= -->
        <!-- プラグイン選択 -->
        <!-- ============================= -->

        <label for="pluginSelect">
            計算プラグイン
        </label>

        <select id="pluginSelect">
        </select>


        <!-- ============================= -->
        <!-- プラグイン説明 -->
        <!-- ============================= -->

        <div
            id="description"
            class="description"
        >
        </div>


        <!-- ============================= -->
        <!-- 数値入力 -->
        <!-- ============================= -->

        <label for="inputValue">
            数値
        </label>

        <input
            id="inputValue"
            type="text"
            inputmode="numeric"
            autocomplete="off"
            placeholder="数値を入力"
        >


        <!-- ============================= -->
        <!-- 計算ボタン -->
        <!-- ============================= -->

        <button
            id="calculateButton"
            disabled
        >
            計算する
        </button>


        <!-- ============================= -->
        <!-- プログレスバー -->
        <!-- ============================= -->

        <div
            id="progressArea"
            class="progress-area"
        >

            <div class="progress-text">

                <span id="progressMessage">
                    計算中...
                </span>

                <span id="progressPercent">
                    0%
                </span>

            </div>


            <div class="progress-bar">

                <div
                    id="progressBar"
                ></div>

            </div>

        </div>


        <!-- ============================= -->
        <!-- エラー -->
        <!-- ============================= -->

        <div
            id="errorArea"
            class="error-area"
        >
        </div>


        <!-- ============================= -->
        <!-- 結果 -->
        <!-- ============================= -->

        <label for="result">
            結果
        </label>

        <textarea
            id="result"
            readonly
            placeholder="ここに結果が表示されます"
        ></textarea>


        <!-- ============================= -->
        <!-- コピー -->
        <!-- ============================= -->

        <button
            id="copyButton"
            class="copy-button"
            disabled
        >
            結果をコピー
        </button>


        <!-- ============================= -->
        <!-- ステータス -->
        <!-- ============================= -->

        <div
            id="status"
            class="status"
        >
            Pythonを準備しています...
        </div>


    </div>

</div>


<!-- ============================= -->
<!-- Pyodide -->
<!-- ============================= -->

<script
    src="https://cdn.jsdelivr.net/pyodide/v0.28.2/full/pyodide.js"
></script>


<script src="app.js"></script>


</body>

</html>
"""


# ==========================================
# CSS
# ==========================================

def create_css():

    return """
/* =========================================
   基本
========================================= */

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
        "Noto Sans JP",
        sans-serif;

    background: #f4f6f8;

    color: #222;
}


/* =========================================
   コンテナ
========================================= */

.container {

    width: 100%;

    max-width: 700px;

    margin: 0 auto;
}


/* =========================================
   タイトル
========================================= */

h1 {

    text-align: center;

    margin-top: 10px;

    margin-bottom: 25px;

    font-size: 30px;
}


/* =========================================
   カード
========================================= */

.card {

    background: white;

    padding: 25px;

    border-radius: 18px;

    box-shadow:
        0 5px 20px rgba(0, 0, 0, 0.08);
}


/* =========================================
   ラベル
========================================= */

label {

    display: block;

    font-weight: bold;

    margin-top: 18px;

    margin-bottom: 8px;
}


/* =========================================
   入力
========================================= */

select,
input,
textarea {

    width: 100%;

    padding: 13px;

    border: 1px solid #ccc;

    border-radius: 10px;

    font-size: 16px;

    background: white;

    color: #222;
}


select,
input {

    min-height: 48px;
}


input:focus,
select:focus,
textarea:focus {

    outline: none;

    border-color: #777;
}


/* =========================================
   説明
========================================= */

.description {

    margin-top: 10px;

    padding: 12px;

    border-radius: 10px;

    background: #f0f4f8;

    color: #555;

    line-height: 1.6;

    min-height: 24px;
}


/* =========================================
   ボタン
========================================= */

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

    transition:
        opacity 0.2s,
        transform 0.1s;
}


button:hover:not(:disabled) {

    opacity: 0.85;
}


button:active:not(:disabled) {

    transform: scale(0.99);
}


button:disabled {

    opacity: 0.5;

    cursor: not-allowed;
}


/* =========================================
   コピー
========================================= */

.copy-button {

    background: #555;
}


/* =========================================
   結果
========================================= */

textarea {

    min-height: 180px;

    resize: vertical;

    font-family:
        Consolas,
        "Courier New",
        monospace;

    line-height: 1.5;
}


/* =========================================
   プログレス
========================================= */

.progress-area {

    display: none;

    margin-top: 20px;
}


.progress-text {

    display: flex;

    justify-content: space-between;

    align-items: center;

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

    border-radius: 999px;
}


/* =========================================
   計算中アニメーション
========================================= */

#progressBar.indeterminate {

    width: 40%;

    animation:
        progressMove 1.2s infinite;
}


@keyframes progressMove {

    0% {

        transform: translateX(-120%);
    }

    100% {

        transform: translateX(350%);
    }
}


/* =========================================
   エラー
========================================= */

.error-area {

    display: none;

    margin-top: 18px;

    padding: 14px;

    border-radius: 10px;

    background: #fff0f0;

    border: 1px solid #ffb0b0;

    color: #c00000;

    white-space: pre-wrap;

    line-height: 1.5;
}


/* =========================================
   ステータス
========================================= */

.status {

    margin-top: 15px;

    text-align: center;

    color: #777;

    font-size: 14px;
}


/* =========================================
   スマホ
========================================= */

@media (max-width: 600px) {

    body {

        padding: 10px;
    }


    .container {

        width: 100%;
    }


    h1 {

        font-size: 24px;

        margin-top: 5px;

        margin-bottom: 18px;
    }


    .card {

        padding: 18px;

        border-radius: 14px;
    }


    button {

        min-height: 52px;

        font-size: 17px;
    }


    input,
    select {

        min-height: 50px;

        font-size: 16px;
    }


    textarea {

        min-height: 200px;

        font-size: 14px;
    }
}


/* =========================================
   ダークモード
========================================= */

@media (prefers-color-scheme: dark) {

    body {

        background: #151515;

        color: #eee;
    }


    .card {

        background: #222;
    }


    select,
    input,
    textarea {

        background: #2c2c2c;

        color: #eee;

        border-color: #555;
    }


    .description {

        background: #2d3236;

        color: #ccc;
    }


    .progress-bar {

        background: #444;
    }


    .status {

        color: #aaa;
    }
}
"""


# ==========================================
# JavaScript
# ==========================================

def create_js(plugins):

    plugin_json = json.dumps(
        plugins,
        ensure_ascii=False
    )

    return f"""
// ==========================================
// プラグインデータ
// ==========================================

const PLUGINS = {plugin_json};


// ==========================================
// Pyodide
// ==========================================

let pyodide = null;


// ==========================================
// DOM
// ==========================================

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


// ==========================================
// プラグイン一覧
// ==========================================

function setupPlugins() {{

    pluginSelect.innerHTML = "";

    PLUGINS.forEach((plugin, index) => {{

        const option =
            document.createElement("option");

        option.value = index;

        option.textContent =
            plugin.name;

        pluginSelect.appendChild(option);
    }});

    updateDescription();
}}


// ==========================================
// 説明更新
// ==========================================

function updateDescription() {{

    const index =
        Number(pluginSelect.value);

    const plugin =
        PLUGINS[index];

    if (!plugin) {{

        description.textContent = "";

        return;
    }}

    description.textContent =
        plugin.description;
}}


// ==========================================
// プログレス設定
// ==========================================

function setProgress(percent, message) {{

    percent =
        Math.max(
            0,
            Math.min(100, percent)
        );

    progressBar.style.width =
        percent + "%";

    progressPercent.textContent =
        Math.round(percent) + "%";

    progressMessage.textContent =
        message;
}}


// ==========================================
// 無限進捗アニメーション
// ==========================================

function startIndeterminateProgress() {{

    progressBar.classList.add(
        "indeterminate"
    );
}}


function stopIndeterminateProgress() {{

    progressBar.classList.remove(
        "indeterminate"
    );
}}


// ==========================================
// エラー表示
// ==========================================

function showError(message) {{

    errorArea.textContent =
        "⚠ " + message;

    errorArea.style.display =
        "block";
}}


function hideError() {{

    errorArea.textContent =
        "";

    errorArea.style.display =
        "none";
}}


// ==========================================
// Python読み込み
// ==========================================

async function loadPython() {{

    try {{

        progressArea.style.display =
            "block";

        setProgress(
            10,
            "Pythonを読み込んでいます..."
        );


        pyodide =
            await loadPyodide();


        setProgress(
            70,
            "Pythonを準備しています..."
        );


        await pyodide.runPythonAsync(`
import sys

try:
    sys.set_int_max_str_digits(0)
except AttributeError:
    pass
`);


        setProgress(
            100,
            "準備完了"
        );


        status.textContent =
            "Python準備完了";


        await new Promise(
            resolve => setTimeout(resolve, 300)
        );


        progressArea.style.display =
            "none";


        calculateButton.disabled =
            false;


    }} catch (error) {{

        progressArea.style.display =
            "none";

        stopIndeterminateProgress();

        showError(
            cleanErrorMessage(error)
        );

        status.textContent =
            "Pythonの準備に失敗しました。";
    }}
}}


// ==========================================
// エラーメッセージ整理
// ==========================================

function cleanErrorMessage(error) {{

    let message =
        error?.message || String(error);


    // 改行を整理
    message =
        message.replace(/\\r/g, "");


    // Tracebackがある場合
    if (message.includes("Traceback")) {{

        const lines =
            message
                .split("\\n")
                .map(line => line.trim())
                .filter(Boolean);


        // 最後のPythonエラー行を探す
        for (
            let i = lines.length - 1;
            i >= 0;
            i--
        ) {{

            const line =
                lines[i];

            if (
                line.startsWith("ValueError:")
                ||
                line.startsWith("TypeError:")
                ||
                line.startsWith("OverflowError:")
                ||
                line.startsWith("ZeroDivisionError:")
                ||
                line.startsWith("IndexError:")
                ||
                line.startsWith("KeyError:")
                ||
                line.startsWith("NameError:")
                ||
                line.startsWith("SyntaxError:")
            ) {{

                message = line;

                break;
            }}
        }}
    }}


    // PythonErrorを削除
    message =
        message.replace(
            /^PythonError:\\s*/i,
            ""
        );


    // エラー種類を削除
    message =
        message.replace(
            /^(ValueError|TypeError|OverflowError|ZeroDivisionError|IndexError|KeyError|NameError|SyntaxError):\\s*/i,
            ""
        );


    return message.trim();
}}


// ==========================================
// 計算
// ==========================================

async function calculate() {{

    hideError();

    result.value = "";


    const index =
        Number(pluginSelect.value);

    const plugin =
        PLUGINS[index];


    const value =
        inputValue.value.trim();


    // --------------------------------------
    // 入力チェック
    // --------------------------------------

    if (!value) {{

        showError(
            "数値を入力してください。"
        );

        return;
    }}


    if (!plugin) {{

        showError(
            "プラグインが選択されていません。"
        );

        return;
    }}


    if (!pyodide) {{

        showError(
            "Pythonをまだ準備中です。"
        );

        return;
    }}


    // --------------------------------------
    // UI無効化
    // --------------------------------------

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

        // UI更新用
        await new Promise(
            resolve => setTimeout(resolve, 50)
        );


        setProgress(
            20,
            plugin.name +
            "を準備しています..."
        );


        // ----------------------------------
        // プラグイン実行
        // ----------------------------------

        await pyodide.runPythonAsync(
            plugin.source
        );


        setProgress(
            45,
            "計算しています..."
        );


        startIndeterminateProgress();


        // Pythonへ入力
        pyodide.globals.set(
            "web_input",
            value
        );


        // ----------------------------------
        // calculate()
        // ----------------------------------

        const output =
            await pyodide.runPythonAsync(`
result = calculate(web_input)
str(result)
`);


        stopIndeterminateProgress();


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
            resolve => setTimeout(resolve, 300)
        );


        progressArea.style.display =
            "none";


        copyButton.disabled =
            false;


        status.textContent =
            "計算完了";


    }} catch (error) {{

        stopIndeterminateProgress();

        progressArea.style.display =
            "none";


        const message =
            cleanErrorMessage(error);


        showError(message);


        status.textContent =
            "計算に失敗しました。";


    }} finally {{

        calculateButton.disabled =
            false;
    }}
}}


// ==========================================
// コピー
// ==========================================

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


    }} catch (error) {{

        // 古いブラウザ向け
        result.select();

        document.execCommand("copy");


        status.textContent =
            "結果をコピーしました！";
    }}
}}


// ==========================================
// イベント
// ==========================================

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


// Enterで計算
inputValue.addEventListener(
    "keydown",
    event => {{

        if (event.key === "Enter") {{

            calculate();
        }}
    }}
);


// ==========================================
// 起動
// ==========================================

setupPlugins();

calculateButton.disabled =
    true;

copyButton.disabled =
    true;

loadPython();
"""


# ==========================================
# docs生成
# ==========================================

def create_docs():

    os.makedirs(
        DOCS_DIR,
        exist_ok=True
    )


    plugins = load_plugins()


    # --------------------------------------
    # index.html
    # --------------------------------------

    with open(
        os.path.join(
            DOCS_DIR,
            "index.html"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            create_html()
        )


    # --------------------------------------
    # style.css
    # --------------------------------------

    with open(
        os.path.join(
            DOCS_DIR,
            "style.css"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            create_css()
        )


    # --------------------------------------
    # app.js
    # --------------------------------------

    with open(
        os.path.join(
            DOCS_DIR,
            "app.js"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            create_js(plugins)
        )


    # --------------------------------------
    # 完了表示
    # --------------------------------------

    print()
    print("=" * 50)
    print("Web版を生成しました！")
    print("=" * 50)

    print()

    print(
        f"プラグイン数: {len(plugins)}"
    )

    print()

    for plugin in plugins:

        print(
            f"・{plugin['name']}"
        )

        print(
            f"  {plugin['description']}"
        )

    print()

    print(
        f"出力先: {DOCS_DIR}"
    )

    print()


# ==========================================
# メイン
# ==========================================

if __name__ == "__main__":

    create_docs()