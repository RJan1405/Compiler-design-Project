function insertEmoji(emoji) {
    const editor = document.getElementById('editor');
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const text = editor.value;
    editor.value = text.substring(0, start) + emoji + text.substring(end);
    editor.focus();
    editor.setSelectionRange(start + emoji.length, start + emoji.length);
}

function clearEditor() {
    document.getElementById('editor').value = '';
    resetOutputs();
}

function resetOutputs() {
    document.getElementById('python-output').textContent = '# Python code will appear here...';
    document.getElementById('console-output').textContent = 'Ready for input...';
    document.getElementById('error-panel').classList.add('hidden');
}

function loadExample() {
    const example = `🙂
🆕 a = 5
🆕 b = 10
📢 a ➕ b
🔚`;
    document.getElementById('editor').value = example;
    resetOutputs();
}

async function compileCode() {
    const code = document.getElementById('editor').value;
    const errorPanel = document.getElementById('error-panel');
    const pythonOut = document.getElementById('python-output');
    const consoleOut = document.getElementById('console-output');

    errorPanel.classList.add('hidden');
    pythonOut.textContent = '# Compiling...';
    consoleOut.textContent = 'Processing request...';

    try {
        const response = await fetch('http://localhost:5000/compile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });

        const result = await response.json();

        if (result.success) {
            pythonOut.textContent = result.python_code;
            consoleOut.textContent = result.execution_output || 'Code executed (no output to display).';
        } else {
            pythonOut.textContent = '# Compilation Failed.';
            consoleOut.textContent = 'Errors found in logic.';
            showError(result.errors ? result.errors.join('<br>') : (result.error || 'Unknown error'));
        }
    } catch (err) {
        pythonOut.textContent = '# Server Connection Error';
        consoleOut.textContent = 'Failed to reach backend.';
        showError('Could not connect to the backend server. Make sure Flask is running on port 5000.');
    }
}

function showError(msg) {
    const panel = document.getElementById('error-panel');
    panel.innerHTML = `<strong>Compiler Error:</strong><br>${msg}`;
    panel.classList.remove('hidden');
    setTimeout(() => panel.classList.add('hidden'), 5000);
}

// Simple Auto-resize for editor
document.getElementById('editor').addEventListener('input', function() {
    // Currently fixed height in layout, but can add scroll logic here if needed
});
