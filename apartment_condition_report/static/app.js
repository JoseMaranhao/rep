const form = document.querySelector('#report-form');
const input = document.querySelector('#photos');
const selected = document.querySelector('#selected');
const status = document.querySelector('#status');
const button = document.querySelector('#submit');
const dropZone = document.querySelector('#drop-zone');

function updateSelection(files) {
  const images = [...files].filter(file => file.type.startsWith('image/') || /\.(jpe?g|png|webp|heic)$/i.test(file.name));
  selected.textContent = images.length ? `${images.length} photo${images.length === 1 ? '' : 's'} selected.` : 'No supported photos selected.';
}
input.addEventListener('change', () => updateSelection(input.files));
['dragenter', 'dragover'].forEach(event => dropZone.addEventListener(event, e => { e.preventDefault(); dropZone.classList.add('dragging'); }));
['dragleave', 'drop'].forEach(event => dropZone.addEventListener(event, e => { e.preventDefault(); dropZone.classList.remove('dragging'); }));
dropZone.addEventListener('drop', event => { input.files = event.dataTransfer.files; updateSelection(input.files); });
form.addEventListener('submit', async event => {
  event.preventDefault();
  if (!input.files.length) { status.textContent = 'Choose at least one photo first.'; return; }
  const data = new FormData();
  data.append('title', form.title.value);
  data.append('analyze', document.querySelector('#analyze').checked ? 'true' : 'false');
  [...input.files].forEach(file => data.append('photos', file, file.webkitRelativePath || file.name));
  button.disabled = true; status.textContent = 'Creating your report package…';
  try {
    const response = await fetch('/api/report', { method: 'POST', body: data });
    if (!response.ok) throw new Error((await response.json()).error || 'Unable to create the report.');
    const link = document.createElement('a'); link.href = URL.createObjectURL(await response.blob()); link.download = 'apartment-condition-report.zip'; link.click(); URL.revokeObjectURL(link.href);
    status.textContent = 'Download ready. Unzip it, review report.pdf and keep the evidence folder.';
  } catch (error) { status.textContent = error.message; }
  finally { button.disabled = false; }
});
