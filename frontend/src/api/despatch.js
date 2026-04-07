const BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function register(email, password, name) {
  const res = await fetch(`${BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name }),
  })
  return res
}

export async function login(email, password) {
  const res = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  return res
}

export async function logout(token) {
  const res = await fetch(`${BASE_URL}/api/auth/logout`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
  })
  return res
}

function authHeaders(token) {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
  }
}

export async function generateDespatch(orderXml, token) {
  const res = await fetch(`${BASE_URL}/api/despatch/despatch-advice`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(orderXml),
  })
  return res
}

export async function getAllDespatches(token) {
  const res = await fetch(`${BASE_URL}/api/despatch/despatch-advice`, {
    headers: authHeaders(token),
  })
  return res
}

export async function getDespatch(id, token) {
  const res = await fetch(`${BASE_URL}/api/despatch/despatch-advice/${id}`, {
    headers: authHeaders(token),
  })
  return res
}

export async function updateDespatch(id, body, token) {
  const res = await fetch(`${BASE_URL}/api/despatch/despatch-advice/${id}`, {
    method: 'PUT',
    headers: authHeaders(token),
    body: JSON.stringify(body),
  })
  return res
}

export async function deleteDespatch(id, token) {
  const res = await fetch(`${BASE_URL}/api/despatch/despatch-advice/${id}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  })
  return res
}