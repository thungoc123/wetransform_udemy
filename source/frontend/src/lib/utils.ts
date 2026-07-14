export function cn(...parts: Array<string | false | null | undefined>): string {
	return parts.filter(Boolean).join(" ");
}

export function formatCountdown(ms: number): string {
	if (ms <= 0) {
		return "00:00";
	}

	const totalSeconds = Math.ceil(ms / 1000);
	const minutes = Math.floor(totalSeconds / 60)
		.toString()
		.padStart(2, "0");
	const seconds = (totalSeconds % 60).toString().padStart(2, "0");

	return `${minutes}:${seconds}`;
}
