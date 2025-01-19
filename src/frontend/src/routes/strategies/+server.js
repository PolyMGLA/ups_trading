import { json } from "@sveltejs/kit";

export function GET() {
    const data = [
        { name: "Anti-mainstream 1", rating: 60, cost: "$46,000", color: "bg-yellow-400" },
        { name: "Anti-mainstream 2", rating: 17, cost: "$17,000", color: "bg-blue-400" },
        { name: "Anti-mainstream 3", rating: 19, cost: "$19,000", color: "bg-teal-400" },
        { name: "Anti-mainstream 4", rating: 29, cost: "$29,000", color: "bg-pink-400" },
    ];

    return json({ data: data });
}