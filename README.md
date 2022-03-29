
# 🤖Hashptcha

Proof-of-Work CAPTCHA with password cracking functionality


![Working demo GIF](/readme_img/demo-gif.gif "Working demo GIF").


## 💡 About
Current CAPTCHA implementations are frustrating yet necessary part of every online form. Despite it's presence many services still struggle with unwanted SPAM and automation from bad actors. What's more there are numerous services providing cheap CAPTCHA-solving services and or even machine learning tools - [Buster](https://chrome.google.com/webstore/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl) being just one example.

What if instead of requiring user to click fire hydrants, we ask him to donate small amount of his CPU computing power to solve a "cryptographic puzzle". Said puzzle is just a password hash we want to crack.

Solution is elegant, easily scalable *(both in terms of amount of users using it and task difficulty)* and partially solves the problem of wasted energy and computing power which was one of the main criticisms of Hashcash and Proof-of-Work in general.

## ⚙️ How it works
After clicking the *"I am not a robot"* button, client receives a following cryptographic puzzle to solve:

```
{
	hash_type: 'MD5',
	start_point: '100110000111001000000101',
	target: '10001000010111101100',
	token: '44b0f554-1348-42be-a3f5-c24885611530'
}
```
where:

 - **hash_type** - defines what hash function needs to be used (currently service supports only MD5 and SHA256)
 - **start_point** - binary representation of a starting value used for cracking. Correct solution needs to find value higher than start_point
 - **target** - hashcash-style target. Defines prefix of binary representation of calculated hash. Used to regulate difficulty and ensure user is not coming up with random hashes
 - **token** - random value associated with the task. Used to ensure that noone tries to replay the same task more than once

Once user finds the solution, he then sends the solution to the application back-end alongside his form data. Server sends following request to the Hashptcha service provider to ensure the puzzle has been solved correctly:
```
{
	token: '44b0f554-1348-42be-a3f5-c24885611530',
	value: '101010001000110011110101',
	secret_key: '0c7906a0-8c45-4cb1-b8b2-cf8cd259d7fd'
}
```
where:

 - **token** - random value associated with the task. Same as before
 - **value** - binary representation of a value, which hash achieves the target. Additionaly value must be higher than start_point
 - **secret_key** - random value used to identify website using the service. You can think of it as an API key.

Simplified service flow can be seen on the picture below.
![Application Flow](/readme_img/ApplicationFlow.png "Simplified application Flow").


## 🛠️ TODO

 - Add more hash functions
 - **Calculations on homomorphic encryption instead of hash cracking?**

## 📚 References

 - [hash-wasm](https://www.npmjs.com/package/hash-wasm) - WebAssembly implementation of most popular hash functions
 - [Hashcash - A Denial of Service Counter-Measure](http://www.hashcash.org/papers/hashcash.pdf)

