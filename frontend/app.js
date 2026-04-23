const express = require('express')
const path = require('path')
const app = express()

const PORT = process.env.PORT || 3000
const API_URL = process.env.API_URL || 'http://api:8000'

app.use(express.json())
app.use(express.static(path.join(__dirname, 'views')))

app.post('/submit', async (req, res) => {
  try {
    const response = await fetch(`${API_URL}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    const data = await response.json()
    res.json(data)
  } catch (err) {
    res.status(500).json({ error: err.message })
  }
})

app.get('/status/:id', async (req, res) => {
  try {
    const response = await fetch(`${API_URL}/status/${req.params.id}`)
    const data = await response.json()
    res.json(data)
  } catch (err) {
    res.status(500).json({ error: err.message })
  }
})

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'))
})

app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`)
})