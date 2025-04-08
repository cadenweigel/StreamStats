let artists = window._data.top_artists;
let albums = window._data.top_albums;
let songs = window._data.top_songs;

let currentTab = 'artists';
let currentSortField = 'streams';

function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll('nav button').forEach(btn => btn.classList.remove('active'));
    document.getElementById('btn-' + tab).classList.add('active');
    fetchAndRender();
}

function formatTime(ms) {
    let totalSeconds = Math.floor((ms || 0) / 1000);
    let hours = Math.floor(totalSeconds / 3600);
    let minutes = Math.floor((totalSeconds % 3600) / 60);
    let seconds = totalSeconds % 60;

    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function truncate(str, maxLength = 30) {
    if (!str) return '';
    return str.length > maxLength ? str.slice(0, maxLength - 1) + '…' : str;
}

function fetchAndRender() {
    fetch(`/api/data?sort=${currentSortField}`)
        .then(res => res.json())
        .then(data => {
            artists = data.top_artists;
            albums = data.top_albums;
            songs = data.top_songs;

            window._data.top_artists = artists;
            window._data.top_albums = albums;
            window._data.top_songs = songs;

            renderData();
        })
        .catch(err => console.error("Failed to fetch sorted data:", err));
}

function setSort(field) {
    if (currentSortField !== field) {
        currentSortField = field;
        fetchAndRender();
    }
}

function renderHeader(label, field) {
    const isActive = currentSortField === field;
    const arrow = '⬇️';
    const style = isActive
        ? 'font-weight: bold; text-decoration: underline;'
        : 'color: #888;';
    return `<th onclick="setSort('${field}')" style="cursor:pointer; ${style}">
                ${label} <span style="display:inline-block; width: 1em;">${arrow}</span>
            </th>`;
}

function renderData() {
    const container = document.getElementById('dataDisplay');
    let data = [];

    if (currentTab === 'artists') data = artists;
    if (currentTab === 'albums') data = albums;
    if (currentTab === 'songs') data = songs;

    let html = '<table><thead><tr>';
    html += '<th>#</th>';
    html += renderHeader('Name', 'name');
    if (currentTab !== 'artists') html += '<th>Artist</th>';
    html += renderHeader('Streams', 'streams');
    html += renderHeader('Listen Time', 'listen_time');
    html += '</tr></thead><tbody>';

    data.forEach((item, index) => {
        html += '<tr>';
        html += `<td>${index + 1}</td>`;
        html += `<td title="${item.name}">${truncate(item.name)}</td>`;
        if (currentTab !== 'artists') {
            const artistValue = item.artist || item.artist_name || '—';
            html += `<td title="${artistValue}">${truncate(artistValue)}</td>`;
        }
        html += `<td>${item.streams || 0}</td>`;
        html += `<td>${formatTime(item.listen_time)}</td>`;
        html += '</tr>';
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

document.addEventListener("DOMContentLoaded", () => {
    renderData();
});
