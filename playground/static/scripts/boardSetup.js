import {getCookie} from "./biscuits.js"
import { resetBoard, sendMoveToServer, getBestMove, isMoveLegal } from "./chessRequests.js";

export var board;

/* -------------------------------------------------------
    Initializes a chessboard.js instance
------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function() {
    board = Chessboard('play-board-svg', {
        draggable: true,
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd,
        dropOffBoard: 'snapback',
        position: 'start',
        pieceTheme: "/static/chessboard/img/chesspieces/wikipedia/{piece}.png"
    });
});


/* -------------------------------------------------------
--------------- HANDLES DRAGGABLE MOVES ------------------
------------------------------------------------------- */
function onDragStart(source, piece, position, orientation) {

}

function onDrop(source, target) {
    let uci_move = source + target;
    isMoveLegal(uci_move)
        .then(data => {
            console.log("Move legality response:", data);
            if (data.is_legal) {
                return sendMoveToServer(uci_move);
            } else {
                console.warn("Illegal move attempted:", uci_move);
                return Promise.reject("Illegal move"); // Prevents `getBestMove` from running
            }
        })
        .then(() => getBestMove())
        .catch(error => console.error("Error:", error));
}

function onSnapEnd() {

}

/* -------------------------------------------------------
--------------- HANDLES CLICKABLE MOVES ------------------
------------------------------------------------------- */
let selectedSquare = null;
const highlightedClassName = "highlight1-32417";
const chessPieceClassName = "piece-417db";

// Listens when a square was clicked
document.getElementById("play-board-svg").addEventListener("click", function(event) {
    let square = getSquareFromEvent(event);  // Detect clicked square
    if (!square) return;

    if (selectedSquare === null) {
        selectedSquare = square;  // Select piece
        highlightSquare(selectedSquare);  // Add UI highlight
    } else {
        let uci_move = selectedSquare + square;
        isMoveLegal(uci_move)
            .then(data => {
                console.log("Move legality response:", data);
                if (data.is_legal) {
                    return sendMoveToServer(uci_move);
                } else {
                    console.warn("Illegal move attempted:", uci_move);
                    return Promise.reject("Illegal move"); // Prevents `getBestMove` from running
                }
            })
            .then(() => getBestMove())
            .catch(error => console.error("Error:", error));

        selectedSquare = null;  // Reset selection
        clearHighlights();
    }
});

document.getElementById('play-info-player-option-reset').addEventListener('click', function() {
    resetBoard();
});

function getSquareFromEvent(event) {
    let boardRect = document.getElementById("play-board-svg").getBoundingClientRect();
    let [x, y] = [event.clientX - boardRect.left, event.clientY - boardRect.top];
    let squareSize = boardRect.width / 8;
    let [file, rank] = [Math.floor(x / squareSize), 7 - Math.floor(y / squareSize)];
    return "abcdefgh"[file] + (rank + 1);
}

function highlightSquare(square) {
    document.querySelector(`[data-square="${square}"]`)?.classList.add(highlightedClassName);
}

function clearHighlights() {
    document.querySelectorAll("."+highlightedClassName).forEach(el => el.classList.remove(highlightedClassName));
}
