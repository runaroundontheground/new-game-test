// this file is used only for testing things

function consoleLogAAAA(message) {
    let myConsole = document.getElementById("console")
    myConsole.innerHTML += message + "<br />"
    myConsole.scrollTop = myConsole.scrollHeight
};


let testObject = {
    "1": 1,
    "2": 2
}

for 