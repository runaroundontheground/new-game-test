

let myConsole = document.getElementById("console");


function consoleLogAAA(message) {
    myConsole.innerHTML += message + "<br />";
    myConsole.scrollTop = myConsole.scrollHeight;
};

document.onerror = function (message, source, lineno, colno, error) {
    consoleLogAAA(message);
};

window.onerror = function (message, source, lineno, colno, error) {
    consoleLogAAA(message);
};


