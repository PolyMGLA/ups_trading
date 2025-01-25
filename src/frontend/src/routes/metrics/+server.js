import { json } from "@sveltejs/kit";
import metrics from "$lib/data/metrics.json";

export function GET() {
    const data = metrics.data;

    return json({ data: data });
}