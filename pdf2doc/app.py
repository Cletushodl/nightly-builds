#!/usr/bin/env python3
"""PDF to DOCX converter — drag-and-drop web app."""

import os
import tempfile
from flask import Flask, request, send_file, render_template_string

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PDF → DOCX</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, system-ui, sans-serif; background: #0a0a0a; color: #e0e0e0; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
.container { text-align: center; width: 90%; max-width: 500px; }
h1 { font-size: 2rem; margin-bottom: 0.5rem; }
h1 span { color: #666; }
.sub { color: #666; margin-bottom: 2rem; font-size: 0.9rem; }
.dropzone {
    border: 2px dashed #333; border-radius: 16px; padding: 60px 20px;
    cursor: pointer; transition: all 0.2s; position: relative;
}
.dropzone:hover, .dropzone.over { border-color: #4a9eff; background: #0d1a2a; }
.dropzone input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
.icon { font-size: 3rem; margin-bottom: 1rem; }
.label { font-size: 1.1rem; color: #999; }
.status { margin-top: 1.5rem; min-height: 2rem; }
.spinner { display: inline-block; width: 20px; height: 20px; border: 2px solid #333; border-top-color: #4a9eff; border-radius: 50%; animation: spin 0.6s linear infinite; vertical-align: middle; margin-right: 8px; }
@keyframes spin { to { transform: rotate(360deg); } }
.error { color: #ff4a4a; }
.success { color: #4aff7f; }
</style>
</head>
<body>
<div class="container">
    <h1>PDF <span>→</span> DOCX</h1>
    <p class="sub">Drop a PDF, get a Word doc</p>
    <div class="dropzone" id="dropzone">
        <div class="icon">📄</div>
        <div class="label">Drop PDF here or tap to browse</div>
        <input type="file" accept=".pdf,application/pdf" id="fileInput">
    </div>
    <div class="status" id="status"></div>
</div>
<script>
const dz = document.getElementById('dropzone');
const fi = document.getElementById('fileInput');
const st = document.getElementById('status');

['dragover','dragenter'].forEach(e => dz.addEventListener(e, ev => { ev.preventDefault(); dz.classList.add('over'); }));
['dragleave','drop'].forEach(e => dz.addEventListener(e, () => dz.classList.remove('over')));

dz.addEventListener('drop', ev => { ev.preventDefault(); if (ev.dataTransfer.files[0]) convert(ev.dataTransfer.files[0]); });
fi.addEventListener('change', () => { if (fi.files[0]) convert(fi.files[0]); });

async function convert(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) { st.innerHTML = '<span class="error">Not a PDF</span>'; return; }
    st.innerHTML = '<span class="spinner"></span> Converting...';
    const fd = new FormData();
    fd.append('file', file);
    try {
        const r = await fetch('/convert', { method: 'POST', body: fd });
        if (!r.ok) { st.innerHTML = `<span class="error">${(await r.json()).error || 'Failed'}</span>`; return; }
        const blob = await r.blob();
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = file.name.replace(/\.pdf$/i, '.docx');
        a.click();
        URL.revokeObjectURL(a.href);
        st.innerHTML = '<span class="success">✓ Done — check downloads</span>';
    } catch (e) { st.innerHTML = `<span class="error">Error: ${e.message}</span>`; }
    fi.value = '';
}
</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/convert', methods=['POST'])
def convert():
    from pdf2docx import Converter
    f = request.files.get('file')
    if not f or not f.filename.lower().endswith('.pdf'):
        return {'error': 'Please upload a PDF file'}, 400
    
    tmp_in = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    tmp_out = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
    try:
        f.save(tmp_in.name)
        cv = Converter(tmp_in.name)
        cv.convert(tmp_out.name)
        cv.close()
        out_name = f.filename.rsplit('.', 1)[0] + '.docx'
        return send_file(tmp_out.name, as_attachment=True, download_name=out_name,
                        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        os.unlink(tmp_in.name)
        # tmp_out cleaned up after send

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
