#/usr/bin/local/gosh

(require "./functions")

(define (date-cell y m d)
  (if d
      (html:a :href #`"?y=,|y|&m=,|m|&d=,|d|" d
              (if (data-exists (dbm-key-start y m d)) (html:span :class "start" #`"出勤: ,(get-data (dbm-key-start y m d))") "")
              (if (data-exists (dbm-key-end y m d)) (html:span :class "end" #`"退勤: ,(get-data (dbm-key-end y m d))") "")
              (if (data-exists (dbm-key-total y m d)) (html:span :class"total" #`"勤務時間: ,(get-data (dbm-key-total y m d))") ""))
      ""))


(define (calendar date)
  (let ((current-year (date-year date))
        (current-month (date-month date))
        (prev-month (prev-month date))
        (next-month (next-month date)))

    `(,(html:div :class "calendar-header"
                 (html:ul
                  (html:li :class "prev-month"
                           (month->link prev-month #`"&lt; ,(date-year prev-month)/,(date-month prev-month)"))

                  (html:li :class "current-month"
                           #`",|current-year|/,|current-month|")

                  (html:li :class "next-month"
                           (month->link next-month #`",(date-year next-month)/,(date-month next-month) &gt;"))))

      ,(html:table :class "calendar"
                   (html:tr (map html:th "日月火水木金土"))
                   (map (lambda (w)
                          (html:tr
                           (map (lambda (d)
                                  (html:td (date-cell current-year current-month d)))
                                w)))
                        (date-slices-of-month date))))))
