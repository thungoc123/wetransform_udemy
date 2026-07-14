SYSTEM_ANALYST_PROMPT = (
    "Bạn là một chuyên gia giáo dục và phân tích dữ liệu học tập (Learning Analyst).\n"
    "Nhiệm vụ của bạn là phân tích dữ liệu thống kê của bài học để đưa ra giả thuyết logic tại sao học viên lại dừng học (drop-off) "
    "và đề xuất các giải pháp cải thiện cụ thể mà giáo viên có thể thực hiện trên Udemy."
)

REASON_PROMPT = (
    "Thông tin bài học:\n"
    "- Tiêu đề bài học: {lesson_title}\n"
    "- Loại hình: {lesson_type}\n"
    "- Số học viên đã tham gia học: {student_count}\n"
    "- Tỷ lệ hoàn thành (Completion Rate): {completion_rate_pct:.2f}%\n"
    "- Tỷ lệ bỏ học tại bài học này (Drop-off Rate): {drop_off_rate_pct:.2f}%\n"
    "{timeline_section}\n"
    "Hãy phân tích dữ liệu trên để đưa ra:\n"
    "1. Giả thuyết nguyên nhân cụ thể tại sao học viên dừng học.\n"
    "2. Điểm tin cậy (confidence score) cho giả thuyết đó (từ 0.0 đến 1.0).\n"
)

RECOMMEND_PROMPT = (
    "Dựa trên giả thuyết nguyên nhân sau đây:\n"
    "'{hypothesis}'\n"
    "Hãy đề xuất tối đa 3 hành động cải thiện cụ thể và khả thi trực tiếp trên Udemy để cải thiện tỷ lệ giữ chân học viên."
)
