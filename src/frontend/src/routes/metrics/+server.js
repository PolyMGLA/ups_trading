import { json } from "@sveltejs/kit";

export function GET() {
    const data = {
        pnl: 46,
        sharp: 46,
        profit_margin: 46,
        max_drawdown: 46,
        turnover: 46
    };

    return json({ data: data });
}