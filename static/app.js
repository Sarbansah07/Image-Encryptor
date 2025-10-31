(() => {
  const fileInput = document.getElementById('fileInput');
  const dropArea = document.getElementById('dropArea');
  const preview = document.getElementById('preview');
  const mainForm = document.getElementById('mainForm');
  const progressWrap = document.getElementById('progressWrap');
  const progressBar = document.getElementById('progressBar');
  const resultArea = document.getElementById('resultArea');
  const submitBtn = document.getElementById('submitBtn');
  const toggleKey = document.getElementById('toggleKey');
  const keyInput = document.getElementById('keyInput');

  // Drag & drop
  ['dragenter','dragover'].forEach(evt => {
    dropArea.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); dropArea.classList.add('dragover'); });
  });
  ['dragleave','drop'].forEach(evt => {
    dropArea.addEventListener(evt, e => { e.preventDefault(); e.stopPropagation(); dropArea.classList.remove('dragover'); });
  });
  dropArea.addEventListener('drop', e => {
    const f = e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) fileInput.files = e.dataTransfer.files;
    showPreview();
  });
  dropArea.addEventListener('click', (e)=> {
    // If the native file input was clicked, don't trigger another click — avoids double popup
    if (e.target === fileInput) return;
    fileInput.click();
  });
  fileInput.addEventListener('change', showPreview);

  function showPreview(){
    const f = fileInput.files && fileInput.files[0];
    if (!f) { preview.classList.add('d-none'); return; }
    if (!f.type.startsWith('image')) { preview.classList.add('d-none'); return; }
    const reader = new FileReader();
    reader.onload = (ev) => {
      preview.src = ev.target.result;
      preview.classList.remove('d-none');
    };
    reader.readAsDataURL(f);
  }

  // Toggle key visibility (simple text toggle)
  toggleKey.addEventListener('click', ()=>{
    if (keyInput.type === 'password') { keyInput.type = 'text'; toggleKey.textContent = 'Hide'; }
    else { keyInput.type = 'password'; toggleKey.textContent = 'Show'; }
  });

  // Form submit with XHR to get progress and blob response
  mainForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    resultArea.innerHTML = '';
    const fd = new FormData(mainForm);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/', true);
    xhr.responseType = 'blob';

    xhr.upload.onprogress = (ev) => {
      if (ev.lengthComputable) {
        const pct = Math.round(ev.loaded / ev.total * 100);
        progressWrap.classList.remove('d-none');
        progressBar.style.width = pct + '%';
      }
    };
    xhr.onload = () => {
      progressBar.style.width = '100%';
      setTimeout(()=>{ progressWrap.classList.add('d-none'); progressBar.style.width = '0%'; }, 600);
      if (xhr.status !== 200) {
        // try to read text message
        const reader = new FileReader();
        reader.onload = ()=> { resultArea.innerHTML = `<div class="alert alert-danger">${reader.result}</div>`; };
        reader.readAsText(xhr.response);
        return;
      }

      const disposition = xhr.getResponseHeader('Content-Disposition') || '';
      let filename = '';
      const m = /filename="?([^";]+)"?/.exec(disposition);
      if (m) filename = m[1];
      if (!filename) filename = (fd.get('file') && fd.get('file').name) || ('result-' + Date.now());

      const blob = xhr.response;
      const url = URL.createObjectURL(blob);

      // create download link and auto-click
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.className = 'btn btn-success';
      a.textContent = 'Download processed file';
      resultArea.appendChild(a);
      // if image, show inline preview
      const ct = xhr.getResponseHeader('Content-Type') || '';
      if (ct.startsWith('image')){
        const img = document.createElement('img');
        img.src = url;
        img.className = 'img-preview mt-3';
        resultArea.appendChild(img);
      }

      // auto click to download
      setTimeout(()=>{ a.click(); }, 150);
    };

    xhr.onerror = ()=>{ resultArea.innerHTML = '<div class="alert alert-danger">Network or server error</div>'; };
    xhr.send(fd);
  });
})();
