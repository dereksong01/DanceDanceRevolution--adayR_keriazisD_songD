'use strict';

var send = (payload, url, method, callback) => {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    const data = JSON.stringify(payload)
    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const result = JSON.parse(xhr.responseText);
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

var join = (room_id, name) => {
    if (name === '' || room_id === '') {
        return;
    }
    send({
        'name': name,
        'room_id': room_id,
    }, '/join', 'POST', ({'player_id': player_id}) => {
        window.sessionStorage.setItem('room_id', room_id);
        window.sessionStorage.setItem('player_id', player_id);
        window.sessionStorage.setItem('name', name);
        window.location.replace(`/room/${room_id}`);
    });
}

var create = (name) => {
    if (name === '') {
        return;
    }
    send({'name': name}, '/create', 'POST',
        ({'room_id': room_id, 'player_id': player_id}) => {
            window.sessionStorage.setItem('room_id', room_id);
            window.sessionStorage.setItem('player_id', player_id);
            window.sessionStorage.setItem('name', name);
            window.location.replace(`/room/${room_id}`);
        }
    );
};

createButton.addEventListener('click', (e) => {
    e.preventDefault();
    create(createName.value);
});

joinButton.addEventListener('click', (e) => {
    e.preventDefault();
    join(joinRoomId.value, joinName.value);
});

