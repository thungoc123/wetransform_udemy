import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(function Input(
	{ className, ...props },
	ref,
) {
	return <input ref={ref} className={cn("text-input", className)} {...props} />;
});
