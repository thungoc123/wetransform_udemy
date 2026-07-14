import * as React from "react";
import { cn } from "@/lib/utils";

type ButtonVariant = "primary" | "secondary";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
	variant?: ButtonVariant;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(function Button(
	{ className, variant = "primary", ...props },
	ref,
) {
	return (
		<button
			ref={ref}
			className={cn(
				"button",
				variant === "primary" ? "button-primary" : "button-secondary",
				className,
			)}
			{...props}
		/>
	);
});
