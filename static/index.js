'use strict';

var send = (payload, url, method, callback) => {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    let data = JSON.stringify(payload)
    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let result = JSON.parse(xhr.responseText);
            callback(result);
        }
    }
    xhr.send(data);
}

const createName = document.getElementById('createName');
const createButton = document.getElementById('createButton');

const joinName = document.getElementById('joinName');
const joinRoomId = document.getElementById('joinRoomId');
const joinButton = document.getElementById('joinButton');

createButton.addEventListener('click', (e) => {
    e.preventDefault();
    if (createName.value === '') {
        return;
    }
    send({'name': createName.value}, '/create', 'POST', console.log);
});

joinButton.addEventListener('click', (e) => {
    e.preventDefault();
    if (joinName.value === '' || joinRoomId.value === '') {
        return;
    }
    send({
        'name': joinName.value,
        'room_id': joinRoomId.value,
    }, '/join', 'POST', console.log);
});


