import { json } from "@sveltejs/kit";
import income from "$lib/data/income.json";

export function GET() {
    const labels = income.labels;
    const values = income.values;

    return json({ labels: labels, values: values });
}