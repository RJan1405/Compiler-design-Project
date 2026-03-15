const editor = document.getElementById('editor');
const lineNumbers = document.getElementById('line-numbers');
const pythonOut = document.getElementById('python-output');
const consoleOut = document.getElementById('console-output');

// Trace Elements
const traceTokens = document.getElementById('trace-tokens');
const traceAst = document.getElementById('trace-ast');
const traceSymbols = document.getElementById('trace-symbols');
const traceTac = document.getElementById('trace-tac');

// Header Navigation
function switchTab(tabId, element) {
    // Nav Items
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    element.classList.add('active');

    // Panes
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
}

// Editor Functionality
function updateLineNumbers() {
    const lines = editor.value.split('\n').length;
    lineNumbers.innerHTML = Array.from({length: lines}, (_, i) => i + 1).join('<br>');
}

editor.addEventListener('input', updateLineNumbers);
editor.addEventListener('scroll', () => {
    lineNumbers.scrollTop = editor.scrollTop;
});

function insertEmoji(emoji) {
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const text = editor.value;
    editor.value = text.substring(0, start) + emoji + text.substring(end);
    editor.focus();
    editor.selectionStart = editor.selectionEnd = start + emoji.length;
    updateLineNumbers();
}

function clearEditor() {
    editor.value = '';
    pythonOut.textContent = '# Waiting for code...';
    consoleOut.textContent = 'Ready for input...';
    
    // Clear traces
    if(traceTokens) traceTokens.textContent = '# No data';
    if(traceAst) traceAst.textContent = '# No data';
    if(traceSymbols) traceSymbols.textContent = '# No data';
    if(traceTac) traceTac.textContent = '# No data';
    
    updateLineNumbers();
}

function loadDefaultSample() {
    const code = `🙂\n🆕 a = 5\n🆕 b = 10\n📢 a ➕ b\n🔚`;
    editor.value = code;
    updateLineNumbers();
    pythonOut.textContent = '# Ready to compile...';
    consoleOut.textContent = 'Sample code loaded.';
}

function copySnippet(element) {
    const code = element.innerText.replace(/\\n/g, '\n');
    editor.value = code;
    updateLineNumbers();
    // Switch to compiler tab automatically
    document.querySelectorAll('.nav-item')[0].click();
}

// Compiler Logic
async function compileCode() {
    const code = editor.value;
    if (!code.trim()) return;

    consoleOut.textContent = "⚙️ Executing compiler logic...";
    pythonOut.textContent = "# Generating intermediate code...";

    try {
        const response = await fetch('http://localhost:5000/compile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });

        const result = await response.json();

        if (result.success) {
            pythonOut.textContent = result.python_code;
            consoleOut.textContent = result.execution_output || '✅ Code executed (no printed output).';
            
            // Populate Live Pipeline Trace
            if(traceTokens) traceTokens.textContent = JSON.stringify(result.tokens, null, 2);
            if(traceAst) traceAst.textContent = JSON.stringify(result.ast, null, 2);
            if(traceSymbols) traceSymbols.textContent = JSON.stringify(result.symbol_table, null, 2);
            if(traceTac) traceTac.textContent = result.tac_code ? result.tac_code.join('\n') : '# No TAC generated';
        } else {
            pythonOut.textContent = '# COMPILATION FAILED';
            consoleOut.textContent = `❌ ${result.error || (result.errors ? result.errors.join('\n') : 'Unknown Error')}`;
            
            // Populate partial trace if possible
            if (result.tokens && traceTokens) traceTokens.textContent = JSON.stringify(result.tokens, null, 2);
            if (result.ast && traceAst) traceAst.textContent = JSON.stringify(result.ast, null, 2);
        }
    } catch (error) {
        consoleOut.textContent = "⛔ Fatal Error: Backend server is offline.\nCheck if 'python app.py' is running.";
        pythonOut.textContent = "# CONNECTION ERROR";
    }
}

// Initialize
updateLineNumbers();

const ALL_EXAMPLES = [
    { title: "Example 1: Absolute Minimum", code: "🙂\n🔚", desc: "The bare minimum structure required." },
    { title: "Example 2: Minimal Print", code: "🙂\n📢 1\n🔚", desc: "A program that just outputs the number 1." },
    { title: "Example 3: Simple Declaration", code: "🙂\n🆕 x = 10\n📢 x\n🔚", desc: "Creating and printing a variable." },
    { title: "Example 4: Variable Update", code: "🙂\n🆕 count = 1\ncount = 5\n📢 count\n🔚", desc: "Updating an existing variable." },
    { title: "Example 5: Var to Var", code: "🙂\n🆕 a = 100\n🆕 b = a\n📢 b\n🔚", desc: "Assigning one variable to another." },
    { title: "Example 8: Addition", code: "🙂\n🆕 sum = 10 ➕ 5\n📢 sum\n🔚", desc: "Basic addition math." },
    { title: "Example 9: Subtraction", code: "🙂\n🆕 diff = 20 ➖ 8\n📢 diff\n🔚", desc: "Basic subtraction math." },
    { title: "Example 10: Multiplication", code: "🙂\n🆕 prod = 4 ✖ 4\n📢 prod\n🔚", desc: "Basic multiplication math." },
    { title: "Example 11: Division", code: "🙂\n🆕 quot = 20 ➗ 5\n📢 quot\n🔚", desc: "Basic division math." },
    { title: "Example 12: Complex Math", code: "🙂\n🆕 result = 10 ➕ 5 ✖ 2 ➖ 4\n📢 result\n🔚", desc: "Order of operations demo." },
    { title: "Example 13: Simple IF", code: "🙂\n🆕 age = 20\n❓ age > 18 ➡\n    📢 1\n🔚", desc: "Basic conditional branching." },
    { title: "Example 14: IF and ELSE", code: "🙂\n🆕 score = 40\n❓ score > 50 ➡\n    📢 100\n🔁\n    📢 0\n🔚", desc: "Binary decision logic." },
    { title: "Example 16: Counter Loop", code: "🙂\n🆕 i = 1\n🔄 i < 4 ➡\n    📢 i\n    i = i ➕ 1\n🔚", desc: "Classic while-loop structure." },
    { title: "Example 17: Countdown", code: "🙂\n🆕 i = 5\n🔄 i > 0 ➡\n    📢 i\n    i = i ➖ 1\n🔚", desc: "Looping backwards." },
    { title: "Example 18: Loop + IF", code: "🙂\n🆕 x = 1\n🔄 x < 6 ➡\n    ❓ x == 3 ➡\n        📢 333\n    🔁\n        📢 x\n    x = x ➕ 1\n🔚", desc: "Combining loops and conditions." },
    { title: "Example 19: Bank Balance", code: "🙂\n🆕 balance = 100\n🆕 withdrawal = 40\nbalance = balance ➖ withdrawal\n❓ balance > 50 ➡\n    📢 balance\n🔁\n    📢 0\n🔚", desc: "Real-world logic simulation." },
    { title: "Example 20: Mult. Table", code: "🙂\n🆕 n = 5\n🆕 i = 1\n🔄 i < 5 ➡\n    📢 n ✖ i\n    i = i ➕ 1\n🔚", desc: "Generating math sequences." },
    { title: "Example 21: Final Boss", code: "🙂\n🆕 count = 1\n🆕 max = 3\n🔄 count == max ➡\n    📢 0\n🆕 a = 10\n🆕 b = 2\n❓ a ➗ b == 5 ➡\n    📢 a ➕ b\n🔚", desc: "Everything combined together." },
    { title: "Example 22: Basic String", code: "🙂\n🆕 message = \"Hello World\"\n📢 message\n🔚", desc: "Handling text characters." },
    { title: "Example 23: String Update", code: "🙂\n🆕 text = \"Original\"\ntext = \"Updated Text\"\n📢 text\n🔚", desc: "Updating text variables." }
];

function initializeGallery() {
    const gallery = document.getElementById('example-gallery');
    if (!gallery) return;

    ALL_EXAMPLES.forEach((ex, index) => {
        const card = document.createElement('div');
        card.className = 'snippet-card';
        card.innerHTML = `
            <div>
                <h4>${ex.title}</h4>
                <p>${ex.desc}</p>
                <pre onclick="loadByIndex(${index})">${ex.code}</pre>
            </div>
            <button class="btn-load-snippet" onclick="loadByIndex(${index})">Load to Editor</button>
        `;
        gallery.appendChild(card);
    });
}

function loadByIndex(index) {
    const ex = ALL_EXAMPLES[index];
    if (!ex) return;
    
    editor.value = ex.code;
    updateLineNumbers();
    
    // Switch to compiler tab
    const compilerTab = document.querySelectorAll('.nav-item')[0];
    if (compilerTab) {
        // Find the right element to trigger the click
        switchTab('compiler', compilerTab);
    }
    
    consoleOut.textContent = "🚀 Loaded: " + ex.title;
    pythonOut.textContent = "# Ready for compilation.";
    
    // Smooth scroll to top of editor
    editor.scrollTop = 0;
}

initializeGallery();
