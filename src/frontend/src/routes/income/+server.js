import { json } from "@sveltejs/kit";

export function GET() {
    const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const values = [10, 14, 13, 25, 66, 29, 41, 52, 69, 60, 77, 88];

    return json({ labels: labels, values: values });
}