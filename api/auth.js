export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { token } = req.body || {};
  if (!token || token !== process.env.ACCESS_TOKEN) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  return res.status(200).json({ ok: true });
}
