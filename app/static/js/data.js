const artists = window._data.top_artists;
const albums = window._data.top_albums;
const songs = window._data.top_songs;

let currentTab = 'artists';
let useListenTime = false;

function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll('nav button').forEach(btn => btn.classList.remove('active'));
    document.getElementById('btn-' + tab).classList.add('active');
    renderData();
}

function toggleView() {
    useListenTime = document.getElementById('toggleView').checked;
    renderData();
}

function renderData() {
    const container = document.getElementById('dataDisplay');
    let data = [];

    if (currentTab === 'artists') data = artists;
    if (currentTab === 'albums') data = albums;
    if (currentTab === 'songs') data = songs;

    let html = '<table><thead><tr>';
    html += '<th>Name</th>';
    if (currentTab !== 'artists') html += '<th>Artist</th>';
    html += `<th>${useListenTime ? 'Listen Time (min)' : 'Streams'}</th>`;
    html += '</tr></thead><tbody>';

    data.forEach(item => {
        html += '<tr>';
        html += `<td>${item.name}</td>`;
        if (currentTab !== 'artists') html += `<td>${item.artist || item.artist_name || '-'}</td>`;
        const metric = useListenTime
            ? Math.round((item.listen_time || 0) / 60000)
            : (item.streams || 0);
        html += `<td>${metric}</td>`;
        html += '</tr>';
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

document.addEventListener("DOMContentLoaded", () => {
    renderData();
});
