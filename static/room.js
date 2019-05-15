'use strict';

const canvas /*: HTMLCanvasElement*/ = document.getElementById('canvas');
const context = canvas.getContext('2d');

const room_id /*: string*/ = window.sessionStorage.getItem('room_id');
const player_id /*: string*/ = window.sessionStorage.getItem('player_id');
const name /*: string*/ = window.sessionStorage.getItem('name');

const minX = canvas.getBoundingClientRect().left;
const minY = canvas.getBoundingClientRect().top;

let mouseDown = false;
document.addEventListener('mousedown', () => {mouseDown = true;});
document.addEventListener('mouseup', () => {mouseDown = false;});

var send = (payload, url, method, callback) => {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    const data = JSON.stringify(payload)
    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = xhr.responseText;
            if (response === '') {
                return;
            }
            const result = JSON.parse(xhr.responseText);
            callback(result);
        }
    }
    xhr.send(data);
}

var clear = () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
}

var drawCircle = (x /*: number*/, y /*: number*/, r /*: number*/) => {
    context.beginPath();
    context.arc(x, y, r, 0, 2 * Math.PI);
    context.fill();
};

let drawRequestId;

var draw = (e /*: MouseEvent*/) => {
    window.cancelAnimationFrame(drawRequestId);
    if (!mouseDown) {
        return;
    }
    context.fillStyle = 'red';
    const x = e.clientX - minX;
    const y = e.clientY - minY;
    drawCircle(x, y, 10);
    send({
        'room_id': room_id,
        'player_id': player_id,
        'point': {
            'x': x,
            'y': y,
        },
    }, '/update', 'POST', () => {});
    drawRequestId = window.requestAnimationFrame(() => draw(e));
};

document.addEventListener('mousedown', draw);
document.addEventListener('mousemove', draw);

let updateRequestId;
let draw_id = '';

// For debugging
let dbg = false;

var updateCanvas = () => {
    window.cancelAnimationFrame(updateRequestId);
    // For debugging
    if (!dbg) {
        return;
    }
    send({
        'room_id': room_id,
        'draw_id': draw_id,
    }, '/canvas', 'POST', ({
        'new_draw_id': new_draw_id,
        'point': {
            'x': x,
            'y': y,
            'color': color,
        },
    }) => {
        draw_id = new_draw_id;
        context.fillStyle = color;
        drawCircle(x, y, 10);
    });
    updateRequestId = window.requestAnimationFrame(updateCanvas);
};

