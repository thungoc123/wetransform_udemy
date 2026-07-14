export type StudentBand = "active" | "inactive" | "at-risk";

export interface CourseOption {
  id: string;
  title: string;
}

export interface CourseOverviewMetrics {
  completionRate: number;
  dropOffRate: number;
  active: number;
  inactive: number;
  atRisk: number;
}

export interface CourseOverviewData {
  courseId: string;
  courseTitle: string;
  metrics: CourseOverviewMetrics;
  options: CourseOption[];
}

export interface LessonDropOffItem {
  lessonId: string;
  lessonTitle: string;
  lessonType: "video" | "exercise" | "document";
  learnerCount: number;
  dropOffRate: number;
}

export interface DropOffAnalysisData {
  courseId: string;
  threshold: number;
  lessons: LessonDropOffItem[];
}

export interface LessonTimelinePoint {
  second: number;
  retention: number;
}

export interface LessonDetailData {
  courseId: string;
  lessonId: string;
  lessonTitle: string;
  lessonType: "video" | "exercise" | "document";
  learnerCount: number;
  dropOffRate: number;
  completionRate: number;
  timeline: LessonTimelinePoint[];
  fallbackDistribution?: {
    completed: number;
    incomplete: number;
    droppedMidway: number;
  };
}

export interface AIInsightItem {
  id: string;
  hypothesis: string;
  suggestion: string;
  manualOnly?: boolean;
  status: "pending" | "applied" | "dismissed";
}

export interface AIInsightData {
  lessonId: string;
  insights: AIInsightItem[];
}