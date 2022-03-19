let currently_working = false;
let solved_data;

// Verification for debugging purposes
function verify(data) {
	fetch('/verify', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(data),
	})
		.then(response => response.json())
		.then(data => {
			console.log('Success:', data);
		})
		.catch((error) => {
			console.error('Error:', error);
		});
}

const hex2bin = (data) => data.split('').map(i =>
	parseInt(i, 16).toString(2).padStart(4, '0')).join('');

async function md5(data) {
	return hashwasm.md5(data);
}

async function sha256(data) {
	return hashwasm.sha256(data);
}

async function binary_to_uint8(data) {
	let int8Buffer = [];
	for(let i =0; i<(data.length/8); i++) {
		let chunk = data.substring(i*8, (i+1)*8);
		int8Buffer.push( parseInt(chunk, 2) );
	}
	const uint8Array = new Uint8Array(int8Buffer);
	return uint8Array;
}

async function start_work(data) {
	currently_working = true;
	let count = 0;
	let data_to_return = {
		"token": data["token"],
		"value": NaN,
	}
	let alg_type = data['hash_type'];
	let hash_func;
	if (alg_type == 'MD5') hash_func = md5;
	else if (alg_type == 'SHA256') hash_func = sha256;
	
	console.log("Difficulty target: ", data["target"].length);
	console.log("Starting point: ", data['start_point']);
	let point = data['start_point'];
	while(true) {
		point = point.padStart(8*Math.ceil(point.length/8), '0');
		if(count >= 10000) break;
		let uint8Buffer = await binary_to_uint8(point);
		const value_hashed = await hash_func(uint8Buffer);
		count++;
		const hash_binary = hex2bin(value_hashed);
		const hash_binary_trimmed = hash_binary.substring(0, data['target'].length);
		if (hash_binary_trimmed == data['target']) {
			data_to_return["value"] = point;
			break;
		}
		point = addBinary(point, '1');
	}
	console.log("Loop ended!");
	console.log("Hashed counter: ", count);
	console.log(data_to_return);
	return data_to_return;
	for (let str of allStrings(DICT)) {
		const value = data['start_point'] + str;
		const value_hashed = await hash_func(value);
		count++;
		const hash_binary = hex2bin(value_hashed);
		const hash_binary_trimmed = hash_binary.substring(0, data['target'].length);
		if (hash_binary_trimmed == data['target']) {
			data_to_return["value"] = value;
			break;
		}
	}
	console.log("Hashed counter: ", count);
	return data_to_return;
}

function markAsDone() {
	$("#loader").hide();
	$("#task-done").fadeIn();
	$('#task-done').css('display','inline-block');
}

function showLoader() {
	$("#square-start").hide();
	$("#loader").show();
	$('#loader').css('display','inline-block');
}

function fetchTask() {
	showLoader();
	fetch('/get-task')
		.then(response => response.json())
		.then(data => {
			console.log(data);
			const task_completed = start_work(data).then((x) => {
				solved_data = x;
				markAsDone();
				verify(solved_data); //verification for debuggging purposes
				window.parent.postMessage(solved_data, '*');
				currently_working = false;
			});
		});
}

$("#square-start").click(function () {
	if (currently_working == false) fetchTask();
});





/**
 * @param {string} a
 * @param {string} b
 * @return {string}
 */

// logic gates
function xor(a, b) {
	return a === b ? 0 : 1;
  }
  
  function and(a, b) {
	return a == 1 && b == 1 ? 1 : 0;
  }
  
  function or(a, b) {
	return a || b;
  }
  
  function halfAdder(a, b) {
	const sum = xor(a, b);
	const carry = and(a, b);
	return [sum, carry];
  }
  
  function fullAdder(a, b, carry) {
	halfAdd = halfAdder(a, b);
	const sum = xor(carry, halfAdd[0]);
	carry = and(carry, halfAdd[0]);
	carry = or(carry, halfAdd[1]);
	return [sum, carry];
  }
  
  function padZeroes(a, b) {
	const lengthDifference = a.length - b.length;
	switch (lengthDifference) {
	  case 0:
		break;
	  default:
		const zeroes = Array.from(Array(Math.abs(lengthDifference)), () =>
		  String(0)
		);
		if (lengthDifference > 0) {
		  // if a is longer than b
		  // then we pad b with zeroes
		  b = `${zeroes.join('')}${b}`;
		} else {
		  // if b is longer than a
		  // then we pad a with zeroes
		  a = `${zeroes.join('')}${a}`;
		}
	}
	return [a, b];
  }
  
  function addBinary(a, b) {
	let sum = '';
	let carry = '';
  
	const paddedInput = padZeroes(a, b);
	a = paddedInput[0];
	b = paddedInput[1];
  
	for (let i = a.length - 1; i >= 0; i--) {
	  if (i == a.length - 1) {
		// half add the first pair
		const halfAdd1 = halfAdder(a[i], b[i]);
		sum = halfAdd1[0] + sum;
		carry = halfAdd1[1];
	  } else {
		// full add the rest
		const fullAdd = fullAdder(a[i], b[i], carry);
		sum = fullAdd[0] + sum;
		carry = fullAdd[1];
	  }
	}
	return carry ? carry + sum : sum;
  }