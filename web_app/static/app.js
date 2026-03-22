/* ===================== State ===================== */
let selectedBrowser = 'chrome';
let selectedFramework = 'python';
let polling = null;
let lastLineCount = 0;
let generationPolling = null;
let generationLastLineCount = 0;

/* ===================== Init ===================== */
document.addEventListener('DOMContentLoaded', async () => {
    await Promise.all([
        loadConfig(),
        checkPrerequisites(),
        loadTestCases(),
        refreshReports(),
    ]);
    const st = await api('/api/run-status');
    if (st && st.status === 'running') {
        setUIRunning();
        startPolling();
    }
    const gst = await api('/api/generate-excel-status').catch(() => null);
    if (gst && gst.status === 'running') {
        setGeneratorUiRunning();
        startGenerationPolling();
    } else if (gst && gst.status === 'completed') {
        setGeneratorUiCompleted();
        if (gst.output_file) {
            const btn = document.getElementById('downloadGeneratedBtn');
            btn.style.display = 'inline-flex';
            btn.href = '/api/generated-excel/download?ts=' + Date.now();
        }
    }
});

/* ===================== API helper ===================== */
async function api(url, options = {}) {
    try {
        const res = await fetch(url, options);
        if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            throw new Error(err.detail || res.statusText);
        }
        return await res.json();
    } catch (e) {
        console.error('API error:', e);
        throw e;
    }
}

/* ===================== Config ===================== */
async function loadConfig() {
    try {
        const cfg = await api('/api/config');
        document.getElementById('baseUrl').value = cfg.base_url || '';
        document.getElementById('apiBaseUrl').value = cfg.api_base_url || '';
        document.getElementById('testUsername').value = cfg.test_username || '';
        document.getElementById('testPassword').value = cfg.test_password || '';
        if (cfg.browser_name) {
            selectedBrowser = cfg.browser_name;
            highlightOption('browserGroup', cfg.browser_name);
        }
    } catch {
        toast('Could not load configuration', 'warning');
    }
}

async function saveConfig() {
    const body = {
        base_url: document.getElementById('baseUrl').value.trim(),
        api_base_url: document.getElementById('apiBaseUrl').value.trim(),
        test_username: document.getElementById('testUsername').value.trim(),
        test_password: document.getElementById('testPassword').value.trim(),
        browser_name: selectedBrowser,
        headless: false,
    };
    try {
        await api('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        toast('Configuration saved successfully', 'success');
    } catch (e) {
        toast('Failed to save: ' + e.message, 'error');
    }
}

function togglePassword() {
    const inp = document.getElementById('testPassword');
    inp.type = inp.type === 'password' ? 'text' : 'password';
}

/* ===================== Browser / Framework select ===================== */
function selectOption(type, el) {
    const group = el.parentElement;
    group.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
    el.classList.add('selected');
    if (type === 'browser') selectedBrowser = el.dataset.value;
    if (type === 'framework') selectedFramework = el.dataset.value;
}

function highlightOption(groupId, value) {
    const group = document.getElementById(groupId);
    if (!group) return;
    group.querySelectorAll('.option-card').forEach(c => {
        c.classList.toggle('selected', c.dataset.value === value);
    });
}

/* ===================== File Upload ===================== */
function handleDragOver(e) {
    e.preventDefault();
    document.getElementById('uploadArea').classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    document.getElementById('uploadArea').classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    document.getElementById('uploadArea').classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) uploadFile(file);
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) uploadFile(file);
}

async function uploadFile(file) {
    const status = document.getElementById('uploadStatus');
    status.style.display = 'block';
    status.className = 'upload-status';
    status.textContent = 'Uploading ' + file.name + '...';

    try {
        const fd = new FormData();
        fd.append('file', file);
        const res = await api('/api/upload-excel', { method: 'POST', body: fd });
        status.className = 'upload-status success';
        status.textContent = 'Uploaded: ' + file.name;
        toast('Excel file uploaded', 'success');
        await loadTestCases();
    } catch (e) {
        status.className = 'upload-status error';
        status.textContent = 'Upload failed: ' + e.message;
        toast('Upload failed', 'error');
    }
}

/* ===================== Test Cases Preview ===================== */
async function loadTestCases() {
    try {
        const cases = await api('/api/test-cases');
        const preview = document.getElementById('tcPreview');
        const list = document.getElementById('tcList');
        if (cases.length > 0) {
            preview.style.display = 'block';
            list.innerHTML = cases.map(tc =>
                `<span class="tc-pill" title="${tc.name} (${tc.steps} steps)">${tc.id}: ${tc.name}</span>`
            ).join('');
        } else {
            preview.style.display = 'none';
        }
    } catch {
        // silently ignore
    }
}

/* ===================== Run / Stop ===================== */
async function runTests() {
    try {
        await api('/api/run-tests', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ method: selectedFramework, browser: selectedBrowser }),
        });
        setUIRunning();
        clearConsole();
        lastLineCount = 0;
        startPolling();
        toast('Test execution started (' + selectedFramework.toUpperCase() + ' / ' + selectedBrowser + ')', 'info');
    } catch (e) {
        toast(e.message, 'error');
    }
}

async function stopTests() {
    try {
        await api('/api/stop-tests', { method: 'POST' });
        toast('Tests stopped', 'warning');
    } catch (e) {
        toast(e.message, 'error');
    }
}

function setUIRunning() {
    document.getElementById('runBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-flex';
    setGlobalStatus('running', 'Running...');
}

function setUIIdle(status, label) {
    document.getElementById('runBtn').style.display = 'inline-flex';
    document.getElementById('stopBtn').style.display = 'none';
    setGlobalStatus(status, label);
}

function setGlobalStatus(state, text) {
    const dot = document.querySelector('#globalStatus .status-dot');
    dot.className = 'status-dot ' + state;
    document.getElementById('statusText').textContent = text;
}

/* ===================== Polling ===================== */
function startPolling() {
    if (polling) clearInterval(polling);
    polling = setInterval(pollStatus, 1200);
    pollStatus();
}

async function pollStatus() {
    try {
        const st = await api('/api/run-status');
        updateConsole(st.output || []);

        if (st.status !== 'running') {
            clearInterval(polling);
            polling = null;
            if (st.status === 'completed') {
                setUIIdle('completed', 'Passed');
                toast('All tests passed!', 'success');
            } else if (st.status === 'failed') {
                setUIIdle('failed', 'Failed');
                toast('Some tests failed. Check console / reports.', 'error');
            } else {
                setUIIdle('stopped', 'Stopped');
            }
            await refreshReports();
        }
    } catch {
        // retry next interval
    }
}

/* ===================== Console ===================== */
function updateConsole(lines) {
    const el = document.getElementById('console');
    if (lines.length === 0 && lastLineCount === 0) return;

    if (lastLineCount === 0) el.innerHTML = '';

    const newLines = lines.slice(lastLineCount);
    for (const raw of newLines) {
        const div = document.createElement('div');
        div.className = 'console-line';
        if (/PASS/i.test(raw)) div.classList.add('pass');
        else if (/FAIL|ERROR/i.test(raw)) div.classList.add('fail');
        else if (/Running:|INFO|==/i.test(raw)) div.classList.add('info');
        div.textContent = raw;
        el.appendChild(div);
    }
    lastLineCount = lines.length;
    el.scrollTop = el.scrollHeight;
}

function clearConsole() {
    const el = document.getElementById('console');
    el.innerHTML = '<div class="console-line muted">Waiting for test execution...</div>';
    lastLineCount = 0;
}

/* ===================== Auto Generator ===================== */
async function generateExcelScripts() {
    const baseUrl = document.getElementById('baseUrl').value.trim();
    const username = document.getElementById('testUsername').value.trim();
    const password = document.getElementById('testPassword').value.trim();
    const maxPagesEl = document.getElementById('maxPagesInput');
    const modeEl = document.getElementById('generationModeInput');
    const maxPages = Math.min(30, Math.max(2, parseInt(maxPagesEl?.value || '12', 10)));
    const generationMode = modeEl?.value || 'auto_login_navigation';

    if (!baseUrl) {
        toast('Please enter URL first', 'warning');
        return;
    }
    if (generationMode === 'auto_login_navigation' && (!username || !password)) {
        toast('Please enter username and password for Auto Login mode', 'warning');
        return;
    }

    try {
        await api('/api/generate-excel-scripts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                base_url: baseUrl,
                username,
                password,
                browser: selectedBrowser,
                max_pages: maxPages,
                generation_mode: generationMode,
            }),
        });
        generationLastLineCount = 0;
        document.getElementById('generatorLog').innerHTML = '<div class="console-line muted">Starting generation...</div>';
        setGeneratorUiRunning();
        startGenerationPolling();
        const prettyMode = generationMode === 'auto_login_navigation'
            ? 'Auto Login + Navigation'
            : generationMode === 'navigation_only'
                ? 'Navigation Only'
                : 'Minimal Smoke';
        toast('Excel generation started (' + prettyMode + ', max pages: ' + maxPages + ')', 'info');
    } catch (e) {
        toast('Generation failed to start: ' + e.message, 'error');
    }
}

function startGenerationPolling() {
    if (generationPolling) clearInterval(generationPolling);
    generationPolling = setInterval(pollGenerationStatus, 1400);
    pollGenerationStatus();
}

async function pollGenerationStatus() {
    try {
        const st = await api('/api/generate-excel-status');
        renderGenerationLogs(st.logs || []);
        document.getElementById('generatorStatus').textContent = 'Status: ' + st.status;

        if (st.status === 'completed') {
            clearInterval(generationPolling);
            generationPolling = null;
            setGeneratorUiCompleted();
            const btn = document.getElementById('downloadGeneratedBtn');
            btn.style.display = 'inline-flex';
            btn.href = '/api/generated-excel/download?ts=' + Date.now();
            await loadTestCases();
            checkPrerequisites();
            toast('Excel generated successfully', 'success');
        } else if (st.status === 'failed') {
            clearInterval(generationPolling);
            generationPolling = null;
            setGeneratorUiIdle();
            toast('Generation failed: ' + (st.error || 'Unknown error'), 'error');
        }
    } catch {
        // retry silently
    }
}

function renderGenerationLogs(lines) {
    const el = document.getElementById('generatorLog');
    if (!el) return;

    if (generationLastLineCount === 0) {
        el.innerHTML = '';
    }
    const newLines = lines.slice(generationLastLineCount);
    for (const raw of newLines) {
        const div = document.createElement('div');
        div.className = 'console-line';
        if (/ERROR|FAIL/i.test(raw)) div.classList.add('fail');
        else if (/Launching|Opening|discovered|generated|Backed up|Profiling/i.test(raw)) div.classList.add('info');
        div.textContent = raw;
        el.appendChild(div);
    }
    generationLastLineCount = lines.length;
    el.scrollTop = el.scrollHeight;
}

function setGeneratorUiRunning() {
    const btn = document.getElementById('generateBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Generating...';
    document.getElementById('downloadGeneratedBtn').style.display = 'none';
    document.getElementById('generatorStatus').textContent = 'Status: running';
}

function setGeneratorUiCompleted() {
    const btn = document.getElementById('generateBtn');
    btn.disabled = false;
    btn.textContent = 'Generate Excel Script';
    document.getElementById('generatorStatus').textContent = 'Status: completed';
}

function setGeneratorUiIdle() {
    const btn = document.getElementById('generateBtn');
    btn.disabled = false;
    btn.textContent = 'Generate Excel Script';
    const status = document.getElementById('generatorStatus');
    if (status.textContent.includes('running')) {
        status.textContent = 'Status: idle';
    }
}

/* ===================== Reports ===================== */
async function refreshReports() {
    try {
        const reports = await api('/api/reports');
        const tbody = document.getElementById('reportsBody');

        if (reports.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="no-data">No reports generated yet. Run tests to see results here.</td></tr>';
            return;
        }

        tbody.innerHTML = reports.map(r => {
            const date = new Date(r.modified).toLocaleString();
            const badge = r.type === 'html'
                ? '<span class="badge badge-html">HTML</span>'
                : '<span class="badge badge-excel">Excel</span>';
            const action = r.type === 'html'
                ? `<a class="btn-link" href="/api/reports/${r.name}" target="_blank">View</a>`
                : `<a class="btn-link" href="/api/reports/${r.name}" download>Download</a>`;
            return `<tr><td>${r.name}</td><td>${date}</td><td>${badge}</td><td>${action}</td></tr>`;
        }).join('');
    } catch {
        // silently ignore
    }
}

/* ===================== Prerequisites ===================== */
async function checkPrerequisites() {
    try {
        const checks = await api('/api/check-prerequisites');

        setPrereq('prPython', checks.python?.installed, checks.python?.version || '');
        setPrereq('prJava', checks.java?.installed, checks.java?.version || '');
        setPrereq('prMaven', checks.maven?.installed, checks.maven?.version || '');

        const exEl = document.getElementById('prExcel');
        if (checks.excel?.exists) {
            exEl.className = 'prereq-item ok';
            exEl.querySelector('.prereq-icon').textContent = '\u2713';
        } else {
            exEl.className = 'prereq-item warn';
            exEl.querySelector('.prereq-icon').textContent = '\u2717';
        }
    } catch {
        // silent
    }
}

function setPrereq(id, installed, version) {
    const el = document.getElementById(id);
    if (installed) {
        el.className = 'prereq-item ok';
        el.querySelector('.prereq-icon').textContent = '\u2713';
        el.title = version;
    } else {
        el.className = 'prereq-item fail';
        el.querySelector('.prereq-icon').textContent = '\u2717';
        el.title = 'Not installed';
    }
}

/* ===================== Toast ===================== */
function toast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const el = document.createElement('div');
    el.className = 'toast toast-' + type;
    el.textContent = message;
    container.appendChild(el);
    requestAnimationFrame(() => el.classList.add('show'));
    setTimeout(() => {
        el.classList.remove('show');
        setTimeout(() => el.remove(), 350);
    }, 3500);
}
