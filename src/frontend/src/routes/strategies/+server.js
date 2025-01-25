import { json } from "@sveltejs/kit";
import strategies from "$lib/data/strategies.json";

export function GET() {
    const data = strategies.data;

    return json({ data: data });
}