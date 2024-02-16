// this file is used only for testing things

function consoleLog(message) {
    let myConsole = document.getElementById("console")
    myConsole.innerHTML += message + "<br />"
    myConsole.scrollTop = myConsole.scrollHeight
};




class testingClass {
    constructor() {
        this.a = 5
        this.b = 3
        this.testingClassFunction = function () {
            return "test value";
        }

        this.hotbar = [this.a, this.b];
    }
}
let testingClassObject = new testingClass()
let testObject = {
    "a": 1,
    "b": 2
}



