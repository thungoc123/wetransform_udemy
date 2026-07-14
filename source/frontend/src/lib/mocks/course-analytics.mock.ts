import {
  AIInsightData,
  CourseOverviewData,
  DropOffAnalysisData,
  LessonDetailData,
  LessonDropOffItem,
} from "@/types/course-analytics";

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

const COURSE_OPTIONS = [
  { id: "course-001", title: "AI Fundamentals For Educators" },
  { id: "course-002", title: "Data Storytelling In LMS" },
  { id: "course-003", title: "Practical Prompt Engineering" },
];

const LESSONS: LessonDropOffItem[] = [
  {
    lessonId: "lesson-01",
    lessonTitle: "Lesson 1 - Intro To Learning Signals",
    lessonType: "video",
    learnerCount: 122,
    dropOffRate: 13,
  },
  {
    lessonId: "lesson-02",
    lessonTitle: "Lesson 2 - Student Motivation Patterns",
    lessonType: "video",
    learnerCount: 95,
    dropOffRate: 27,
  },
  {
    lessonId: "lesson-03",
    lessonTitle: "Lesson 3 - Practice Worksheet",
    lessonType: "exercise",
    learnerCount: 84,
    dropOffRate: 22,
  },
  {
    lessonId: "lesson-04",
    lessonTitle: "Lesson 4 - Capstone Demo",
    lessonType: "video",
    learnerCount: 24,
    dropOffRate: 36,
  },
];

const TIMELINE = [
  { second: 30, retention: 98 },
  { second: 60, retention: 94 },
  { second: 120, retention: 85 },
  { second: 180, retention: 74 },
  { second: 240, retention: 62 },
  { second: 300, retention: 57 },
  { second: 360, retention: 49 },
];

export async function getCourseOverviewMock(
  courseId: string,
  state: "default" | "empty" | "loading-error",
): Promise<CourseOverviewData> {
  await delay(700);

  if (state === "loading-error") {
    throw new Error("Unable to load course overview");
  }

  if (state === "empty") {
    throw new Error("NO_DATA");
  }

  const selected = COURSE_OPTIONS.find((course) => course.id === courseId) ?? COURSE_OPTIONS[0];

  return {
    courseId: selected.id,
    courseTitle: selected.title,
    options: COURSE_OPTIONS,
    metrics: {
      completionRate: 78,
      dropOffRate: 24,
      active: 640,
      inactive: 212,
      atRisk: 143,
    },
  };
}

export async function getDropOffAnalysisMock(
  courseId: string,
  threshold: number,
): Promise<DropOffAnalysisData> {
  await delay(750);

  if (courseId === "empty") {
    throw new Error("NO_DATA");
  }

  return {
    courseId,
    threshold,
    lessons: LESSONS,
  };
}

export async function getLessonDetailMock(
  courseId: string,
  lessonId: string,
): Promise<LessonDetailData> {
  await delay(700);

  const lesson = LESSONS.find((item) => item.lessonId === lessonId);
  if (!lesson) {
    throw new Error("NOT_FOUND");
  }

  return {
    courseId,
    lessonId,
    lessonTitle: lesson.lessonTitle,
    lessonType: lesson.lessonType,
    learnerCount: lesson.learnerCount,
    dropOffRate: lesson.dropOffRate,
    completionRate: 100 - lesson.dropOffRate,
    timeline: lesson.lessonType === "video" ? TIMELINE : [],
    fallbackDistribution:
      lesson.lessonType === "video"
        ? undefined
        : {
            completed: 52,
            incomplete: 21,
            droppedMidway: 11,
          },
  };
}

export async function getAIInsightsMock(lessonId: string): Promise<AIInsightData> {
  await delay(600);

  return {
    lessonId,
    insights: [
      {
        id: "insight-01",
        hypothesis: "Video segment from minute 3 to 6 is too dense for first-time learners.",
        suggestion: "Split section into two shorter clips and add a quick recap checkpoint.",
        status: "pending",
      },
      {
        id: "insight-02",
        hypothesis: "Practice task appears after a long theory block causing motivation drop.",
        suggestion: "Move one guided exercise earlier to rebalance theory vs practice.",
        status: "pending",
      },
      {
        id: "insight-03",
        hypothesis: "Recommendation may require custom interaction not available in Udemy editor.",
        suggestion: "Add mini interactive activity externally and reference it in lecture notes.",
        manualOnly: true,
        status: "pending",
      },
    ],
  };
}