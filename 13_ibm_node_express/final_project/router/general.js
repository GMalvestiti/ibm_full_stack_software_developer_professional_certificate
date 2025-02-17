const express = require('express');
let books = require("./booksdb.js");
let isValid = require("./auth_users.js").isValid;
let users = require("./auth_users.js").users;
const axios = require('axios');

const public_users = express.Router();

const URL = 'https://gustavosmalv-5000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai';

public_users.post("/register", (req, res) => {
    const username = req.body.username;
    const password = req.body.password;

    if (username && password) {
        if (!isValid(username)) { 
            users.push({"username": username, "password": password});
            return res.status(200).json({message: "User successfully registred. Now you can login."});
        } else {
            return res.status(404).json({message: "User already exists!"});    
        }
    } 

    return res.status(404).json({message: "Unable to register user."});
});

// Get the book list available in the shop
public_users.get('/', function (req, res) {
    res.status(200).json(books);
});

// Get book details based on ISBN
public_users.get('/isbn/:isbn', function (req, res) {
    const isbn = req.params.isbn;
    res.status(200).json(books[isbn]);
});
  
// Get book details based on author
public_users.get('/author/:author', function (req, res) {
    const author = req.params.author;
    let selectedBooks = {};
    for (let bookId in books) {
        if (books[bookId].author == author) {
            selectedBooks[bookId] = books[bookId];
        } 
    }
    res.status(200).json(selectedBooks);
});

// Get all books based on title
public_users.get('/title/:title', function (req, res) {
    const title = req.params.title;
    let selectedBooks = {};
    for (let bookId in books) {
        if (books[bookId].title == title) {
            selectedBooks[bookId] = books[bookId];
        } 
    }
    res.status(200).json(selectedBooks);
});

// Get book review
public_users.get('/review/:isbn', function (req, res) {
    const isbn = req.params.isbn;
    res.status(200).json(books[isbn].reviews);
});

// Task 10
public_users.get('/task10', async function (req, res) {
    try {
        const response = await axios.get(URL + '/');
        const books = response.data;

        res.status(200).json(books);
    } catch (error) {
        res.status(500).json({error: 'Internal server error'});
    }
});

// Task 11
public_users.get('/task11/:isnb', async function (req, res) {
    try {
        const isnb = req.params.isnb;
        const response = await axios.get(URL + '/isbn/' + isnb);
        const books = response.data;

        res.status(200).json(books);
    } catch (error) {
        res.status(500).json({error: 'Internal server error'});
    }
});

// Task 12
public_users.get('/task12/:author', async function (req, res) {
    try {
        const author = req.params.author;
        const response = await axios.get(URL + '/author/' + author);
        const books = response.data;

        res.status(200).json(books);
    } catch (error) {
        res.status(500).json({error: 'Internal server error'});
    }
});

// Task 13
public_users.get('/task13/:title', async function (req, res) {
    try {
        const title = req.params.title;
        const response = await axios.get(URL + '/title/' + title);
        const books = response.data;

        res.status(200).json(books);
    } catch (error) {
        res.status(500).json({error: 'Internal server error'});
    }
});

module.exports.general = public_users;