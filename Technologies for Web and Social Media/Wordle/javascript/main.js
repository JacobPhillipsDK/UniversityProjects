let CorrectWord = String("space").toUpperCase() // Correct guess and ensures the correct guess is in uppercase
// User defined values
let NUMBER_OF_GUESSES = 6; // Number of guesses allowed
let LEN_OF_WORD = CorrectWord.length; // Length of word to guess // Will be based on random word selection

// import {wordlist} from "./wordlist";

// Global statements and variables
let NUMBER_OF_ROWS = NUMBER_OF_GUESSES;
let GuessRemaining = NUMBER_OF_GUESSES;
let currentGuess = [];
let nextLetter = 0;

// Debug Mode
let DEBUG_MODE = true;


function createBoard() {
    let board = document.getElementById("game-board"); // Get the game board
    document.getElementsByTagName('span').textContent = NUMBER_OF_GUESSES; // Debug


    for (let i = 0; i < NUMBER_OF_ROWS; i++) {  // For loop based on the number of guesses
        let row = document.createElement("div") // Create a row with div tag
        row.className = "letter-row"; // Add class to the row

        for (let j = 0; j < LEN_OF_WORD; j++) { // Create 5 divs in each row
            let box = document.createElement("div") // Create a box with div tag
            box.className = "letter-box" // Add class to the box
            row.appendChild(box) // Append the box to the row
        }
        board.appendChild(row) // Append the row to the board
    }
}


function insertLetterFromPressedKey(pressedKey) {
    if (nextLetter === 5) {
        return
    }
    pressedKey = pressedKey.toUpperCase() // Convert the key to uppercase
    let row = document.getElementsByClassName("letter-row")[NUMBER_OF_ROWS - GuessRemaining] // Get the row
    let box = row.children[nextLetter] // Get the box
    box.textContent = pressedKey // Insert the letter into the box
    box.classList.add("filled-box") // Add class to the box
    currentGuess.push(pressedKey) // Add the letter to the currentGuess array
    nextLetter += 1 // Increment the nextLetter
}


function deleteInsertedLetter() {
    let row = document.getElementsByClassName("letter-row")[NUMBER_OF_ROWS - GuessRemaining]
    let box = row.children[nextLetter - 1]
    box.textContent = ""
    box.classList.remove("filled-box")
    currentGuess.pop()
    nextLetter -= 1
}


function ValidateLetters(currentGuess, correctWord) {
    let row = document.getElementsByClassName("letter-row")[NUMBER_OF_ROWS - GuessRemaining]
    let correctWordArray = correctWord.split("") // Convert the correct word to an array
    let currentGuessArray = currentGuess.split("") // Convert the current guess to an array
    if (DEBUG_MODE) { // Debug Mode
        console.log("currentGuessArray : " + currentGuessArray)
        console.log("correctWordArray :" + correctWordArray)
    }

    for (let i = 0; i < currentGuessArray.length; i++) {
        let letterPosition = correctWordArray.indexOf(currentGuessArray[i]) // Get the position of the letter in the correct word
        let letterPosition2 = correctWordArray.indexOf(correctWordArray[i]) // Get the position of the letter in the correct word
        let box = row.children[i]
        for (let j = 0; j < correctWordArray.length; j++) {
            if (letterPosition === letterPosition2 && currentGuessArray[i] === correctWordArray[j]) {
                box.classList.add("correctLetterPlacement") // Add class to the box if the letter is correct
            } else if (currentGuessArray[i] === correctWordArray[j]) {
                if (DEBUG_MODE) { // Debug Mode
                    console.log("currentGuessArray : " + currentGuessArray[i] + " correctWordArray : " + correctWordArray[j])
                    console.log("letterPosition : " + letterPosition)
                    console.log("letterPosition2 : " + letterPosition2)
                }
                box.classList.add("correctLetter") // Add class to the box if the letter is correct
                if (DEBUG_MODE) { // Debug Mode
                    console.log("letterPosition === letterPosition2 : " + (letterPosition === letterPosition2))
                }
            }
        }
        if (letterPosition === -1) {
            box.classList.add("wrongLetterGuess") // Add class to the box if the letter is incorrect
        }
    }
}


function ValidateWord(CurrentGuess, CorrectWord) {
    let correctWord = String(CorrectWord).toUpperCase();
    let guess = CurrentGuess.join("").toUpperCase();


    if (DEBUG_MODE) { // Debug Mode
        console.log("CorrectWord: " + correctWord)
        console.log("CurrentGuess: " + guess)
    }

    if (guess === correctWord) { // If the guess is correct
        ValidateLetters(guess, correctWord)
        alert("You Guessed the Word!")
        location.reload();
        if (DEBUG_MODE) {
            console.log("Correct Word")
            location.reload();

        }
    } else {
        ValidateLetters(guess, correctWord)
        if (DEBUG_MODE) {
            console.log("Incorrect Guess")
            console.log("Next Row")
        }
        nextRow()
        if (DEBUG_MODE) {
            console.log("GuessRemaining: " + GuessRemaining)
        }
        if (GuessRemaining === 0) {
            alert("You Lose! " + "The Correct word was : " + correctWord.toLowerCase())
            return location.reload();//
        }
    }
}


function nextRow() {
    GuessRemaining = GuessRemaining - 1
    nextLetter = 0
    currentGuess = []
}


document.addEventListener("keyup", (user_input) => { // Add event listener to the keyup event
    let pressedKey = user_input.key// Get the pressed key
    pressedKey = pressedKey.toUpperCase() // Convert the pressed key to uppercase
    let pressedKeyMatch = user_input.key.match(/[a-z]/gi) // Match the key pressed to a letter

    // Evil BACKSPACE : Because of every input is read in UPPERCASE then BACKSPACE also needs to be read in UPPERCASE otherwise not working
    if (pressedKey === 'BackSpace'.toUpperCase() && nextLetter !== 0) { // If the pressed key is backspace and the next letter is not 0
        deleteInsertedLetter()
        if (DEBUG_MODE) {
            console.log("Backspace Pressed deleting letter")
        }
        return
    }

    if (!pressedKeyMatch || pressedKeyMatch.length > 1) { // If the pressed key is not a letter
        if (DEBUG_MODE) {
            console.log("Not a letter :" + pressedKey)
        }
    } else {
        insertLetterFromPressedKey(pressedKey) // Call the function to insert the letter
    }

    if (pressedKey === "Enter".toUpperCase() && nextLetter === LEN_OF_WORD && currentGuess.length === LEN_OF_WORD) { // If the pressed key is enter and the next letter is equal to the length of the word
        if (DEBUG_MODE) {
            console.log(String("Running Validator").toUpperCase())
            console.log("currentGuess in raw form : " + currentGuess)
        }
        ValidateWord(currentGuess, CorrectWord)
    }

})

createBoard() // Create the game board