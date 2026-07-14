import * as React from "react";
import { cn } from "@/lib/utils";

export function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
	return <div className={cn("metric-card", className)} {...props} />;
}

export function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
	return <p className={cn("metric-label", className)} {...props} />;
}

export function CardValue({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
	return <p className={cn("metric-value", className)} {...props} />;
}

export function CardNote({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
	return <p className={cn("metric-note", className)} {...props} />;
}
