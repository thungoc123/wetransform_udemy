import {
  ApiConnectResult,
  ApiCredentialsInput,
  DataMethod,
  ProcessingResult,
  ProcessingStep,
  UploadValidationResult,
} from "@/types/data-integration";

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

export const PROCESSING_STEPS: ProcessingStep[] = [
  { id: "validate", label: "Validate schema" },
  { id: "parse", label: "Parse dataset" },
  { id: "anonymize", label: "Anonymize PII" },
  { id: "store", label: "Store records" },
];

export async function connectUdemyApiMock(input: ApiCredentialsInput): Promise<ApiConnectResult> {
  await delay(850);

  const clientId = input.clientId.trim().toLowerCase();
  const apiKey = input.apiKey.trim().toLowerCase();

  if (clientId.includes("invalid") || apiKey.includes("invalid")) {
    return {
      ok: false,
      code: "INVALID_CREDENTIALS",
      message: "Kết nối thất bại. Vui lòng kiểm tra lại Client ID hoặc API Key của bạn.",
    };
  }

  if (apiKey.includes("timeout") || apiKey.includes("ratelimit")) {
    return {
      ok: false,
      code: "API_TIMEOUT",
      message: "Hệ thống Udemy đang bận hoặc quá tải. Vui lòng thử lại sau ít phút.",
    };
  }

  if (apiKey.includes("overlimit")) {
    return {
      ok: false,
      code: "MVP_LIMIT_EXCEEDED",
      message:
        "Vượt quá giới hạn phiên bản thử nghiệm (MVP): tối đa 3 khóa học và 2.600 học viên.",
    };
  }

  return {
    ok: true,
    scenario: apiKey.includes("inconsistent") ? "warning" : "success",
  };
}

export async function validateUdemyFileMock(file: File): Promise<UploadValidationResult> {
  await delay(700);

  const lowerName = file.name.toLowerCase();
  const isAllowed = lowerName.endsWith(".csv") || lowerName.endsWith(".xlsx");
  if (!isAllowed) {
    return {
      ok: false,
      code: "FORMAT_INVALID",
      message: "Tải lên thất bại. Chỉ hỗ trợ file CSV/XLSX xuất chuẩn từ Udemy.",
    };
  }

  if (lowerName.includes("missing-columns")) {
    return {
      ok: false,
      code: "MISSING_COLUMNS",
      message:
        "Tải lên thất bại. Tệp không đúng cấu trúc xuất chuẩn của Udemy. Vui lòng tải lại tệp chuẩn.",
      missingColumns: ["User ID", "Lesson Completed", "Timestamp"],
    };
  }

  if (lowerName.includes("over-limit") || lowerName.includes("overlimit")) {
    return {
      ok: false,
      code: "MVP_LIMIT_EXCEEDED",
      message:
        "Vượt quá giới hạn phiên bản thử nghiệm (MVP): tối đa 3 khóa học và 2.600 học viên.",
    };
  }

  return {
    ok: true,
    scenario: lowerName.includes("inconsistent") ? "warning" : "success",
    fileName: file.name,
  };
}

export async function finalizeProcessingMock(
  method: DataMethod,
  scenario: "success" | "warning" | "error",
): Promise<ProcessingResult> {
  await delay(400);

  if (scenario === "error") {
    return {
      status: "error",
      message: "Xử lý dữ liệu thất bại. Vui lòng kiểm tra dữ liệu và thử lại.",
    };
  }

  const successMessage =
    method === "api"
      ? "Kết nối Udemy API thành công và dữ liệu đã được đồng bộ."
      : "Tải file dữ liệu thành công và dữ liệu đã được nạp vào hệ thống.";

  if (scenario === "warning") {
    return {
      status: "success",
      message: successMessage,
      warning:
        "Cảnh báo: một phần học viên thiếu lịch sử hoạt động nên không thể phân tích đầy đủ.",
    };
  }

  return {
    status: "success",
    message: successMessage,
  };
}