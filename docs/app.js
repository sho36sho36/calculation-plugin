
const PLUGINS = [{"filename": "collatz.py", "name": "コラッツ予想", "description": "数が1になるまでのコラッツ操作を計算します。", "source": "PLUGIN_NAME = \"コラッツ予想\"\nPLUGIN_DESCRIPTION = \"数が1になるまでのコラッツ操作を計算します。\"\n\n\ndef calculate(value):\n    n = int(value)\n\n    if n < 1:\n        raise ValueError(\"1以上の整数を指定してください。\")\n\n    sequence = [n]\n\n    while n != 1:\n        if n % 2 == 0:\n            n //= 2\n        else:\n            n = n * 3 + 1\n\n        sequence.append(n)\n\n    steps = len(sequence) - 1\n\n    return \" → \".join(map(str, sequence)) + f\"\\n\\nステップ数: {steps}\""}, {"filename": "double_factorial.py", "name": "二重階乗", "description": "n × (n-2) × (n-4) × … を計算します。", "source": "import math\n\nPLUGIN_NAME = \"二重階乗\"\nPLUGIN_DESCRIPTION = \"n × (n-2) × (n-4) × … を計算します。\"\n\n\ndef calculate(value):\n    n = int(value)\n\n    if n < 0:\n        raise ValueError(\"負の数には対応していません。\")\n\n    if n == 0 or n == 1:\n        return 1\n\n    if n % 2 == 0:\n        k = n // 2\n        return (2 ** k) * math.factorial(k)\n\n    k = (n - 1) // 2\n    return math.factorial(n) // ((2 ** k) * math.factorial(k))"}, {"filename": "hyperfactorial.py", "name": "超階乗", "description": "このプラグインの説明はありません。", "source": "PLUGIN_NAME = \"超階乗\"\n\n\ndef calculate(value):\n    n = int(value)\n\n    if n < 1:\n        raise ValueError(\"1以上の数を指定してください。\")\n\n    result = 1\n\n    for i in range(1, n + 1):\n        result *= i ** i\n\n    return result"}, {"filename": "power_tower.py", "name": "累乗階乗", "description": "n↑↑n の累乗塔を計算します。", "source": "PLUGIN_NAME = \"累乗階乗\"\nPLUGIN_DESCRIPTION = \"n↑↑n の累乗塔を計算します。\"\n\n\ndef calculate(value):\n    n = int(value)\n\n    if n < 1:\n        raise ValueError(\"1以上の整数を指定してください。\")\n\n    if n > 5:\n        raise ValueError(\"大きすぎるため、5以下にしてください。\")\n\n    result = 1\n\n    for _ in range(n):\n        result = n ** result\n\n    return result"}, {"filename": "primes.py", "name": "素数", "description": "指定した個数の素数を小さい順に求めます。", "source": "PLUGIN_NAME = \"素数\"\nPLUGIN_DESCRIPTION = \"指定した個数の素数を小さい順に求めます。\"\n\n\ndef calculate(value):\n    count = int(value)\n\n    if count < 1:\n        raise ValueError(\"1以上の数を指定してください。\")\n\n    primes = []\n    number = 2\n\n    while len(primes) < count:\n        is_prime = True\n\n        for p in primes:\n            if p * p > number:\n                break\n\n            if number % p == 0:\n                is_prime = False\n                break\n\n        if is_prime:\n            primes.append(number)\n\n        number += 1\n\n    return \", \".join(map(str, primes))"}, {"filename": "primorial.py", "name": "素数階乗", "description": "2からnまでの素数をすべて掛け合わせます。", "source": "PLUGIN_NAME = \"素数階乗\"\nPLUGIN_DESCRIPTION = \"2からnまでの素数をすべて掛け合わせます。\"\n\n\ndef calculate(value):\n    n = int(value)\n\n    if n < 2:\n        raise ValueError(\"2以上の整数を指定してください。\")\n\n    result = 1\n\n    for number in range(2, n + 1):\n        is_prime = True\n\n        for i in range(2, int(number ** 0.5) + 1):\n            if number % i == 0:\n                is_prime = False\n                break\n\n        if is_prime:\n            result *= number\n\n    return result"}, {"filename": "test.py", "name": "テスト計算", "description": "このプラグインの説明はありません。", "source": "PLUGIN_NAME = \"テスト計算\"\n\n\ndef calculate(value):\n    return value"}];

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


function setupPlugins() {

    pluginSelect.innerHTML = "";

    PLUGINS.forEach((plugin, index) => {

        const option =
            document.createElement("option");

        option.value = index;

        option.textContent = plugin.name;

        pluginSelect.appendChild(option);
    });

    updateDescription();
}


function updateDescription() {

    const plugin =
        PLUGINS[pluginSelect.value];

    if (!plugin) {
        description.textContent = "";
        return;
    }

    description.textContent =
        plugin.description;
}


function setProgress(percent, message) {

    percent = Math.max(0, Math.min(100, percent));

    progressBar.style.width =
        percent + "%";

    progressPercent.textContent =
        Math.round(percent) + "%";

    progressMessage.textContent =
        message;
}


function showError(message) {

    errorArea.textContent =
        "⚠ " + message;

    errorArea.style.display =
        "block";
}


function hideError() {

    errorArea.textContent = "";

    errorArea.style.display =
        "none";
}


async function loadPython() {

    try {

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

    } catch (error) {

        showError(
            "Pythonの読み込みに失敗しました。\n"
            + error
        );

        status.textContent =
            "Pythonの準備に失敗しました。";

    }
}


async function calculate() {

    hideError();

    result.value = "";

    const plugin =
        PLUGINS[pluginSelect.value];

    const value =
        inputValue.value.trim();

    if (!value) {

        showError("数値を入力してください。");

        return;
    }

    if (!plugin) {

        showError("プラグインが選択されていません。");

        return;
    }

    if (!pyodide) {

        showError("Pythonをまだ準備中です。");

        return;
    }

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

    try {

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

    } catch (error) {

        progressArea.style.display =
            "none";

        let message =
            error?.message || String(error);

        // Pyodideのエラー表示を少し整理
        message =
            message
                .replace(/^PythonError:\s*/i, "")
                .replace(/Traceback[\\s\\S]*?ValueError:\s*/i, "");

        showError(message);

    } finally {

        calculateButton.disabled =
            false;
    }
}


async function copyResult() {

    if (!result.value) {
        return;
    }

    try {

        await navigator.clipboard.writeText(
            result.value
        );

        status.textContent =
            "結果をコピーしました！";

    } catch {

        result.select();

        document.execCommand("copy");

        status.textContent =
            "結果をコピーしました！";
    }
}


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
    event => {

        if (event.key === "Enter") {
            calculate();
        }
    }
);


setupPlugins();

calculateButton.disabled =
    true;

copyButton.disabled =
    true;

loadPython();
