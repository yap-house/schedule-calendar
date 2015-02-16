#!/usr/local/bin/gosh


(define (view-show-report y m d)
  (let
      ((start (get-data (dbm-key-start y m d)))
       (end (get-data (dbm-key-end y m d)))
       (total (get-data (dbm-key-total y m d)))
       (comment (get-data (dbm-key-comment y m d))))

    (page
     (html:h2 #`",|y|年,|m|月,|d|日の日報" (html:a :href #`"?y=,|y|&m=,|m|&d=,|d|&status=e" "[予定を編集]"))
     (html:dl :class "report"
              (html:dt "出勤:")
              (html:dd (html-escape-string start))
              (html:dt "退勤:")
              (html:dd (html-escape-string end))
              (html:dt "勤務時間:")
              (html:dd (html-escape-string total))
              (html:dt "コメント:")
              (html:td (html-escape-string comment))))))

