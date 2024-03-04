// this file is used only for testing things

function consoleLog(message) {
    let myConsole = document.getElementById("console")
    myConsole.innerHTML += message + "<br />"
    myConsole.scrollTop = myConsole.scrollHeight
};


/*
class test {
    constructor() {
        this.a = "1"
        this.testFunction = this.testFunction.bind(this);
    }
    testFunction() {
        consoleLog(this.a);
        this.a = 5;
        consoleLog(this.a);
    }
}


let testing = new test();

testing.testFunction();
*/
