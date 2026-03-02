import { Redis } from '@upstash/redis';

const redis = Redis.fromEnv();
const KV_KEY = 'reviews';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const data = await redis.get(KV_KEY);
    return res.status(200).json(data || []);
  }

  if (req.method === 'PUT') {
    const reviews = req.body;
    if (!Array.isArray(reviews)) {
      return res.status(400).json({ error: 'Body must be a JSON array' });
    }
    await redis.set(KV_KEY, reviews);
    return res.status(200).json({ ok: true });
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
