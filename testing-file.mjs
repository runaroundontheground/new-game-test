// this file is used only for testing things

function consoleLog(message) {
    let myConsole = document.getElementById("console")
    myConsole.innerHTML += message + "<br />"
    myConsole.scrollTop = myConsole.scrollHeight
};

let test = (1, 5, 3)
let test2 = toString(test)

consoleLog(test2)



