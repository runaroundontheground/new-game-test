

let myConsole = document.getElementById("console");


function consoleLogAAA(message) {
    myConsole.innerHTML += message + "<br />";
    myConsole.scrollTop = myConsole.scrollHeight;
};

window.onerror = function (message, source, lineno, colno, error) {
    consoleLogAAA(
        message + "<br>"
        + "source: " + source + "<br>"
        + "line number: " + lineno + "<br>"
        + "column number: " + colno + "<br>"
    );
};


