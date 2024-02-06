

const myConsole = document.getElementById("console");


function consoleLog(message) {
    myConsole.innerHTML += message + "<br />"
    myConsole.scrollTop = myConsole.scrollHeight
};

document.onerror = function (message, source, lineno, colno, error) {
    consoleLog(message);
};

window.onerror = function (message, source, lineno, colno, error) {
    consoleLog(message);
};


document.addEventListener("keydown", function (event) {
    consoleLog(event.key);
});