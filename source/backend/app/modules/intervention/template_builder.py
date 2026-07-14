def build_default_template(lesson_name: str) -> str:
    """
    Builds the default email template for at-risk students.
    The placeholders {student_name} and {best_practice_tip} will be
    replaced dynamically before sending.
    """
    return (
        "Chào {student_name},\n\n"
        f"Bạn đang học dở bài '{lesson_name}'. Đừng bỏ cuộc nhé!\n\n"
        "Mẹo học tập: {best_practice_tip}\n\n"
        "Trân trọng,\nĐội ngũ Giảng viên"
    )
