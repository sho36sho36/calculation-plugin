
const PLUGINS = [{"filename": "double_factorial.py", "source": "import math\n\nPLUGIN_NAME = \"二重階乗\"\n\n\ndef calculate(value):\n    n = int(value)\n\n    if n < 0:\n        raise ValueError(\"負の数には対応していません。\")\n\n    if n == 0 or n == 1:\n        return 1\n\n    # 偶数二重階乗\n    #\n    # n!! = 2^(n/2) × (n/2)!\n    if n % 2 == 0:\n        k = n // 2\n        return (2 ** k) * math.factorial(k)\n\n    # 奇数二重階乗\n    #\n    # n!! = n! / (2^k × k!)\n    k = (n - 1) // 2\n\n    return math.factorial(n) // (\n        (2 ** k) * math.factorial(k)\n    )"}, {"filename": "test.py", "source": "PLUGIN_NAME = \"テスト計算\"\n\n\ndef calculate(value):\n    return value"}];

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


function showMessage(text) {

    messageElement.textContent = text;

}


function setupPlugins() {

    pluginElement.innerHTML = "";

    for (
        let i = 0;
        i < PLUGINS.length;
        i++
    ) {

        const option =
            document.createElement("option");

        option.value = i;

        option.textContent =
            PLUGINS[i].filename;

        pluginElement.appendChild(option);
    }

}


async function loadPython() {

    try {

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

    } catch (error) {

        console.error(error);

        statusElement.textContent =
            "Pythonの読み込みに失敗しました";

        showMessage(
            error.toString()
        );
    }

}


async function calculate() {

    if (!ready) {
        return;
    }

    const input =
        inputElement.value.trim();

    if (input === "") {

        showMessage(
            "数値を入力してください。"
        );

        return;
    }

    const index =
        Number(pluginElement.value);

    const plugin =
        PLUGINS[index];

    if (!plugin) {

        showMessage(
            "プラグインが見つかりません。"
        );

        return;
    }

    calculateButton.disabled = true;

    copyButton.disabled = true;

    resultElement.value = "";

    showMessage(
        "計算しています..."
    );

    try {

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

    } catch (error) {

        console.error(error);

        showMessage(
            "計算エラー: " +
            error.toString()
        );

    } finally {

        calculateButton.disabled = false;

    }

}


async function copyResult() {

    const text =
        resultElement.value;

    if (!text) {
        return;
    }

    try {

        await navigator.clipboard.writeText(
            text
        );

        showMessage(
            "結果をコピーしました。"
        );

    } catch (error) {

        // 古いブラウザ向け
        resultElement.focus();

        resultElement.select();

        document.execCommand("copy");

        showMessage(
            "結果をコピーしました。"
        );
    }

}


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
    function(event) {

        if (
            event.key === "Enter"
        ) {
            calculate();
        }

    }
);


loadPython();
