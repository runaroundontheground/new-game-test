// this file is used only for testing things

function consoleLogAAAA(message) {
    let myConsole = document.getElementById("console")
    myConsole.innerHTML += message + "<br />"
    myConsole.scrollTop = myConsole.scrollHeight
};
/*
class testingClass {
    constructor() {
        this.a = 5
        this.b = 3
    }
}
let testingClassObject = new testingClass()
let testObject = {
    "a": 1,
    "b": 2
}

for (let entry of Object.entries(testingClassObject)) {
    let property = entry[0]
    let key = entry[1]
    consoleLogAAAA(property + " that was property");
    consoleLogAAAA(key + " that was key");
}
*/