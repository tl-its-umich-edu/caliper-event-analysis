SELECT
  # Return JSONL (i.e., individual JSON objects, without commas in between)
  json_object(
      'action', CASE responses.answer
                WHEN 0
                  THEN 'Skipped'
                ELSE 'Completed' END,
      'actorAnswer', concat('', responses.answer), # String coercion
      'actorUniqname', user.username,
      'attemptCountNum', (
        # Subquery: Count answers user gave before and including this one.
        SELECT count(*)
        FROM responses AS attempt_responses
        WHERE
          attempt_responses.prob_id = responses.prob_id AND
          attempt_responses.user_id = responses.user_id AND
          attempt_responses.end_time <= responses.end_time
      ),
      'correctAnswer', concat('', problems.correct), # String coercion
      'courseIdNum', class.id,
      'courseName', class.name,
      'durationSeconds', concat(
          'PT', timestampdiff(SECOND, start_time, end_time), 'S'), # ISO 8601 period
      'endTime', date_format(convert_tz(responses.end_time, @@session.time_zone, '+00:00'),
                             '%Y-%m-%dT%TZ'), # as GMT in ISO 8601
      'isAnswerCorrect', CASE ans_correct
                         WHEN 1
                           THEN 'true'
                         ELSE 'false' END, # Convert 0/1 to Boolean *string*
      'problemName', problems.name,
      'problemUrl', problems.url,
      'startTime', date_format(convert_tz(responses.start_time, @@session.time_zone, '+00:00'),
                               '%Y-%m-%dT%TZ'), # as GMT in ISO 8601
      'topicIdNum', topic.id,
      'topicName', topic.name
  ) AS json
FROM
  responses
  INNER JOIN problems ON responses.prob_id = problems.id
  INNER JOIN topic ON responses.topic_id = topic.id
  INNER JOIN `user` ON responses.user_id = `user`.id
  INNER JOIN `12m_class_topic` ON responses.topic_id = `12m_class_topic`.topic_id
  INNER JOIN class ON `12m_class_topic`.class_id = class.id
WHERE
  #   responses.end_time > '2016-06-26 00:00:00' # Caliper feature deployment date (EST)
  #   AND `user`.id = 11447 AND problems.id = 942 # Helpful test criteria
  #   AND
  responses.end_time >= convert_tz(
      '2016-10-19T02:22:06.383Z', '+00:00', @@session.time_zone
  ) # Caliper feature interruption begins (from GMT in ISO 8601)
  AND
  responses.end_time <= convert_tz(
      '2016-12-14T04:43:05.264Z', '+00:00', @@session.time_zone
  ) # Caliper feature interruption ends (from GMT in ISO 8601)
ORDER BY
  responses.end_time ASC
LIMIT
  10