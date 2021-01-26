{
  "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
  "@type": "http://purl.imsglobal.org/caliper/v1/AssessmentItemEvent",
  "action": "http://purl.imsglobal.org/vocab/caliper/v1/action#\(.action)",
  "actor": {
    "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
    "@id": "https://mcommunity.umich.edu/#profile:\(.actorUniqname)",
    "@type": "http://purl.imsglobal.org/caliper/v1/lis/Person",
    "name": .actorUniqname,
  },
  "edApp": {
    "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
    "@id": "https://problemroulette.lsa.umich.edu/",
    "@type": "http://purl.imsglobal.org/caliper/v1/SoftwareApplication",
  },
  "eventTime": .endTime,
  "extensions": {
    "edu.umich": {
      "description": "Event regenerated from application data, not live interaction.",
      "regeneratedTime": (now|todateiso8601),
    },
  },
  "generated": {
    "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
    "@id": "\(.problemUrl)/response",
    "@type": "http://purl.imsglobal.org/caliper/v1/MultipleChoiceResponse",
    "attempt": {
      "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
      "@id": "\(.problemUrl)/attempt",
      "@type": "http://purl.imsglobal.org/caliper/v1/Attempt",
      "count": .attemptCountNum,
      "duration": .durationSeconds,
      "endedAtTime": .endTime,
      "startedAtTime": .startTime,
    },
    "extensions": {
      "correctAnswer": "\(.correctAnswer)",
      "isStudentAnswerCorrect": "\(.isAnswerCorrect)",
    },
    "value": "\(.actorAnswer)",
  },
  "group": {
    "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
    "@id": "https://problemroulette.lsa.umich.edu/courses/\(.courseIdNum)",
    "@type": "http://purl.imsglobal.org/caliper/v1/lis/CourseOffering",
    "name": .courseName,
  },
  "object": {
    "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
    "@id": .problemUrl,
    "@type": "http://purl.imsglobal.org/caliper/v1/AssessmentItem",
    "isPartOf": {
      "@context": "http://purl.imsglobal.org/ctx/caliper/v1/Context",
      "@id": "https://problemroulette.lsa.umich.edu/courses/\(.courseIdNum)/topics/\(.topicIdNum)",
      "@type": "http://purl.imsglobal.org/caliper/v1/Assessment",
      "name": .topicName,
    },
    "name": .problemName,
  },
}
