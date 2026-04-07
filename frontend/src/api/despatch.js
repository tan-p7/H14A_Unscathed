const BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function generateDespatch(orderXml) {
  const res = await fetch(`${BASE_URL}/despatch-advice`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(orderXml),
  })
  return res
}

export async function getAllDespatches() {
  const res = await fetch(`${BASE_URL}/despatch-advice`)
  return res
}

export async function getDespatch(id) {
  const res = await fetch(`${BASE_URL}/despatch-advice/${id}`)
  return res
}

export async function updateDespatch(id, body) {
  const res = await fetch(`${BASE_URL}/despatch-advice/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return res
}

export async function deleteDespatch(id) {
  const res = await fetch(`${BASE_URL}/despatch-advice/${id}`, {
    method: 'DELETE',
  })
  return res
}