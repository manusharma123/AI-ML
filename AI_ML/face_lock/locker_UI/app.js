async function captureFace() {
  // Calls the /register-user endpoint
  document.getElementById('registerResult').innerText = 'Registering...';
  const res = await fetch('http://127.0.0.1:8001/register-user', { method: 'POST' });
  const data = await res.json();
  document.getElementById('registerResult').innerText = data.status || 'Registration complete';
}

async function startMonitor() {
  // Calls the /monitor-unlock endpoint
  document.getElementById('monitorResult').innerText = 'Monitoring...';
  const folderPath = document.getElementById('folderPath').value;
  const formData = new FormData();
  formData.append('folder_path', folderPath);
  const res = await fetch('http://127.0.0.1:8001/monitor-unlock', { method: 'POST', body: formData });
  const data = await res.json();
  document.getElementById('monitorResult').innerText = data.status || 'Monitoring complete';
}

async function lockFolder() {
  const path = document.getElementById('folderPath').value;
  const formData = new FormData();
  formData.append('folder_path', path);
  const res = await fetch('http://127.0.0.1:8001/lock-folder', { method: 'POST', body: formData });
  const data = await res.json();
  document.getElementById('lockResult').innerText = data.status || `Locked folder: ${path}`;
}

async function unlockFolder() {
  const path = document.getElementById('folderPath').value;
  const formData = new FormData();
  formData.append('folder_path', path);
  const res = await fetch('http://127.0.0.1:8001/unlock-folder', { method: 'POST', body: formData });
  const data = await res.json();
  document.getElementById('lockResult').innerText = data.status || `Unlocked folder: ${path}`;
}


async function loadDocuments() {
  const resultEl = document.getElementById('documentResult');
  resultEl.innerText = 'Loading documents...';

  try {
    const res = await fetch('http://127.0.0.1:8001/documents');
    const data = await res.json();

    if (!data || data.length === 0) {
      resultEl.innerText = 'No documents found';
      return;
    }

    resultEl.innerText = JSON.stringify(data, null, 2);
  } catch (error) {
    resultEl.innerText = 'Error loading documents';
  }
}


window.onload = function() {
  // Optionally, fetch and display folder status here
  loadDocuments();
};