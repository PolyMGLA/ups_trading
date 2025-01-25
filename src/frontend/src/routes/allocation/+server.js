import { json } from "@sveltejs/kit";
import allocation from "$lib/data/allocation.json";

export function GET() {
    const labels = allocation.labels;
    const values = allocation.values;

    return json({ labels: labels, values: values });
}