const BASE_URL = "http://127.0.0.1:8000/api";
let token = localStorage.getItem("token");

// AUTO LOGIN
if (token) {
  showDashboard();
}

// AUTH
async function register() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();
  document.getElementById("auth-msg").innerText = JSON.stringify(data);
}

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (data.access_token) {
    token = data.access_token;
    localStorage.setItem("token", token);
    showDashboard();
  } else {
    document.getElementById("auth-msg").innerText = "Login failed";
  }
}

function logout() {
  localStorage.removeItem("token");
  location.reload();
}

function showDashboard() {
  document.getElementById("auth-section").classList.add("hidden");
  document.getElementById("dashboard").classList.remove("hidden");
}

// FILE UPLOAD
async function uploadFile() {
  const file = document.getElementById("file").files[0];
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/ingestion/upload`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    },
    body: formData
  });

  const data = await res.json();
  showOutput(data);
}

// QUERY
async function askQuery() {
  const query = document.getElementById("query").value;

  const res = await fetch(`${BASE_URL}/query/ask?query=${query}`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await res.json();
  showOutput(data.response);
}

// EMAIL
async function generateEmail() {
  const task = document.getElementById("emailTask").value;

  const res = await fetch(`${BASE_URL}/email/generate?task=${task}`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await res.json();
  showOutput(data.email);
}

// CALL
async function generateCall() {
  const task = document.getElementById("callTask").value;

  const res = await fetch(`${BASE_URL}/call/generate?task=${task}`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await res.json();
  showOutput(data.call_script);
}

// AGENT
async function runAgent() {
  const task = document.getElementById("agentTask").value;

  const res = await fetch(`${BASE_URL}/agent/run?task=${task}`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await res.json();
  showOutput(data.result);
}

// OUTPUT
function showOutput(data) {
  document.getElementById("output").innerText = JSON.stringify(data, null, 2);
}