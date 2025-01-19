import { json } from "@sveltejs/kit";

export function GET() {
    const labels = ['BTC, ETH', 'Альт-коины', 'Стейбл-коины'];
    const values = [27, 43, 50];

    return json({ labels: labels, values: values });
}