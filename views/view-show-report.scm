#!/usr/local/bin/gosh


(define (view-show-report start end total comment)
    (page
     (html:h2 #`",|y|年,|m|月,|d|日の日報" (html:a :href #`"?y=,|y|&m=,|m|&d=,|d|&status=e" "[予定を編集]"))
     (html:dl :class "report"
              (html:dt "出勤:")
              (html:dd (html-escape-string (get-data start)))
              (html:dt "退勤:")
              (html:dd (html-escape-string (get-data end)))
              (html:dt "勤務時間:")
              (html:dd (html-escape-string (get-data total)))
              (html:dt "コメント:")
              (html:td (html-escape-string (get-data comment))))))
