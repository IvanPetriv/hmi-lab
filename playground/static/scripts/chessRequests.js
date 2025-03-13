import {getCookie} from "./biscuits.js"
import {board} from "./boardSetup.js";


// Checks if the move is legal
export function isMoveLegal(move) {
    return fetch(`./is_legal/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: new URLSearchParams({
            move: move
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


// Sends a played move to the Python chess engine
export function sendMoveToServer(move) {
    fetch(`./move/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: new URLSearchParams({
            move: move
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.fen) {
            board.position(data.fen);
        }
    })
    .catch(error => console.error("Error:", error));
}


// Gets the best move
export function getBestMove() {
    fetch(`./best_move/`, {
        method: "GET",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.fen) {
            board.position(data.fen);
        }
        console.log(data);
    })
    .catch(error => console.error("Error:", error));
}


// Resets the board
export function resetBoard() {
    fetch('./reset_game/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.fen) {
            board.position(data.fen);
            console.log("Game reset to:", data.fen);
        } else {
            console.error('Failed to reset the game.');
        }
    })
    .catch(error => console.error('Error:', error));
}
