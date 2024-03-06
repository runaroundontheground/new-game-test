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
        this.x = 0
        this.testFunction = this.testFunction.bind(this);
        this.otherTestFunction = function (change = 0) {
            this.x += change;
            consoleLog(this.x);
        }
    }
    testFunction() {
        consoleLog(this.a);
        this.a = 5;
        consoleLog(this.a);
        this.newFunction = function() {
            this.x += 5;
        }
        this.newFunction()
    }
}
let testing = new test();


testing.otherTestFunction(3);

testing.testFunction();
testing.otherTestFunction(-1);*/

