export type DataMethod = "api" | "file";

export type IntegrationErrorCode =
  | "INVALID_CREDENTIALS"
  | "API_TIMEOUT"
  | "FORMAT_INVALID"
  | "MISSING_COLUMNS"
  | "MVP_LIMIT_EXCEEDED"
  | "PROCESSING_FAILED";

export interface ApiCredentialsInput {
  clientId: string;
  apiKey: string;
}

export interface ApiConnectSuccess {
  ok: true;
  scenario: "success" | "warning";
}

export interface ApiConnectFailure {
  ok: false;
  code: IntegrationErrorCode;
  message: string;
}

export type ApiConnectResult = ApiConnectSuccess | ApiConnectFailure;

export interface UploadValidationSuccess {
  ok: true;
  scenario: "success" | "warning";
  fileName: string;
}

export interface UploadValidationFailure {
  ok: false;
  code: IntegrationErrorCode;
  message: string;
  missingColumns?: string[];
}

export type UploadValidationResult = UploadValidationSuccess | UploadValidationFailure;

export interface ProcessingStep {
  id: string;
  label: string;
}

export interface ProcessingResult {
  status: "success" | "error";
  message: string;
  warning?: string;
}